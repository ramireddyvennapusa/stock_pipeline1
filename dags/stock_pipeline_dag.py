from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

from include.fetch_stock_data import run_fetch_and_load   # FIXED

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="stock_pipeline_googl",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval="0 * * * *",
    catchup=False,
    tags=["assignment", "stocks"],
) as dag:

    fetch_task = PythonOperator(
        task_id="fetch_stock",
        python_callable=run_fetch_and_load,
    )

