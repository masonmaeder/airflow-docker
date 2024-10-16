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
    description='A child DAG that runs only when the parent DAG succeeds.',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
) as dag:

    # Sensor to wait for the parent DAG to succeed
    wait_for_parent_success = ExternalTaskSensor(
        task_id='wait_for_parent_success',
        external_dag_id='parent_success',  # The ID of the successful parent DAG
        external_task_id='end',  # The final task in the parent DAG
        mode='poke',  # Keep checking periodically
        timeout=600,  # Fail if not complete in 10 minutes
        poke_interval=30,  # Check every 30 seconds
        soft_fail=False,  # Hard fail if parent task does not succeed
    )

    # Dummy task to indicate successful execution of the child DAG
    child_task = DummyOperator(task_id='child_task')

    # Set dependencies
    wait_for_parent_success >> child_task
