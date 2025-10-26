#!/usr/bin/env python3
"""
crawl_and_extract.py
Crawl a given start URL (same-domain only), extract @spit.ac.in emails (handles obfuscation),
respect robots.txt and a polite delay, and save unique emails to out/spit_emails.txt.

Usage:
    python crawl_and_extract.py
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import os
from urllib.parse import urljoin, urlparse
import collections
import urllib.robotparser
import sys

# --- CONFIG ---
START_URL = "https://www.spit.ac.in/"     # change to the site you have permission to crawl
DOMAIN = urlparse(START_URL).netloc
MAX_PAGES = 200
DELAY = 1.2           # seconds between requests
USER_AGENT = "BreachSenseCrawler/1.0 (contact: omkar.khanolkar25@spit.ac.in)"  # YOUR contact
HEADERS = {"User-Agent": USER_AGENT}

# regex for matching obfuscated emails for spit.ac.in
EMAIL_PATTERN = re.compile(
    r'([\w\.-]+)\s*(?:\[\s*at\s*\]|\(\s*at\s*\)|\s+at\s+|@)\s*spit\.ac\.in',
    flags=re.IGNORECASE
)

# --- robots.txt ---
rp = urllib.robotparser.RobotFileParser()
robots_url = urljoin(START_URL, "/robots.txt")
try:
    rp.set_url(robots_url)
    rp.read()
except Exception as e:
    # if robots cannot be read, remain conservative (still delay and limit pages)
    print(f"[warn] couldn't read robots.txt: {e}")

def allowed(url):
    try:
        return rp.can_fetch(USER_AGENT, url)
    except Exception:
        return True

# --- helpers ---
def same_domain(url):
    return urlparse(url).netloc == DOMAIN

def normalize_email(local_part):
    local = local_part.strip().lower()
    return f"{local}@spit.ac.in"

def extract_emails_from_text(text):
    found = set()
    for m in EMAIL_PATTERN.findall(text):
        # m may be either a string or tuple from capture groups
        local = m if isinstance(m, str) else m[0]
        email = normalize_email(local)
        found.add(email)
    return found

# --- crawler ---
def crawl(start_url):
    q = collections.deque([start_url])
    seen = set([start_url])
    emails = set()
    pages = 0

    session = requests.Session()
    session.headers.update(HEADERS)

    while q and pages < MAX_PAGES:
        url = q.popleft()
        if not allowed(url):
            print(f"Skipping (robots disallow): {url}")
            continue

        try:
            print(f"[{pages+1}] GET {url}")
            resp = session.get(url, timeout=20)
        except Exception as e:
            print(f"  request error: {e}")
            time.sleep(DELAY)
            continue

        pages += 1

        # ensure html
        content_type = resp.headers.get('Content-Type','')
        if resp.status_code != 200 or 'text/html' not in content_type:
            # skip non-html or error pages
            time.sleep(DELAY)
            continue

        text = resp.text
        # extract emails
        emails.update(extract_emails_from_text(text))

        # parse links and enqueue same-domain http/https links
        soup = BeautifulSoup(text, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a['href'].split('#')[0]  # drop fragment
            if not href:
                continue
            new = urljoin(url, href)
            p = urlparse(new)
            if p.scheme not in ("http", "https"):
                continue
            if not same_domain(new):
                continue
            if new not in seen:
                seen.add(new)
                q.append(new)

        time.sleep(DELAY)

    return emails

def save_emails(emails):
    os.makedirs("out", exist_ok=True)
    path = "out/spit_emails.txt"
    with open(path, "w", encoding="utf-8") as f:
        for e in sorted(emails):
            f.write(e + "\n")
    print(f"Saved {len(emails)} unique emails to {path}")

if __name__ == "__main__":
    print(f"Starting crawl: {START_URL}")
    print(f"User-Agent: {USER_AGENT}")
    try:
        found_emails = crawl(START_URL)
        save_emails(found_emails)
    except KeyboardInterrupt:
        print("\nInterrupted by user — saving whatever we found so far.")
        # attempt to save partial results if any
        try:
            save_emails(found_emails)
        except Exception:
            pass
        sys.exit(0)

