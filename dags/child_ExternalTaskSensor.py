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
    dag_id='child_ExternalTaskSensor',
    default_args=default_args,
    description='Child DAG triggered by parent on success',
    schedule_interval='* * * * *',  # Every minute
    start_date=days_ago(1),
    catchup=False,
) as dag:
    start = DummyOperator(task_id='start')

    wait_for_parent_success = ExternalTaskSensor(
        task_id='wait_for_parent_success',
        external_dag_id='parent_ExternalTaskSensor',
        external_task_id='end',  # Must provide task within parent DAG to wait for
        # Use poke to keep checking (uses worker slot while running) or reschedule to wait for the next interval (better efficiency)
        # https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/sensors.html
        mode='poke',
        timeout=60,  # 1 minute timeout
        poke_interval=5,  # Check every 5 seconds
        soft_fail=False,
    )

    end = DummyOperator(task_id='end')

    start >> wait_for_parent_success >> end
