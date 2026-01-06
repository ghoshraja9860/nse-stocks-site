import csv
import requests
from datetime import datetime

# 1) Configure your Chartink screener slug
SCREENER_SLUG = "rsi-oversold-nifty"  # example; replace with your screener slug
API_URL = f"https://chartink.com/screener/{SCREENER_SLUG}"

# 2) Optional: if your screener needs cookies/headers (private scans), add them here
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
}
COOKIES = {}  # e.g., {"ci_session": "YOUR_SESSION_COOKIE"} if required

# 3) Map Chartink fields to your CSV columns
# Adjust keys based on the JSON fields returned by your screener
def transform_row(row):
    stock = row.get("nsecode") or row.get("symbol") or row.get("name")
    m_rsi = row.get("monthly_rsi") or ""
    w_rsi = row.get("weekly_rsi") or ""
    d_rsi = row.get("rsi") or row.get("daily_rsi") or ""
    pct_daily = row.get("per_chg") or row.get("day_change_pct") or ""
    pct_weekly = row.get("week_change_pct") or ""
    pct_monthly = row.get("month_change_pct") or ""
    pct_3m = row.get("3m_change_pct") or ""
    universe = row.get("index") or ""  # e.g., nifty50/nifty200/nifty500 if available

    return [
        stock, m_rsi, w_rsi, d_rsi,
        pct_daily, pct_weekly, pct_monthly, pct_3m, universe
    ]

def fetch_chartink():
    # For public scans, Chartink returns HTML with embedded JSON; for API endpoints, use their documented path
    # If your scan returns JSON via POST, adapt accordingly.
    resp = requests.get(API_URL, headers=HEADERS, cookies=COOKIES, timeout=30)
    resp.raise_for_status()
    text = resp.text

    # Simple extraction: if your scan exposes JSON via a known endpoint, replace this with that call.
    # Otherwise, parse embedded JSON or switch to a POST endpoint used by Chartink’s API docs.
    # Placeholder: assume you have a JSON endpoint returning {"data": [...]}
    # Example:
    # data_resp = requests.post("https://chartink.com/screener/process", data={"scan_clause": "..."}, headers=HEADERS)
    # rows = data_resp.json().get("data", [])

    # For demonstration, we’ll assume you have rows from a JSON endpoint:
    rows = []  # TODO: replace with actual parsed rows

    return rows

def write_csv(rows, path="stocks.csv"):
    header = ["Stock","MonthlyRSI","WeeklyRSI","DailyRSI","%Daily","%Weekly","%Monthly","%3Month","Universe"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for r in rows:
            writer.writerow(transform_row(r))

def main():
    rows = fetch_chartink()
    if not rows:
        print("No rows fetched—check screener slug or authentication.")
        return
    write_csv(rows)
    print(f"Updated stocks.csv at {datetime.now().isoformat()}")

if __name__ == "__main__":
    main()
