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
    description='Child DAG triggered by parent_success',
    schedule_interval=None,  # Not scheduled, triggered by parent
    start_date=days_ago(1),  # Ensure this aligns with parent DAG start_date
    catchup=False,
) as dag:
    wait_for_parent_success = ExternalTaskSensor(
        task_id='wait_for_parent_success',
        external_dag_id='parent_success',  # Ensure parent DAG ID matches exactly
        external_task_id='end',  # Ensure parent task ID matches
        mode='poke',
        timeout=60,  # 1 minute timeout
        poke_interval=30,  # Check every 30 seconds
        soft_fail=False,  # Set to False to ensure it triggers only on success
    )

    child_task = DummyOperator(task_id='child_task')

    wait_for_parent_success >> child_task
