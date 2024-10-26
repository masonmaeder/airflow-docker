from airflow import DAG, Dataset  # type: ignore
from airflow.operators.python import PythonOperator  # type: ignore
from datetime import datetime
import psycopg2  # type: ignore
import random
import string

# Database connection parameters
DB_NAME = 'airflow'
DB_USER = 'airflow'
DB_PASSWORD = 'airflow'
DB_HOST = 'airflow-docker-postgres-1'
DB_PORT = '5432'

# Dataset definition (must match the name used in dataset1.py)
DATASET_NAME = "my_dataset"
dataset = Dataset(f"dataset.json")  # Optional, for local reference


def generate_random_string():
    """Generates a random string of fixed length."""
    length = 10  # Length of the random string
    random_string = ''.join(random.choices(
        string.ascii_letters + string.digits, k=length))
    return random_string


def update_dataset(random_string):
    """Updates the PostgreSQL dataset with the generated string."""
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    # Insert the random string into the dataset table
    cursor.execute(
        f"INSERT INTO {DATASET_NAME} (data) VALUES (%s);", (random_string,))
    conn.commit()

    cursor.close()
    conn.close()


with DAG(
    dag_id="dataset2",
    start_date=datetime(2023, 10, 26),
    schedule_interval="@once",  # Run once when triggered
    catchup=False,
) as dag:

    generate_string_task = PythonOperator(
        task_id="generate_random_string",
        python_callable=generate_random_string,
        do_xcom_push=True  # Enable XCom to pass the random string to the next task
    )

    update_dataset_task = PythonOperator(
        task_id="update_dataset",
        python_callable=update_dataset,
        op_kwargs={
            "random_string": "{{ task_instance.xcom_pull(task_ids='generate_random_string') }}"},
    )

    generate_string_task >> update_dataset_task  # Set task dependencies
