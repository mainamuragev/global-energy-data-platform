import os
import requests
import psycopg
import pandas as pd
from dotenv import load_dotenv
from datetime import date

# Load environment variables
load_dotenv()

# Connect to Postgres
conn = psycopg.connect(
    host=os.getenv("PGHOST"),
    port=os.getenv("PGPORT"),
    dbname=os.getenv("PGDATABASE"),
    user=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    sslmode=os.getenv("PGSSLMODE")
)
cur = conn.cursor()

# Create table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS energy_prices (
    id SERIAL PRIMARY KEY,
    date DATE,
    commodity TEXT,
    price NUMERIC,
    source TEXT
)
""")

# Fetch live data from EnergypriceAPI
API_KEY = os.getenv("ENERGY_API_KEY")
url = f"https://api.energypriceapi.com/v1/latest?apikey={API_KEY}&base=USD&currencies=WTI,BRENT,NATURALGAS,GASOLINE"
print("Request URL:", url)

response = requests.get(url).json()
print("Raw response:", response)

if response.get("success"):
    rates = response["rates"]
    today = date.today().isoformat()
    data = [
        (today, "WTI", rates.get("WTI"), "EnergypriceAPI"),
        (today, "BRENT", rates.get("BRENT"), "EnergypriceAPI"),
        (today, "NATURALGAS", rates.get("NATURALGAS"), "EnergypriceAPI"),
        (today, "GASOLINE", rates.get("GASOLINE"), "EnergypriceAPI"),
    ]

    # Insert into Postgres
    cur.executemany(
        "INSERT INTO energy_prices (date, commodity, price, source) VALUES (%s, %s, %s, %s)",
        data
    )
    conn.commit()
    print("Inserted live energy data:", data)

    # Save raw CSV for validation DAG
    raw_path = "/home/mainavm/global-energy-data-platform/data/raw"
    os.makedirs(raw_path, exist_ok=True)
    df = pd.DataFrame(data, columns=["date", "commodity", "price", "source"])
    df.to_csv(f"{raw_path}/energy.csv", index=False)
    print(f"Raw energy data saved to {raw_path}/energy.csv")

else:
    print("API error:", response)

cur.close()
conn.close()
