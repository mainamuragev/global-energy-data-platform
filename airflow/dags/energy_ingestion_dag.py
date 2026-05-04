from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "maina",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="energy_ingestion_dag",
    default_args=default_args,
    description="Daily ingestion of energy prices into Postgres",
    schedule ="@daily",   # runs once per day
    start_date=datetime(2026, 5, 4),
    catchup=False,
    tags=["energy", "postgres", "api"],
) as dag:

    ingest_task = BashOperator(
        task_id="run_ingestion",
        bash_command="python /home/mainavm/global-energy-data-platform/ingest_energy_data.py"
    )

    ingest_task
