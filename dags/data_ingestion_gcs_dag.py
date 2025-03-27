import pandas as pd
from google.cloud import storage, bigquery
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os

# Replace with the path to your downloaded service account key file

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/airflow/opt/airflow/config/crd.json'

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET_NAME = os.environ.get("GCP_GCS_BUCKET")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET")
BIGQUERY_TABLE = os.environ.get("BIGQUERY_TABLE")

# Get the current year, month, and week number
today = datetime.today().strftime('%Y-%m-%d')
week = today.split('-')[2]
month = today.split('-')[1]
year = today.split('-')[0]

# Define constants
TSV_URLS = [
    ("https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/us_national_market_tracker.tsv000.gz", "national_"),
    ("https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/redfin_metro_market_tracker.tsv000.gz", "metro_"),
    ("https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/state_market_tracker.tsv000.gz", "state_"),
    ("https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/county_market_tracker.tsv000.gz", "county_"),
    ("https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/city_market_tracker.tsv000.gz", "city_")
]

#BUCKET_NAME = "prj-redfin-housing-markt-data"
#DESTINATION_BLOB_NAME = f"indata/{year}/{month}/{week}/weekly_housing_market_data.parquet"
#LOCAL_PARQUET_FILE = "/tmp/weekly_housing_market_data.parquet"

#BIGQUERY_PROJECT_ID = "omega-byte-447718-e2"
#BIGQUERY_DATASET = "redfin_housing_market"
#BIGQUERY_TABLE = "monthly_housing_market_data"


def download_and_convert():
    """
    Download the TSV file, convert the first 100 rows to Parquet, and upload to GCS.
    """

    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    #storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    #storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    for url, prefix in TSV_URLS:
        print("Downloading TSV file...")
        #df = pd.read_csv(url, sep="\t", compression='gzip', nrows=100) # For test
        df = pd.read_csv(url, sep="\t", compression='gzip')
        parquet_file = f"/tmp/{prefix}market_tracker.parquet"

        print("Saving as Parquet...")
        df.to_parquet(parquet_file, engine='pyarrow')
        
        destination_blob_name = f"indata/{year}/{month}/{week}/{prefix}market_tracker.parquet"
        blob = bucket.blob(destination_blob_name)

        print("Uploading to GCS...")
        blob.upload_from_filename(parquet_file)
        print(f"File uploaded to gs://{BUCKET_NAME}/{destination_blob_name}")
    

def load_to_bigquery():
    """
    Load the Parquet files from GCS into a BigQuery table.
    """
    client = bigquery.Client(project=PROJECT_ID)
    table_id = f"{PROJECT_ID}.{BIGQUERY_DATASET}"


    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE  # Overwrites existing data
    )

    for _, prefix in TSV_URLS:
        uri = f"gs://{BUCKET_NAME}/indata/{year}/{month}/{week}/{prefix}market_tracker.parquet"
        table_name = f"{table_id}.staging_{prefix}{BIGQUERY_TABLE}"
        print(f"Loading data from {uri} into BigQuery table {table_name}...")
        load_job = client.load_table_from_uri(uri, table_name, job_config=job_config)
        load_job.result()  # Wait for job to complete
        print(f"Data successfully loaded into BigQuery table: {table_name}")

# Define Airflow DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 3, 17),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'copy_tsv_to_gcs_and_bq',
    default_args=default_args,
    description='Download TSV, upload to GCS, and load into BigQuery',
    schedule_interval='0 0 * * 1',  # Runs every Monday at 12 AM
    catchup=False
)

# Define Task 1: Download & Upload to GCS
download_task = PythonOperator(
    task_id='download_and_upload',
    python_callable=download_and_convert,
    dag=dag
)

# Define Task 2: Load into BigQuery
load_task = PythonOperator(
    task_id='load_to_bigquery',
    python_callable=load_to_bigquery,
    dag=dag
)

# Task Dependency: Load into BigQuery only after GCS upload is done
download_task >> load_task
