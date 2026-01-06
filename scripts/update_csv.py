import requests
import csv
from datetime import datetime

# Direct download link for your screener
# Use the same link you get when you tap "Download CSV" on the screener page
url = "https://chartink.com/screener/rsi-strategy-agni/download"

def fetch_chartink():
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.content.decode("utf-8").splitlines()

def write_csv(lines, path="stocks.csv"):
    reader = csv.reader(lines)
    rows = list(reader)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)

def main():
    lines = fetch_chartink()
    write_csv(lines)
    print(f"Updated stocks.csv at {datetime.now().isoformat()}")

if __name__ == "__main__":
    main()
