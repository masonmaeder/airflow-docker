from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 0,
}

with DAG(
    dag_id='parent_success',
    default_args=default_args,
    description='parent always succeeds',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
) as dag:

    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    start >> end
