from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from pymongo import MongoClient

def store_data():
    client = MongoClient("your_atlas_connection_string")
    db = client["EnergyDB"]
    collection = db["CleanEnergy"]
    df = pd.read_csv("/home/mainavm/global-energy-data-platform/data/clean/energy_clean.csv")
    collection.insert_many(df.to_dict("records"))

with DAG(
    dag_id="store_energy_data",
    start_date=datetime(2026, 5, 4),
    schedule="@daily",
    catchup=False,
) as dag:
    store_task = PythonOperator(
        task_id="store_energy",
        python_callable=store_data
    )
