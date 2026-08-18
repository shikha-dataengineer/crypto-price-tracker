# Cryptocurrency Price Analysis & Live Tracking Pipeline on Google Cloud

## Overview
This project combines two things: an automated ETL pipeline that loads, cleans, and visualizes historical daily cryptocurrency price data using Google Cloud Platform (GCP) tools like Cloud Storage, BigQuery, and Looker Studio - and a live price tracker that fetches current crypto prices every hour and logs them to this repository.

## Who this is for
This project is a lightweight template for anyone who wants to (a) load historical crypto OHLC data into Google Cloud (BigQuery) and build a clean, queryable, partitioned dataset with a Looker Studio dashboard on top, and (b) maintain a simple, free, ongoing log of live crypto prices without needing any cloud billing. Useful for analysts, students, or data engineers prototyping financial data pipelines.

## Problem
Analyzing large volumes of crypto market data manually is slow and inefficient, and most lightweight tracking tools require paid infrastructure just to log prices over time.

## Part 1: Historical Data Pipeline (GCP / BigQuery)

### Dataset Overview
Contains historical OHLC (Open, High, Low, Close) price data for over 50 cryptocurrencies from **May 2013 to October 2022** on a daily basis, in USD.

Original dataset on Kaggle: [Crypto Price Prediction Dataset by shashwat1001](https://www.kaggle.com/code/shashwat1001/crypto-price-prediction)

### Data Description

| Column       | Description                                                                                  |
|--------------|----------------------------------------------------------------------------------------------|
| `open`       | Opening price on the date (UTC time)                                                        |
| `high`       | Highest price reached on the date (UTC time)                                                |
| `low`        | Lowest price reached on the date (UTC time)                                                 |
| `close`      | Closing price on the date (UTC time)                                                        |
| `volume`     | Quantity of asset bought or sold, in base currency                                          |
| `marketCap`  | Total market value of all coins mined (coins in circulation × current coin price)           |
| `timestamp`  | UTC timestamp representing the day                                                          |
| `crypto_name`| Name of the cryptocurrency                                                                  |
| `date`       | Date derived from the timestamp                                                             |

### Tools used
- Google Cloud Storage (GCS)
- BigQuery (SQL transforms & storage)
- Python (ETL orchestration)
- Looker Studio (Visualization)

### ETL Pipeline Steps
1. **Data Ingestion** — CSV uploaded to Cloud Storage, loaded into a BigQuery table
2. **Data Transformation** — cleaned via `bigquery/transform_query.sql`: parses `timestamp` into `date`/`time`, checks for `NULL` rows, deduplicates by `crypto_name + date`, and produces a clean, partitioned final table
3. **Visualization in Looker Studio** — connected to the cleaned table with charts:
   - 📈 Line chart of `close` price over time
   - 📊 Bar chart of `volume` by `crypto_name`
   - 💰 Line chart of Market Cap trend
   - 🥧 Pie chart of market share by Market Cap
   - ✨ Scatter plot of Volume vs Market Cap

## Part 2: Live Price Tracker (no cloud billing required)

- Script: [`live_fetch.py`](live_fetch.py) pulls current prices, market cap, and 24h volume for Bitcoin, Ethereum, Dogecoin, Cardano, and Solana from the free [CoinGecko API](https://www.coingecko.com/en/api).
- A scheduled GitHub Actions workflow ([`.github/workflows/live-tracker.yml`](.github/workflows/live-tracker.yml)) runs this script automatically **every hour** and commits the results.
- Results accumulate in [`data/live_prices.csv`](data/live_prices.csv), building a genuine time-stamped price history entirely for free — no GCP billing needed for this part.

## Automation & Testing
- Automated tests: [`tests/test_pipeline.py`](tests/test_pipeline.py)
- Continuous integration via GitHub Actions runs the test suite automatically on every change ([`.github/workflows/tests.yml`](.github/workflows/tests.yml))
- The live tracker itself runs as a second, independent scheduled workflow

## Result
A reusable, tested pipeline combining historical financial data analytics on GCP with a free, ongoing live price log with no paid infrastructure required for the live component.

## Setup

### Historical pipeline (requires a GCP project)
1. Clone this repo
2. Copy `config/.env` and fill in your own GCP project details
3. Install dependencies: `pip install -r requirements.txt`
4. Replace `YOUR_PROJECT_ID` in `bigquery/transform_query.sql` with your own GCP project ID
5. Run the pipeline: `python etl_pipeline.py`
6. Run the tests: `pytest tests/`

### Live tracker (no GCP account needed)
1. Fork or clone this repo
2. The `live-tracker.yml` GitHub Actions workflow runs automatically on a schedule once enabled on your repo — no setup beyond that
3. To run it manually or test locally: `pip install requests` then `python live_fetch.py`

## License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
