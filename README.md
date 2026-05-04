```markdown
# Global Energy Data Platform

## Overview
Global Energy Data Platform is an Airflow‑orchestrated pipeline that ingests live energy price data from APIs, validates and cleans records, and stores them in Postgres. It enables reproducible workflows, daily updates, and prepares the foundation for future machine learning and analytics.

## Current DAGs
- **energy_ingestion_dag**  
  Fetches live energy prices from EnergypriceAPI, inserts into Postgres, and saves a raw CSV (`data/raw/energy.csv`).
- **validate_energy_data**  
  Cleans raw data (drops nulls, removes duplicates, enforces schema) and outputs validated CSV (`data/validated/energy_validated.csv`).
- **store_energy_data**  
  Loads validated records into Postgres (`energy_validated` table).

## Project Structure
```
global-energy-data-platform/
├── airflow/
│   └── dags/
│       ├── energy_ingestion_dag.py
│       ├── validate_energy_data.py
│       └── store_energy_data.py
├── data/
│   ├── raw/
│   └── validated/
├── ingest_energy_data.py
├── requirements.txt
├── pyproject.toml
├── uv.lock
└── README.md
```

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/mainamuragev/global-energy-data-platform.git
   cd global-energy-data-platform
   ```
2. Create a `.env` file with your Postgres and API credentials:
   ```
   PGHOST=...
   PGPORT=...
   PGDATABASE=...
   PGUSER=...
   PGPASSWORD=...
   PGSSLMODE=require
   ENERGY_API_KEY=...
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start Airflow scheduler:
   ```bash
   airflow scheduler
   ```
5. Trigger DAGs:
   ```bash
   airflow dags trigger energy_ingestion_dag
   airflow dags trigger validate_energy_data
   airflow dags trigger store_energy_data
   ```

## Next Steps
- Add **feature engineering DAG** to transform validated data into ML‑ready features.
- Add **model training DAG** for predictive analytics.
- Document DAG runs with screenshots in README.
```

---
