import requests
import json
import time
import os

# Input and output paths
IN_PATH = os.path.join("out", "spit_emails.txt")
OUT_PATH = os.path.join("out", "leak_results.json")

# --- anonymize_email function is intentionally removed ---

def check_leak(email):
    """Check a single email using LeakCheck public API."""
    url = f"https://leakcheck.io/api/public?check={email}"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            data = res.json()
            if data.get("success") and data.get("found", 0) > 0:
                # Retain the original email
                return {
                    "email": email, 
                    "found": data["found"],
                    "sources": [src["name"] for src in data.get("sources", [])] 
                }
        # If not found
        return {"email": email, "found": 0, "sources": []}
    except Exception as e:
        print(f"⚠️ Error for {email}: {e}")
        return None

def main():
    if not os.path.exists(IN_PATH):
        print("❌ File not found:", IN_PATH)
        return

    with open(IN_PATH, "r", encoding="utf-8") as f:
        emails = [line.strip() for line in f if line.strip()]

    results = []
    print(f"🔍 Checking {len(emails)} emails with LeakCheck...\n")

    for email in emails:
        info = check_leak(email)
        if info:
            results.append(info)
            # Print the unmasked email
            print(f"✔️ {info['email']}: {info['found']} leaks found") 
        time.sleep(1.2)  # to avoid getting blocked

    # Save results to JSON
    os.makedirs("out", exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"\n✅ Done! Results saved to {OUT_PATH}")

if __name__ == "__main__":
    main()