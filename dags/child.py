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
    dag_id='child',
    default_args=default_args,
    description='child dag',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
) as dag:
    wait_for_parent_success = ExternalTaskSensor(
        task_id='wait_for_parent_success',
        external_dag_id='parent_success',
        external_task_id='end',
        mode='poke',  # check
        timeout=600,  # 10 minutes
        poke_interval=1,  # check every second
        soft_fail=True,
    )

    child_task = DummyOperator(task_id='child_task')

    wait_for_parent_success >> child_task
