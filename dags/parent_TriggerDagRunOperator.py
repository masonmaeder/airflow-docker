from airflow import DAG  # type: ignore
from airflow.operators.dummy import DummyOperator  # type: ignore
from airflow.operators.trigger_dagrun import TriggerDagRunOperator  # type: ignore
from airflow.operators.python import PythonOperator  # type: ignore
from airflow.utils.dates import days_ago  # type: ignore
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 0,
}


def check_minute():
    current_minute = datetime.now().minute
    if current_minute % 2 == 0:
        return 'success'
    else:
        raise ValueError('Failing this run')


with DAG(
    dag_id='parent_TriggerDagRunOperator',
    default_args=default_args,
    description='Parent DAG that triggers child DAG on success',
    schedule_interval='* * * * *',  # Every minute
    start_date=days_ago(1),
    catchup=False,
) as dag:
    start = DummyOperator(task_id='start')

    # Pass if the current minute is even (fail every other run)
    # This is to demonstrate the TriggerDagRunOperator only triggers on success; change this to your predecessor task(s)
    check_minute_task = PythonOperator(
        task_id='check_minute',
        python_callable=check_minute,
    )

    end = DummyOperator(task_id='end')

    trigger_child = TriggerDagRunOperator(
        task_id='trigger_child',
        # Ensure this matches the child (dependency) DAG ID
        trigger_dag_id='child_TriggerDagRunOperator',
        # Set to True if the parent task needs to wait to pass for the child DAG to complete
        wait_for_completion=False,
    )

    start >> check_minute_task >> end >> trigger_child
