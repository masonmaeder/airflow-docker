from airflow import DAG  # type: ignore
from airflow.operators.dummy import DummyOperator  # type: ignore
from airflow.sensors.external_task import ExternalTaskSensor  # type: ignore
from airflow.utils.dates import days_ago  # type: ignore

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 0,
}

with DAG(
    dag_id='parent_ExternalTaskSensor',
    default_args=default_args,
    description='Parent DAG child waits for',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
) as dag:
    # DummyOperator always success
    start = DummyOperator(task_id='start')

    # Parent (preceding) task(s) to wait for here...

    end = DummyOperator(task_id='end')

    start >> end
