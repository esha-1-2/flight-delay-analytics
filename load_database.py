from pathlib import Path
import sqlite3
import pandas as pd

csv_path = Path("data/flights.csv")
db_path = Path("sql/flight_delay.db")

if not csv_path.exists():
    raise FileNotFoundError(
        f"Dataset not found: {csv_path}. Download flights.csv from Kaggle "
        "and place it in the data/ folder."
    )

db_path.parent.mkdir(parents=True, exist_ok=True)

# Start fresh so rerunning this script does not duplicate all flight rows.
if db_path.exists():
    db_path.unlink()

with sqlite3.connect(db_path) as conn:
    for chunk in pd.read_csv(
        csv_path,
        chunksize=100_000,
        low_memory=False
    ):
        chunk.to_sql("flights", conn, if_exists="append", index=False)
        print(f"Loaded {len(chunk):,} rows in this batch...")

print(f"DATABASE LOADED SUCCESSFULLY: {db_path}")
