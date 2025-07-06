import subprocess

# Step 1: Load from GCS to BigQuery
subprocess.run(["python", "bigquery/load_csv_to_bq.py"])

# Step 2: Run BQ SQL transform
from google.cloud import bigquery
from dotenv import load_dotenv
import os

load_dotenv("config/.env")

client = bigquery.Client(project=os.getenv("GCP_PROJECT"))

with open("bigquery/transform_query.sql", "r") as f:
    query = f.read()

query_job = client.query(query)
query_job.result()
print("Transformation query executed.")
