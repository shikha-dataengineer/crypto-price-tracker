---
title: 'crypto-price-tracker: A lightweight, free pipeline for historical and live cryptocurrency price data on Google Cloud'
tags:
  - Python
  - cryptocurrency
  - data engineering
  - ETL
  - Google Cloud Platform
  - BigQuery
authors:
  - name: Shikha Agrawal
    affiliation: 1
affiliations:
  - name: Independent Researcher
    index: 1
date: 18 August 2026
bibliography: paper.bib
---

# Summary

`crypto-price-tracker` is an open-source Python tool for working with
cryptocurrency price data at two different time scales. A historical ETL
pipeline loads daily OHLC (open, high, low, close) price records for over
50 cryptocurrencies, spanning May 2013 to October 2022, into Google
BigQuery, validates and deduplicates the data, and exposes it for
querying and dashboarding in Looker Studio. A separate live tracker
fetches current price, market capitalization, and 24-hour trading volume
from the public CoinGecko API on an hourly schedule and appends each
observation to a version-controlled CSV file. Both components are
automated and tested, and the live tracker is deliberately designed to
run on entirely free infrastructure, using GitHub Actions' scheduled
workflows rather than a hosted database.

# Statement of need

This project started from a personal interest in tracking cryptocurrency
markets, and grew into a small but complete example of a common data
engineering pattern: taking a static historical dataset, loading and
validating it in a cloud data warehouse, and pairing it with an ongoing,
low-cost live data feed. Many existing crypto tracking examples either
stop at a one-off notebook analysis of historical data, or assume paid
hosting for anything live. `crypto-price-tracker` keeps both parts
genuinely free and reproducible: the historical pipeline runs on Google
Cloud's free-tier BigQuery sandbox, and the live tracker avoids cloud
billing entirely by persisting its output as a file inside the
repository itself, updated automatically via a scheduled GitHub Actions
workflow. This makes the project useful as a practical, minimal template
for students and analysts who want to learn or prototype a real ETL and
live-data workflow without needing to set up paid infrastructure first.

# Functionality

The historical pipeline (`etl_pipeline.py`) loads a CSV of historical
price records into Google Cloud Storage and BigQuery, then applies a SQL
transformation (`bigquery/transform_query.sql`) that checks for null
values, removes duplicate `(crypto_name, date)` pairs, and validates that
`low <= open, close <= high` for every row, writing the result to a
clean, partitioned table. One practical detail worth noting: BigQuery's
free "sandbox" mode (used when no billing account is attached to a
project) requires datasets to have a default table and partition
expiration set, and does not permit some table-creation operations at
all regardless of table-level settings — a constraint this project works
around by keeping the live component entirely outside of BigQuery. The
live tracker (`live_fetch.py`) queries the CoinGecko public API for a
configurable list of coins and appends the results, timestamped in UTC,
to `data/live_prices.csv`. Both components are covered by an automated
test suite (`tests/test_pipeline.py`) that validates the data-quality
rules independently of any live cloud connection, and both run
automatically via GitHub Actions: one workflow runs the test suite on
every change, and a second runs the live tracker every hour and commits
its output.

# Acknowledgements

The historical dataset used in this project is derived from the publicly
available Kaggle dataset by Shashwat (2022). Live price data is provided
by the CoinGecko API.

# References
