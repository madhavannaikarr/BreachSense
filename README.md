# BreachSense
SPIT Email Breach Intelligence Dashboard.BreachSense is an automated system that scans local HTML files for SPIT (spit.ac.in) email addresses, checks their exposure on LeakCheck.io, and visualizes the results in an interactive dark-web intelligence dashboard.

⚙️ Features

  🧩 Email Extraction — Detects normal and obfuscated SPIT emails from .html files.

  ✉️ Normalization — Converts obfuscated forms (e.g., [at], (at)) into valid addresses.

  🌐 Leak Verification — Uses the LeakCheck.io public API to check for breach exposure.

  📊 Interactive Dashboard — Visualizes breach statistics, charts, and sources with confetti effects for safe accounts.

  💾 Structured Output — Saves results as out/spit_emails.txt and out/leak_results.json.

🧠 How It Works

Scan HTML Files:
The first Python script searches the current directory for .html files and extracts all @spit.ac.in emails.

Check Leaks:
The second script queries LeakCheck’s API for each email and logs the findings in a JSON file.

Visualize Results:
Open dashboard.html in your browser to explore charts, detailed breach sources, and safety insights.

🛡️ Notes

  Uses LeakCheck.io public API (no API key required).

  Built-in delay to prevent rate limits (≈1.2s per request).

  Emails are saved in plain text for visualization — handle responsibly.

👨‍💻 Authors

Madhavan Naikar, Yash Chand, Omkar Khanolkar, Sohel Pathan
