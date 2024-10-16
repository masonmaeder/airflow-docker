from airflow import DAG  # type: ignore
from airflow.operators.dummy import DummyOperator  # type: ignore
from airflow.operators.python import PythonOperator  # type: ignore
from airflow.utils.dates import days_ago  # type: ignore


def fail_task():
    raise Exception("intentional failure")


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 0,
}

with DAG(
    dag_id='parent_fail',
    default_args=default_args,
    description='parent fails',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
) as dag:
    start = DummyOperator(task_id='start')
    fail = PythonOperator(task_id='fail', python_callable=fail_task)

    start >> fail
