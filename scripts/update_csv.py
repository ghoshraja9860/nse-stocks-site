import requests, csv, os

# Chartink API endpoint
url = "https://chartink.com/screener/process"

# Replace with your screener's scan_clause (copied from Network tab)
payload = {
    "scan_clause": "( {cash} ( latest rsi(14) > 60 ) )"  # example only
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded"
}

# If your screener is private, add your Chartink session cookie here
cookies = {
    "ci_session": os.environ.get("CI_SESSION", "")
}

resp = requests.post(url, data=payload, headers=headers, cookies=cookies)
resp.raise_for_status()
data = resp.json()

rows = data.get("data", [])

with open("stocks.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Stock","MonthlyRSI","WeeklyRSI","DailyRSI","%Daily","%Weekly","%Monthly","%3Month","Universe"])
    for r in rows:
        stock = r.get("nsecode")
        d_rsi = r.get("rsi")
        pct_daily = r.get("per_chg")
        # Chartink usually returns daily RSI and % change; weekly/monthly RSI may need extra clauses
        writer.writerow([stock, "", "", d_rsi, pct_daily, "", "", "", ""])
