import requests
import csv
import os
from datetime import datetime

# Chartink API endpoint
url = "https://chartink.com/screener/process"

# Replace this with your screener's actual scan_clause.
# You can copy it from the "Scan Criteria" section when you open or clone your screener.
payload = {
    "scan_clause": "( {cash} ( latest rsi(14) > 60 ) )"  # <-- replace with your RSI Strategy Agni criteria
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded"
}

# If your screener is private, add your Chartink session cookie as a GitHub secret
cookies = {
    "ci_session": os.environ.get("CI_SESSION", "")
}

def fetch_chartink():
    resp = requests.post(url, data=payload, headers=headers, cookies=cookies, timeout=30)
    resp.raise_for_status()
    return resp.json().get("data", [])

def write_csv(rows, path="stocks.csv"):
    header = ["Stock","MonthlyRSI","WeeklyRSI","DailyRSI","%Daily","%Weekly","%Monthly","%3Month","Universe"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for r in rows:
            stock = r.get("nsecode")
            d_rsi = r.get("rsi")
            pct_daily = r.get("per_chg")
            # Chartink usually returns daily RSI and % change.
            # Weekly/Monthly RSI and % changes require extra clauses in your screener.
            writer.writerow([stock, "", "", d_rsi, pct_daily, "", "", "", ""])

def main():
    rows = fetch_chartink()
    if not rows:
        print("No data returned — check your scan_clause or cookies.")
        return
    write_csv(rows)
    print(f"Updated stocks.csv at {datetime.now().isoformat()}")

if __name__ == "__main__":
    main()
