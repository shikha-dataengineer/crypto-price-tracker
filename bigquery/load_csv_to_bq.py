import os
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv("config/.env")

project = os.getenv("GCP_PROJECT")
dataset = os.getenv("BQ_DATASET")
table = os.getenv("BQ_TABLE")
bucket = os.getenv("GCS_BUCKET")
gcs_file = os.getenv("GCS_FILE")

client = bigquery.Client(project=project)
table_id = f"{project}.{dataset}.{table}"
gcs_uri = f"gs://{bucket}/{gcs_file}"

job_config = bigquery.LoadJobConfig(
    autodetect=True,
    skip_leading_rows=1,
    source_format=bigquery.SourceFormat.CSV,
)

load_job = client.load_table_from_uri(gcs_uri, table_id, job_config=job_config)
load_job.result()
print(f"Loaded data from {gcs_uri} into {table_id}")
