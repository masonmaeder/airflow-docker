from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.exceptions import AirflowFailException

# This function forces a failure


def force_failure():
    raise AirflowFailException("This DAG is designed to always fail.")


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 0,
}

with DAG(
    dag_id='parent_failure',
    default_args=default_args,
    description='A parent DAG that always fails.',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
) as dag:

    fail_task = PythonOperator(
        task_id='fail_task',
        python_callable=force_failure
    )

    fail_task
