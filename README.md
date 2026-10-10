# Flight Delay & Airport Operations Analytics

## Project Overview
This project analyzes flight delays, cancellations, airline performance, and monthly arrival-delay trends using Python, SQL, and Power BI.

## Objectives
- Analyze overall flight delays and cancellations.
- Compare delay rates across airlines.
- Identify monthly arrival-delay patterns.
- Explore the major causes of flight delays.
- Build a Power BI dashboard to present key findings.

## Tools & Technologies
- **Python:** Data analysis and preprocessing
- **Pandas:** Data manipulation
- **SQL / SQLite:** Data storage and querying
- **Power BI:** Interactive dashboard and visualizations
- **DAX:** Dashboard calculations

## Key Findings
- Total flights analyzed: 5,819,079
- Delayed flights: 2,086,896
- Overall delay rate: 35.86%
- Cancelled flights: 89,884
- Average arrival delay: 4.41 minutes
- Late-arriving aircraft and airline-related issues were the two largest reported delay causes.

## Dashboard
The Power BI dashboard includes five KPI cards and three charts:
- Airline Delay Rate Comparison
- Cancellation Rate by Airline
- Average Arrival Delay by Month

## Project Files
- `flight_delay_analysis.py` — Python analysis
- `load_database.py` — Database loading script
- `run_sql.py` — SQL execution script
- `flight_delay_analysis.sql` — SQL analysis queries

## Dataset
The analysis uses the 2015 Flight Delays and Cancellations dataset from the U.S. Department of Transportation, available on Kaggle.

Dataset source: https://www.kaggle.com/datasets/usdot/flight-delays

## Author
Esha Patel
