import re
import os

# ------------------------------------------------------------
# Regex for SPIT emails (includes obfuscated forms)
# ------------------------------------------------------------
EMAIL_RE = re.compile(
    r'\b[A-Za-z0-9._%+-]+\s*(?:@|\[at\]|\(at\)|\{at\}|\s+at\s+)\s*spit\.ac\.in\b',
    re.IGNORECASE
)

# Regex for just the domain (spit.ac.in)
DOMAIN_RE = re.compile(r'\bspit\.ac\.in\b', re.IGNORECASE)


# ------------------------------------------------------------
# Normalize obfuscated emails to standard form
# ------------------------------------------------------------
def normalize_email(e):
    e = re.sub(r'\s*(?:@|\[at\]|\(at\)|\{at\}|\s+at\s+)\s*', '@', e, flags=re.IGNORECASE)
    return e.lower().strip()


# ------------------------------------------------------------
# Extract all emails and domains from one file
# ------------------------------------------------------------
def extract_from_file(path):
    """Read a file and extract all SPIT emails and domain mentions."""
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    except Exception as e:
        print(f"❌ Could not read {path}: {e}")
        return set(), 0

    # Find emails and domains
    emails_found = set(m.group(0) for m in EMAIL_RE.finditer(text))
    domain_mentions = len(DOMAIN_RE.findall(text))

    return emails_found, domain_mentions


# ------------------------------------------------------------
# Main driver
# ------------------------------------------------------------
def main():
    base_dir = os.getcwd()  # current folder
    files = [f for f in os.listdir(base_dir) if f.lower().endswith('.html')]
    if not files:
        print("❌ No HTML files found in this folder.")
        return

    all_emails = set()
    total_domains = 0
    print(f"🔍 Scanning {len(files)} HTML files...\n")

    for file in files:
        path = os.path.join(base_dir, file)
        found_emails, domain_mentions = extract_from_file(path)

        if found_emails:
            print(f"{file}: {len(found_emails)} emails found")
        else:
            print(f"{file}: 0 emails")

        all_emails |= found_emails
        total_domains += domain_mentions

    # Normalize all found emails
    normalized_emails = sorted(set(normalize_email(e) for e in all_emails))

    # Save all results
    os.makedirs("out", exist_ok=True)
    out_path = os.path.join("out", "spit_emails.txt")

    with open(out_path, "w", encoding="utf-8") as f:
        for e in normalized_emails:
            f.write(e + "\n")

    print(f"\n✅ Total {len(normalized_emails)} unique normalized @spit.ac.in emails saved to: {out_path}")
    print(f"📊 Total domain mentions (spit.ac.in found anywhere): {total_domains}")


# ------------------------------------------------------------
# Run the script
# ------------------------------------------------------------
if __name__ == "__main__":
    main()
