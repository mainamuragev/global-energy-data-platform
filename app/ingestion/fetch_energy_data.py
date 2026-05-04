import os
import requests
import psycopg
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
url = f"https://api.energypriceapi.com/v1/latest?apikey={API_KEY}"
response = requests.get(url).json()

if response.get("success"):
    rates = response["rates"]
    today = date.today().isoformat()
    data = [
        (today, "WTI", rates["WTI"], "EnergypriceAPI"),
        (today, "BRENT", rates["BRENT"], "EnergypriceAPI"),
        (today, "NATURALGAS", rates["NATURALGAS"], "EnergypriceAPI"),
        (today, "GASOLINE", rates["GASOLINE"], "EnergypriceAPI"),
    ]

    cur.executemany(
        "INSERT INTO energy_prices (date, commodity, price, source) VALUES (%s, %s, %s, %s)",
        data
    )
    conn.commit()
    print("Inserted live energy data:", data)
else:
    print("API error:", response)

cur.close()
conn.close()
