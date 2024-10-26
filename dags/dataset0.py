from airflow import DAG  # type: ignore
from airflow.providers.postgres.operators.postgres import PostgresOperator  # type: ignore
from datetime import datetime

with DAG(
    dag_id='dataset0',
    start_date=datetime(2023, 10, 26),
    schedule_interval='@daily',
    catchup=False,
) as dag:

    query_task = PostgresOperator(
        task_id='query_postgres',
        postgres_conn_id='my_postgres',  # Connection ID created earlier
        sql='SELECT * FROM dag;',  # SQL query to execute
    )