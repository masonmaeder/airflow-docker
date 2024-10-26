from airflow import DAG  # type: ignore
from airflow.operators.dummy import DummyOperator  # type: ignore
from airflow.operators.python import PythonOperator  # type: ignore
from airflow.sensors.external_task import ExternalTaskSensor  # type: ignore
from airflow.utils.dates import days_ago  # type: ignore
import time
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 0,
}


def sleep_for_10_seconds():
    """Sleep for 10 seconds before finishing."""
    time.sleep(10)


def check_minute():
    current_minute = datetime.now().minute
    if current_minute % 2 == 0:
        return 'success'
    else:
        raise ValueError('Failing this run')


with DAG(
    dag_id='parent_ExternalTaskSensor',
    default_args=default_args,
    description='Parent DAG child waits for',
    schedule_interval='* * * * *',  # Every minute
    # Child (sensor) task must be running before the parent DAG completes in order to trigger.
    # Both DAGs must be scheduled (not manually triggered) for the sensor to work.
    # Consider scheduling the child DAG prior to the parent if parent tasks are not long-running.
    start_date=days_ago(1),
    catchup=False,
) as dag:
    # DummyOperator always success
    start = DummyOperator(task_id='start')

    # Pass if the current minute is even (fail every other run)
    # This is to demonstrate the ExternalTaskSensor only continues on success; change this to your predecessor task(s)
    check_minute_task = PythonOperator(
        task_id='check_minute',
        python_callable=check_minute,
    )

    # 10-second delay. Simulates a task that takes time to process, allowing more time for child DAG to initialize
    end = PythonOperator(
        task_id='end',
        python_callable=sleep_for_10_seconds,
    )

    start >> check_minute_task >> end
