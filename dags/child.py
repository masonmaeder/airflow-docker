from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 0,
}

with DAG(
    dag_id='child',
    default_args=default_args,
    description='A child DAG that runs only when the successful parent DAG completes.',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
) as dag:

    wait_for_parent = ExternalTaskSensor(
        task_id='wait_for_parent',
        external_dag_id='parent_success',  # ID of the successful parent DAG
        external_task_id='end',  # Waits for the 'end' task of the parent DAG
        mode='poke',  # Continuously checks for completion
        timeout=600,  # Fails if not completed in 10 minutes
        poke_interval=30,  # Checks every 30 seconds
        soft_fail=False,  # Fails if the parent DAG doesn't succeed
    )

    child_task = DummyOperator(task_id='child_task')

    wait_for_parent >> child_task
