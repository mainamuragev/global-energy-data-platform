from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import os

RAW_DATA_PATH = "/home/mainavm/global-energy-data-platform/data/raw/energy.csv"
VALIDATED_PATH = "/home/mainavm/global-energy-data-platform/data/validated/energy_validated.csv"

def validate_data():
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"Raw data not found at {RAW_DATA_PATH}")

    df = pd.read_csv(RAW_DATA_PATH)

    # Basic validation checks
    df = df.dropna()                # remove nulls
    df = df.drop_duplicates()       # remove duplicates

    # Example schema enforcement
    required_columns = ["country", "fuel", "price", "consumption"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Save validated data
    os.makedirs(os.path.dirname(VALIDATED_PATH), exist_ok=True)
    df.to_csv(VALIDATED_PATH, index=False)

with DAG(
    dag_id="validate_energy_data",
    start_date=datetime(2026, 5, 4),
    schedule="@daily",
    catchup=False,
) as dag:
    validate_task = PythonOperator(
        task_id="validate_energy",
        python_callable=validate_data
    )
