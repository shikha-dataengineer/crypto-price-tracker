"""
Fetches live cryptocurrency prices from the free CoinGecko API
and appends them to a BigQuery table, so this project has a
genuinely real-time component alongside the historical dataset.
"""

import os
import requests
from datetime import datetime, timezone, timedelta
from google.cloud import bigquery

COINS = ["bitcoin", "ethereum", "dogecoin", "cardano", "solana"]

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

def ensure_table(client, table_id):
    schema = [
        bigquery.SchemaField("crypto_name", "STRING"),
        bigquery.SchemaField("price_usd", "FLOAT"),
        bigquery.SchemaField("market_cap", "FLOAT"),
        bigquery.SchemaField("volume_24h", "FLOAT"),
        bigquery.SchemaField("fetched_at", "TIMESTAMP"),
    ]
    table = bigquery.Table(table_id, schema=schema)
    # Sandbox-mode (free, no billing) projects require tables to have
    # an expiration date. 59 days keeps it safely under the 60-day limit.
    table.expires = datetime.now(timezone.utc) + timedelta(days=59)
    client.create_table(table, exists_ok=True)

def main():
    project = os.getenv("GCP_PROJECT")
    dataset = os.getenv("BQ_DATASET", "crypto_analytics")
    table_id = f"{project}.{dataset}.live_crypto_prices"

    client = bigquery.Client(project=project)
    ensure_table(client, table_id)

    data = fetch_live_prices()
    rows = build_rows(data)

    errors = client.insert_rows_json(table_id, rows)
    if errors:
        raise RuntimeError(f"Failed to insert rows: {errors}")
    print(f"Inserted {len(rows)} live price rows into {table_id}")

if __name__ == "__main__":
    main()
