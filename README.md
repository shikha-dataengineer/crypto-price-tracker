# Cryptocurrency Price Analysis Pipeline on Google Cloud

## Overview
This project implements an automated ETL pipeline to load, clean, and visualize historical daily cryptocurrency price data using Google Cloud Platform (GCP) tools like **Cloud Storage**, **BigQuery**, and **Looker Studio**.

## Who this is for
This project is a lightweight template for anyone who wants to load historical crypto OHLC data into Google Cloud (BigQuery) and build a clean, queryable, partitioned dataset with a Looker Studio dashboard on top. Useful for analysts, students, or data engineers prototyping GCP-based financial data pipelines.

## Problem
Analyzing large volumes of crypto market data manually is slow and inefficient.

## Dataset Overview
The dataset contains historical OHLC (Open, High, Low, Close) price data for over 50 cryptocurrencies from **May 2013 to October 2022** on a daily basis. Prices are represented in USD. The data is stored in CSV format for fast and efficient loading.

You can find the original dataset on Kaggle here:  
[Crypto Price Prediction Dataset by shashwat1001](https://www.kaggle.com/code/shashwat1001/crypto-price-prediction)

## Data Description

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

## Project Overview
1. Source: Historical crypto price data from Kaggle
2. Objective: Build a clean, analytics-ready dataset for crypto market trends
3. Tools used:
  - Google Cloud Storage (GCS)
  - BigQuery (SQL transforms & storage)
  - Python (ETL orchestration)
  - Looker Studio (Visualization)

## ETL Pipeline Overview

### 1. **Data Ingestion**
- CSV uploaded to Google Cloud Storage
- Loaded into a BigQuery table

### 2. **Data Transformation**
- Applied SQL cleaning via `bigquery/transform_query.sql`:
  - Parsed `timestamp` into `date` and `time`
  - Checked `NULL` rows if any
  - Deduplicated by `crypto_name + date`
  - Created a clean, partitioned final table for querying

### 3. **Visualized results in Looker Studio**
   - Connected to the cleaned BigQuery table
   - Created charts:
     - 📈 Line chart of `close` price over time
     - 📊 Bar chart of `volume` by `crypto_name`
     - 💰 Line chart of Market Cap trend
     - 🥧 Pie chart Market share by Market cap
     - ✨ Scatter Plot for Volume vs Market cap

### 4. **ETL Automation**
- Script: [`etl_pipeline.py`](etl_pipeline.py)
- Automated tests: [`tests/test_pipeline.py`](tests/test_pipeline.py)
- Continuous integration via GitHub Actions runs the test suite automatically on every change.

## Result
A reusable, scalable, tested pipeline for financial data analytics using GCP.

## Setup

1. Clone this repo
2. Copy  `config/.env` and fill in your own GCP project details
3. Install dependencies: `pip install -r requirements.txt`
4. Replace `YOUR_PROJECT_ID` in `bigquery/transform_query.sql` with your own GCP project ID
5. Run the pipeline: `python etl_pipeline.py`
6. Run the tests: `pytest tests/`

## License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
