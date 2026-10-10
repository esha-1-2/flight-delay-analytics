-- Flight Delay Analytics: reusable SQLite queries
-- Run these after executing load_database.py.
-- A positive arrival delay means ARRIVAL_DELAY > 0.
-- Delay-rate denominator below is flights with a recorded arrival delay.

-- 1. Overall dataset and KPI summary
SELECT
    COUNT(*) AS total_flights,
    SUM(CASE WHEN ARRIVAL_DELAY > 0 THEN 1 ELSE 0 END) AS delayed_flights,
    ROUND(
        100.0 * SUM(CASE WHEN ARRIVAL_DELAY > 0 THEN 1 ELSE 0 END)
        / NULLIF(COUNT(ARRIVAL_DELAY), 0), 2
    ) AS delay_rate_among_known_arrivals_pct,
    SUM(CASE WHEN CANCELLED = 1 THEN 1 ELSE 0 END) AS cancelled_flights,
    ROUND(100.0 * AVG(CASE WHEN CANCELLED = 1 THEN 1.0 ELSE 0.0 END), 2)
        AS cancellation_rate_pct,
    ROUND(AVG(ARRIVAL_DELAY), 2) AS average_arrival_delay_minutes
FROM flights;

-- 2. Delay rate by airline (excludes missing arrival-delay values)
SELECT
    AIRLINE,
    COUNT(ARRIVAL_DELAY) AS flights_with_known_arrival_delay,
    SUM(CASE WHEN ARRIVAL_DELAY > 0 THEN 1 ELSE 0 END) AS delayed_flights,
    ROUND(
        100.0 * SUM(CASE WHEN ARRIVAL_DELAY > 0 THEN 1 ELSE 0 END)
        / NULLIF(COUNT(ARRIVAL_DELAY), 0), 2
    ) AS delay_rate_pct
FROM flights
GROUP BY AIRLINE
ORDER BY delay_rate_pct DESC;

-- 3. Average arrival delay by month
SELECT
    MONTH,
    ROUND(AVG(ARRIVAL_DELAY), 2) AS average_arrival_delay_minutes
FROM flights
GROUP BY MONTH
ORDER BY MONTH;

-- 4. Cancellation rate by airline
SELECT
    AIRLINE,
    COUNT(*) AS total_flights,
    SUM(CASE WHEN CANCELLED = 1 THEN 1 ELSE 0 END) AS cancelled_flights,
    ROUND(100.0 * AVG(CASE WHEN CANCELLED = 1 THEN 1.0 ELSE 0.0 END), 2)
        AS cancellation_rate_pct
FROM flights
GROUP BY AIRLINE
ORDER BY cancellation_rate_pct DESC;
