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
Open dashboard.html in your browser to explore charts, detailed breach sources.
<img width="1600" height="743" alt="image" src="https://github.com/user-attachments/assets/09f31d34-56e3-4fc6-858d-655bce5402a0" />
<img width="1600" height="755" alt="image" src="https://github.com/user-attachments/assets/dfa48848-eff9-40f9-8d4d-11fbc7bca217" />
<img width="1600" height="652" alt="image" src="https://github.com/user-attachments/assets/a70490eb-b1ee-4711-bc7c-f43bdf19081f" />



🛡️ Notes

  Uses LeakCheck.io public API (no API key required).

  Built-in delay to prevent rate limits (≈1.2s per request).

  Emails are saved in plain text for visualization — handle responsibly.

👨‍💻 Authors

Madhavan Naikar, Yash Chand, Omkar Khanolkar, Sohel Pathan
