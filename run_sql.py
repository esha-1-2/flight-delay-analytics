import sqlite3

conn = sqlite3.connect("sql/flight_delay.db")

query = """
SELECT
    COUNT(*) AS total_flights,

    SUM(
        CASE
            WHEN ARRIVAL_DELAY > 0 THEN 1
            ELSE 0
        END
    ) AS delayed_flights,

    ROUND(
        SUM(
            CASE
                WHEN ARRIVAL_DELAY > 0 THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS delay_rate,

    SUM(
        CASE
            WHEN CANCELLED = 1 THEN 1
            ELSE 0
        END
    ) AS cancelled_flights,

    ROUND(
        SUM(
            CASE
                WHEN CANCELLED = 1 THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS cancellation_rate,

    ROUND(
        AVG(ARRIVAL_DELAY),
        2
    ) AS average_arrival_delay,

    MAX(ARRIVAL_DELAY) AS maximum_arrival_delay

FROM flights;
"""

result = conn.execute(query)

row = result.fetchone()

print("\nFINAL FLIGHT DELAY PROJECT KPIs")
print("=" * 60)

print("Total Flights:          ", row[0])
print("Delayed Flights:        ", row[1])
print("Delay Rate:             ", row[2], "%")
print("Cancelled Flights:      ", row[3])
print("Cancellation Rate:      ", row[4], "%")
print("Average Arrival Delay:  ", row[5], "minutes")
print("Maximum Arrival Delay:  ", row[6], "minutes")

conn.close()