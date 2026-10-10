from pathlib import Path
import sqlite3

db_path = Path("sql/flight_delay.db")
if not db_path.exists():
    raise FileNotFoundError(
        f"Database not found: {db_path}. Run 'python load_database.py' first."
    )

query = """
SELECT
    COUNT(*) AS total_flights,
    COUNT(ARRIVAL_DELAY) AS flights_with_known_arrival_delay,
    SUM(CASE WHEN ARRIVAL_DELAY > 0 THEN 1 ELSE 0 END) AS delayed_flights,
    ROUND(
        100.0 * SUM(CASE WHEN ARRIVAL_DELAY > 0 THEN 1 ELSE 0 END)
        / NULLIF(COUNT(ARRIVAL_DELAY), 0),
        2
    ) AS delay_rate,
    SUM(CASE WHEN CANCELLED = 1 THEN 1 ELSE 0 END) AS cancelled_flights,
    ROUND(
        100.0 * SUM(CASE WHEN CANCELLED = 1 THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS cancellation_rate,
    ROUND(AVG(ARRIVAL_DELAY), 2) AS average_arrival_delay,
    MAX(ARRIVAL_DELAY) AS maximum_arrival_delay
FROM flights;
"""

with sqlite3.connect(db_path) as conn:
    row = conn.execute(query).fetchone()

print("\nFINAL FLIGHT DELAY PROJECT KPIs")
print("=" * 60)
print(f"Total Flights:          {row[0]:,}")
print(f"Flights with Known Arrival Delay: {row[1]:,}")
print(f"Delayed Flights:        {row[2]:,}")
print(f"Delay Rate:             {row[3]}%")
print(f"Cancelled Flights:      {row[4]:,}")
print(f"Cancellation Rate:      {row[5]}%")
print(f"Average Arrival Delay:  {row[6]} minutes")
print(f"Maximum Arrival Delay:  {row[7]} minutes")
