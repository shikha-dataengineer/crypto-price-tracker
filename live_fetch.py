"""
Fetches live cryptocurrency prices from the free CoinGecko API
and appends them as new rows to data/live_prices.csv, giving this
project a genuinely real-time component alongside the historical
BigQuery dataset. No cloud billing required — this just writes
to a file inside the repo itself.
"""

import csv
import os
import requests
from datetime import datetime, timezone

COINS = ["bitcoin", "ethereum", "dogecoin", "cardano", "solana"]
OUTPUT_FILE = "data/live_prices.csv"

def fetch_live_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(COINS),
        "vs_currencies": "usd",
        "include_market_cap": "true",
        "include_24hr_vol": "true",
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def build_rows(data):
    now = datetime.now(timezone.utc).isoformat()
    rows = []
    for coin, values in data.items():
        rows.append({
            "crypto_name": coin,
            "price_usd": values.get("usd"),
            "market_cap": values.get("usd_market_cap"),
            "volume_24h": values.get("usd_24h_vol"),
            "fetched_at": now,
        })
    return rows

def append_to_csv(rows):
    os.makedirs("data", exist_ok=True)
    file_exists = os.path.isfile(OUTPUT_FILE)
    with open(OUTPUT_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["crypto_name", "price_usd", "market_cap", "volume_24h", "fetched_at"])
        if not file_exists:
            writer.writeheader()
        writer.writerows(rows)

def main():
    data = fetch_live_prices()
    rows = build_rows(data)
    append_to_csv(rows)
    print(f"Appended {len(rows)} live price rows to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
