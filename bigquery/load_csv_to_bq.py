import os
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv("config/.env")

client = bigquery.Client(project=os.getenv("GCP_PROJECT"))
table_id = f"{os.getenv('GCP_PROJECT')}.{os.getenv('BQ_DATASET')}.{os.getenv('BQ_TABLE')}"
gcs_uri = f"gs://{os.getenv('GCS_BUCKET')}/{os.getenv('GCS_FILE')}"

job_config = bigquery.LoadJobConfig(
    autodetect=True, skip_leading_rows=1, source_format=bigquery.SourceFormat.CSV
)
client.load_table_from_uri(gcs_uri, table_id, job_config=job_config).result()
print(f" Loaded data from {gcs_uri} into {table_id}")

