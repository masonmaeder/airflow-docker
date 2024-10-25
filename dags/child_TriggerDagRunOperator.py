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
    dag_id='child_TriggerDagRunOperator',
    default_args=default_args,
    description='Child DAG triggered by parent on success',
    schedule_interval=None,  # Not scheduled, triggered by parent
    start_date=days_ago(1),
    catchup=False,
) as dag:
    # DummyOperator always success
    start = DummyOperator(task_id='start')

    # Dependencies here...

    end = DummyOperator(task_id='end')

    start >> end
