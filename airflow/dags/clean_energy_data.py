from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd

def clean_data():
    df = pd.read_csv("/home/mainavm/global-energy-data-platform/data/raw/energy.csv")
    df = df.dropna().drop_duplicates()
    df.to_csv("/home/mainavm/global-energy-data-platform/data/clean/energy_clean.csv", index=False)

with DAG(
    dag_id="clean_energy_data",
    start_date=datetime(2026, 5, 4),
    schedule="@daily",
    catchup=False,
) as dag:
    clean_task = PythonOperator(
        task_id="clean_energy",
        python_callable=clean_data
    )
