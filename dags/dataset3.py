from airflow import DAG, Dataset  # type: ignore
from airflow.operators.python import PythonOperator  # type: ignore
from airflow.sensors.sql import SqlSensor  # type: ignore
from datetime import datetime
import psycopg2  # type: ignore

# Database connection parameters
DB_NAME = 'airflow'
DB_USER = 'airflow'
DB_PASSWORD = 'airflow'
DB_HOST = 'airflow-docker-postgres-1'
DB_PORT = '5432'

# Dataset definition (must match the name used in dataset1.py)
DATASET_NAME = "my_dataset"
# dataset = Dataset(f"dataset.json")  # Optional, for local reference


def print_latest_string():
    """Prints the latest string from the dataset in PostgreSQL."""
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    # Query to get the latest string added to the dataset
    cursor.execute(
        f"SELECT data FROM {DATASET_NAME} ORDER BY created_at DESC LIMIT 1;")
    latest_string = cursor.fetchone()

    if latest_string:
        print(f"Latest string from dataset: {latest_string[0]}")
    else:
        print("No data found in the dataset.")

    cursor.close()
    conn.close()


with DAG(
    dag_id="dataset3",
    start_date=datetime(2023, 10, 26),
    schedule=[Dataset("my_dataset")],
    catchup=False,
) as dag:

    # Task to print the latest string
    print_string_task = PythonOperator(
        task_id="print_latest_string",
        python_callable=print_latest_string,
    )
