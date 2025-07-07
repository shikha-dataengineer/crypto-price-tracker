import subprocess, os
from google.cloud import bigquery
from dotenv import load_dotenv

subprocess.run(["python", "bigquery/load_csv_to_bq.py"])  # Step 1: Load CSV
load_dotenv("config/.env")
client = bigquery.Client(project=os.getenv("GCP_PROJECT"))  # Step 2: Run SQL
query = open("bigquery/transform_query.sql").read()
client.query(query).result()
print("✅ Transformation query executed.")
