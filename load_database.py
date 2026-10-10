import sqlite3
import pandas as pd

csv_path = "data/flights.csv"
db_path = "sql/flight_delay.db"

conn = sqlite3.connect(db_path)

for chunk in pd.read_csv(
    csv_path,
    chunksize=100000,
    low_memory=False
):
    chunk.to_sql(
        "flights",
        conn,
        if_exists="append",
        index=False
    )
    print("100,000 rows loaded...")

conn.close()

print("DATABASE LOADED SUCCESSFULLY!")