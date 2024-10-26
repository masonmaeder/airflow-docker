from airflow import DAG, Dataset  # type: ignore
from airflow.operators.python import PythonOperator  # type: ignore
from datetime import datetime
import psycopg2  # type: ignore
import json
import os

# Database connection parameters (change to actual credentials)
DB_NAME = 'airflow'
DB_USER = 'airflow'
DB_PASSWORD = 'airflow'
DB_HOST = 'airflow-docker-postgres-1'
DB_PORT = '5432'

# Dataset definition
DATASET_NAME = "my_dataset"
dataset = Dataset(DATASET_NAME)


def create_dataset_if_not_exists():
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    # Create a table for the dataset if it doesn't exist
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {DATASET_NAME} (
            id SERIAL PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()


with DAG(
    dag_id="dataset1",
    start_date=datetime(2023, 10, 26),
    schedule_interval="@once",  # Run once to create the dataset
    catchup=False,
) as dag:

    create_dataset_task = PythonOperator(
        task_id="create_dataset_if_not_exists",
        python_callable=create_dataset_if_not_exists,
    )

    create_dataset_task
