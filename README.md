# Real-Time Cryptocurrency Price Tracker ETL Pipeline

## Overview
This project ingests historical cryptocurrency price data into BigQuery for real-time analytics and forecasting.

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


## Progress So Far
1. Dataset sourced from Kaggle  
2. GCS bucket created and dataset uploaded via Cloud Shell  
3. BigQuery dataset (`crypto_analytics`) created  

## Next Steps (Automated)
- Loaded CSV data from GCS into BigQuery  
- Run SQL transformations for data cleaning and enrichment  
- Visualize results in Looker Studio 

## How to Run
Run the ETL pipeline with:

```bash
python etl/etl_pipeline.py
