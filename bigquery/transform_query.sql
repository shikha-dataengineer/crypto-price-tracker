-- Validation check Performed

-- A) NULL CHECKS
SELECT
  COUNTIF(crypto_name IS NULL) AS crypto_name_nulls,
  COUNTIF(timestamp IS NULL) AS timestamp_nulls,
  COUNTIF(open IS NULL) AS open_nulls,
  COUNTIF(high IS NULL) AS high_nulls,
  COUNTIF(low IS NULL) AS low_nulls,
  COUNTIF(close IS NULL) AS close_nulls,
  COUNTIF(volume IS NULL) AS volume_nulls,
  COUNTIF(marketCap IS NULL) AS marketCap_nulls
FROM `crypto-price-data-55010.crypto_analytics.crypto_prices`
WHERE _PARTITIONTIME BETWEEN TIMESTAMP("2013-01-01") AND TIMESTAMP("2022-12-31");



--B) Data Cleaning and deduplication query

CREATE OR REPLACE TABLE `crypto-price-data-55010.crypto_analytics.cleaned_crypto_prices` AS
WITH ranked_data AS (
  SELECT
    crypto_name,
    timestamp,
    date,
    open,
    high,
    low,
    close,
    volume,
    marketCap,
    _PARTITIONTIME,
    ROW_NUMBER() OVER (PARTITION BY crypto_name, timestamp ORDER BY _PARTITIONTIME DESC) AS rn
  FROM `crypto-price-data-55010.crypto_analytics.crypto_prices`
  WHERE TIMESTAMP_TRUNC(_PARTITIONTIME, DAY) = TIMESTAMP("2025-07-02")
),
validated_data AS (
  SELECT
    crypto_name,
    TIMESTAMP(timestamp) AS trade_time,
    DATE(timestamp) AS trade_date,
    SAFE_CAST(open AS FLOAT64) AS open_price,
    SAFE_CAST(high AS FLOAT64) AS high_price,
    SAFE_CAST(low AS FLOAT64) AS low_price,
    SAFE_CAST(close AS FLOAT64) AS close_price,
    SAFE_CAST(volume AS FLOAT64) AS trade_volume,
    SAFE_CAST(marketCap AS FLOAT64) AS market_cap
  FROM ranked_data
  WHERE rn = 1  -- keep only the latest duplicate
    AND close IS NOT NULL
    AND open IS NOT NULL
    AND volume >= 0
    AND marketCap >= 0
    AND high >= low
    AND open >= 0
    AND close >= 0
    AND low <= open
    AND open <= high
    AND low <= close
    AND close <= high
    AND volume BETWEEN 0 AND 1e12
    AND marketCap BETWEEN 0 AND 1e14
    AND crypto_name IS NOT NULL
    AND crypto_name != ''
    AND TIMESTAMP(timestamp) <= CURRENT_TIMESTAMP()
    AND DATE(timestamp) = date
)
SELECT * FROM validated_data;
