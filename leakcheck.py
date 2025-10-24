import requests
import json
import time
import os
from datetime import datetime

# ------------------------------------------------------------
# Input and output paths
# ------------------------------------------------------------
IN_PATH = os.path.join("out", "spit_emails.txt")
OUT_PATH = os.path.join("out", "leak_results.json")

# ------------------------------------------------------------
# Sector and PII mapping for enrichment
# ------------------------------------------------------------
SOURCE_SECTOR_MAPPING = {
    "Twitter.com": "Social Media",
    "LinkedIn": "Professional Networking",
    "Facebook": "Social Media",
    "Canva": "Design / Tech",
    "Chegg.com": "Education",
    "Bigbasket.com": "E-Commerce",
    "Amazon.com": "E-Commerce",
    "Netflix": "Entertainment",
    "Zomato.com": "Food / Delivery",
    "Truecaller": "Communication",
    "Dominos": "Food / Retail",
    "Dropbox": "Cloud Storage",
    "Adobe": "Software / Tech",
}

PII_MAPPING = {
    "Twitter.com": ["Email", "Username"],
    "LinkedIn": ["Email", "Password", "Name"],
    "Canva": ["Email", "Password", "Name"],
    "Chegg.com": ["Email", "Password"],
    "Bigbasket.com": ["Email", "Phone", "Address"],
    "Amazon.com": ["Email", "Password", "Purchase History"],
    "Netflix": ["Email", "Password"],
    "Zomato.com": ["Email", "Phone"],
    "Truecaller": ["Email", "Phone", "Name"],
    "Dropbox": ["Email", "Password"],
    "Adobe": ["Email", "Password"],
}

# ------------------------------------------------------------
# LeakCheck API fetcher
# ------------------------------------------------------------
def check_leak(email):
    """Check if the email is breached using LeakCheck public API and enrich results."""
    url = f"https://leakcheck.io/api/public?check={email}"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            print(f"⚠️ HTTP {res.status_code} for {email}")
            return None

        data = res.json()
        if not data.get("success"):
            print(f"❌ API failed for {email}: {data}")
            return {"email": email, "found": 0, "sources": []}

        found = data.get("found", 0)
        sources_data = data.get("sources", [])
        enriched_sources = []

        for src in sources_data:
            name = src.get("name", "Unknown")
            breach_date = src.get("date") or src.get("last_breach") or "Unknown"
            method = src.get("method") or "Unknown Method"
            # Add sector + PII based on mapping
            sector = SOURCE_SECTOR_MAPPING.get(name, "Uncategorized")
            pii = PII_MAPPING.get(name, ["Unknown"])
            enriched_sources.append({
                "name": name,
                "date": breach_date,
                "method": method,
                "sector": sector,
                "pii": pii
            })

        return {
            "email": email,
            "found": found,
            "sources": enriched_sources
        }

    except Exception as e:
        print(f"⚠️ Error for {email}: {e}")
        return {"email": email, "found": 0, "sources": []}

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():
    if not os.path.exists(IN_PATH):
        print("❌ File not found:", IN_PATH)
        return

    with open(IN_PATH, "r", encoding="utf-8") as f:
        emails = [line.strip() for line in f if line.strip()]

    results = []
    print(f"🔍 Checking {len(emails)} emails with LeakCheck...\n")

    for i, email in enumerate(emails, start=1):
        info = check_leak(email)
        if info:
            results.append(info)
            print(f"{i:02d}. {info['email']} → {info['found']} leaks found")
        else:
            print(f"{i:02d}. {email} → failed to check")
        time.sleep(1.2)  # Prevent rate limiting

    os.makedirs("out", exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"\n✅ Done! Results saved to {OUT_PATH}")
    print("🕓 Checked at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# ------------------------------------------------------------
if __name__ == "__main__":
    main()
