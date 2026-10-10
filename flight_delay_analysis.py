import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# LOAD FLIGHT DATA
# ==========================================

flights = pd.read_csv("data/flights.csv", low_memory=False)

print("Flight data loaded successfully!")
print("Total flights:", len(flights))


# ==========================================
# ANALYSIS 1: DELAY RATE BY AIRLINE
# ==========================================

valid = flights["ARRIVAL_DELAY"].notna()

airline_delay_rate = (
    flights[valid]
    .groupby("AIRLINE")["ARRIVAL_DELAY"]
    .apply(lambda x: (x > 0).mean() * 100)
    .sort_values(ascending=False)
)

print("\nDelay Rate by Airline:")
print(airline_delay_rate.round(2))


# Create bar chart
plt.figure(figsize=(10, 6))

sns.barplot(
    x=airline_delay_rate.index,
    y=airline_delay_rate.values
)

plt.title("Flight Delay Rate by Airline")
plt.xlabel("Airline")
plt.ylabel("Delay Rate (%)")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ==========================================
# ANALYSIS 2: AVERAGE ARRIVAL DELAY BY MONTH
# ==========================================

monthly_delay = (
    flights.groupby("MONTH")["ARRIVAL_DELAY"]
    .mean()
)

print("\nAverage Arrival Delay by Month:")
print(monthly_delay.round(2))


# Create line chart
plt.figure(figsize=(10, 6))

sns.lineplot(
    x=monthly_delay.index,
    y=monthly_delay.values,
    marker="o"
)

plt.title("Average Flight Arrival Delay by Month")
plt.xlabel("Month")
plt.ylabel("Average Arrival Delay (minutes)")
plt.xticks(range(1, 13))
plt.grid(True)

plt.tight_layout()
plt.show()

# ==========================================
# ANALYSIS 3: CANCELLATION RATE BY AIRLINE
# ==========================================

cancellation_rate = (
    flights.groupby("AIRLINE")["CANCELLED"]
    .mean() * 100
)

cancellation_rate = cancellation_rate.sort_values(ascending=False)

print("\nCancellation Rate by Airline:")
print(cancellation_rate.round(2))


# Create bar chart
plt.figure(figsize=(10, 6))

sns.barplot(
    x=cancellation_rate.index,
    y=cancellation_rate.values
)

plt.title("Flight Cancellation Rate by Airline")
plt.xlabel("Airline")
plt.ylabel("Cancellation Rate (%)")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# ==========================================
# ANALYSIS 4: DELAY RATE BY DESTINATION AIRPORT
# ==========================================

airport_delay_rate = (
    flights[flights["ARRIVAL_DELAY"].notna()]
    .groupby("DESTINATION_AIRPORT")["ARRIVAL_DELAY"]
    .apply(lambda x: (x > 0).mean() * 100)
    .sort_values(ascending=False)
)

# Show top 20 airports
top_airports = airport_delay_rate.head(20)

print("\nTop 20 Airports by Delay Rate:")
print(top_airports.round(2))


# Create bar chart
plt.figure(figsize=(12, 7))

sns.barplot(
    x=top_airports.values,
    y=top_airports.index
)

plt.title("Top 20 Airports by Flight Delay Rate")
plt.xlabel("Delay Rate (%)")
plt.ylabel("Destination Airport")

plt.tight_layout()
plt.show()

# ==========================================
# ANALYSIS 5: CLEAN AIRPORT INFORMATION
# ==========================================

# Load airport data
airports = pd.read_csv("data/airports.csv")

print("\nAirport Data:")
print(airports.head())

print("\nAirport Columns:")
print(airports.columns)


# Clean airport column names
airports.columns = airports.columns.str.upper()


# Show the first few airport records
print("\nCleaned Airport Data:")
print(airports.head())

# ==========================================
# ANALYSIS 6: ADD AIRPORT NAMES TO FLIGHT DATA
# ==========================================

# Create a lookup table for airport information
airport_lookup = airports[
    ["IATA_CODE", "AIRPORT", "CITY", "STATE"]
].copy()


# Rename columns for destination airport
airport_lookup = airport_lookup.rename(columns={
    "IATA_CODE": "DESTINATION_AIRPORT",
    "AIRPORT": "DESTINATION_AIRPORT_NAME",
    "CITY": "DESTINATION_CITY",
    "STATE": "DESTINATION_STATE"
})


# Convert airport codes to strings
flights["DESTINATION_AIRPORT"] = (
    flights["DESTINATION_AIRPORT"].astype(str)
)

airport_lookup["DESTINATION_AIRPORT"] = (
    airport_lookup["DESTINATION_AIRPORT"].astype(str)
)


# Merge airport information with flight data
flights_with_airports = flights.merge(
    airport_lookup,
    on="DESTINATION_AIRPORT",
    how="left"
)


print("\nFlight Data with Airport Information:")
print(
    flights_with_airports[
        [
            "DESTINATION_AIRPORT",
            "DESTINATION_AIRPORT_NAME",
            "DESTINATION_CITY",
            "DESTINATION_STATE"
        ]
    ].head(10)
)

# ==========================================
# ANALYSIS 7: TOP AIRPORTS BY DELAY RATE
# WITH AIRPORT NAMES
# ==========================================

airport_delay_rate = (
    flights_with_airports[
        flights_with_airports["ARRIVAL_DELAY"].notna()
    ]
    .groupby([
        "DESTINATION_AIRPORT",
        "DESTINATION_AIRPORT_NAME",
        "DESTINATION_CITY"
    ])["ARRIVAL_DELAY"]
    .apply(lambda x: (x > 0).mean() * 100)
    .sort_values(ascending=False)
)

# Get top 20 airports
top_airports = airport_delay_rate.head(20)

print("\nTop 20 Airports by Delay Rate:")
print(top_airports.round(2))


# Create bar chart
plt.figure(figsize=(12, 8))

sns.barplot(
    x=top_airports.values,
    y=top_airports.index.get_level_values("DESTINATION_AIRPORT")
)

plt.title("Top 20 Airports by Flight Delay Rate")
plt.xlabel("Delay Rate (%)")
plt.ylabel("Airport Code")

plt.tight_layout()
plt.show()

# ==========================================
# ANALYSIS 8: MOST DELAYED FLIGHT ROUTES
# ==========================================

route_delay = (
    flights[flights["ARRIVAL_DELAY"].notna()]
    .groupby([
        "ORIGIN_AIRPORT",
        "DESTINATION_AIRPORT"
    ])
    .agg(
        Average_Delay=("ARRIVAL_DELAY", "mean"),
        Flight_Count=("ARRIVAL_DELAY", "count")
    )
    .reset_index()
)


# Keep routes with at least 100 flights
route_delay = route_delay[
    route_delay["Flight_Count"] >= 100
]


# Sort by average delay
top_routes = route_delay.sort_values(
    "Average_Delay",
    ascending=False
).head(20)


print("\nTop 20 Most Delayed Routes:")
print(top_routes.round(2))


# Create route names
top_routes["ROUTE"] = (
    top_routes["ORIGIN_AIRPORT"]
    + " → "
    + top_routes["DESTINATION_AIRPORT"]
)


# Create bar chart
plt.figure(figsize=(12, 8))

sns.barplot(
    x=top_routes["Average_Delay"],
    y=top_routes["ROUTE"]
)

plt.title("Top 20 Most Delayed Flight Routes")
plt.xlabel("Average Arrival Delay (minutes)")
plt.ylabel("Flight Route")

plt.tight_layout()
plt.show()

# ==========================================
# ANALYSIS 9: DELAY CAUSES
# ==========================================

delay_causes = {
    "Air System": flights["AIR_SYSTEM_DELAY"].sum(),
    "Security": flights["SECURITY_DELAY"].sum(),
    "Airline": flights["AIRLINE_DELAY"].sum(),
    "Late Aircraft": flights["LATE_AIRCRAFT_DELAY"].sum(),
    "Weather": flights["WEATHER_DELAY"].sum()
}

delay_causes = pd.Series(delay_causes)

delay_causes = delay_causes.sort_values(
    ascending=False
)

print("\nTotal Delay Minutes by Cause:")
print(delay_causes.round(0))


# Calculate percentage contribution
delay_cause_percentage = (
    delay_causes / delay_causes.sum() * 100
)

print("\nDelay Cause Percentage:")
print(delay_cause_percentage.round(2))


# Create bar chart
plt.figure(figsize=(10, 6))

sns.barplot(
    x=delay_cause_percentage.values,
    y=delay_cause_percentage.index
)

plt.title("Flight Delay Causes")
plt.xlabel("Percentage of Total Delay (%)")
plt.ylabel("Delay Cause")

plt.tight_layout()
plt.show()

# ==========================================
# ANALYSIS 10: CANCELLATION ANALYSIS
# ==========================================

cancellation_rate = (
    flights.groupby("AIRLINE")["CANCELLED"]
    .mean() * 100
)

cancellation_rate = cancellation_rate.sort_values(ascending=False)

print("\nCancellation Rate by Airline (%):")
print(cancellation_rate.round(2))

plt.figure(figsize=(10, 6))

sns.barplot(
    x=cancellation_rate.values,
    y=cancellation_rate.index
)

plt.title("Cancellation Rate by Airline")
plt.xlabel("Cancellation Rate (%)")
plt.ylabel("Airline")

plt.tight_layout()
plt.show()

# ==========================================
# ANALYSIS 11: DELAY BY MONTH
# ==========================================

monthly_delay = (
    flights.groupby("MONTH")["ARRIVAL_DELAY"]
    .mean()
)

print("\nAverage Arrival Delay by Month:")
print(monthly_delay.round(2))

plt.figure(figsize=(10, 6))

sns.lineplot(
    x=monthly_delay.index,
    y=monthly_delay.values,
    marker="o"
)

plt.title("Average Flight Delay by Month")
plt.xlabel("Month")
plt.ylabel("Average Arrival Delay (minutes)")

plt.xticks(range(1, 13))

plt.tight_layout()
plt.show()

# ==========================================
# ANALYSIS 12: DELAY BY DAY OF WEEK
# ==========================================

weekly_delay = (
    flights.groupby("DAY_OF_WEEK")["ARRIVAL_DELAY"]
    .mean()
)

day_names = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday"
}

weekly_delay.index = weekly_delay.index.map(day_names)

print("\nAverage Arrival Delay by Day of Week:")
print(weekly_delay.round(2))

plt.figure(figsize=(10, 6))

sns.barplot(
    x=weekly_delay.index,
    y=weekly_delay.values
)

plt.title("Average Flight Delay by Day of Week")
plt.xlabel("Day of Week")
plt.ylabel("Average Arrival Delay (minutes)")

plt.xticks(rotation=30)

plt.tight_layout()
plt.show()

# ==========================================
# ANALYSIS 13: DEPARTURE VS ARRIVAL DELAY
# ==========================================

delay_relationship = flights[
    ["DEPARTURE_DELAY", "ARRIVAL_DELAY"]
].dropna()

correlation = delay_relationship[
    "DEPARTURE_DELAY"
].corr(
    delay_relationship["ARRIVAL_DELAY"]
)

print("\nCorrelation between Departure Delay and Arrival Delay:")
print(round(correlation, 2))

plt.figure(figsize=(10, 6))

sample_data = delay_relationship.sample(
    n=10000,
    random_state=42
)

sns.scatterplot(
    data=sample_data,
    x="DEPARTURE_DELAY",
    y="ARRIVAL_DELAY",
    alpha=0.4
)

plt.title("Departure Delay vs Arrival Delay")
plt.xlabel("Departure Delay (minutes)")
plt.ylabel("Arrival Delay (minutes)")

plt.tight_layout()
plt.show()

# ==========================================
# ANALYSIS 14: DELAY SEVERITY
# ==========================================

delay_data = flights[
    flights["ARRIVAL_DELAY"].notna()
].copy()

def classify_delay(delay):
    if delay <= 0:
        return "On Time / Early"
    elif delay <= 30:
        return "Minor Delay"
    elif delay <= 60:
        return "Moderate Delay"
    elif delay <= 120:
        return "Severe Delay"
    else:
        return "Extreme Delay"

delay_data["DELAY_SEVERITY"] = (
    delay_data["ARRIVAL_DELAY"]
    .apply(classify_delay)
)

severity_counts = (
    delay_data["DELAY_SEVERITY"]
    .value_counts()
)

severity_percentage = (
    severity_counts /
    severity_counts.sum() * 100
)

print("\nDelay Severity Count:")
print(severity_counts)

print("\nDelay Severity Percentage:")
print(severity_percentage.round(2))

plt.figure(figsize=(10, 6))

sns.barplot(
    x=severity_percentage.index,
    y=severity_percentage.values
)

plt.title("Flight Delay Severity")
plt.xlabel("Delay Category")
plt.ylabel("Percentage of Flights (%)")

plt.xticks(rotation=20)

plt.tight_layout()
plt.show()

# ==========================================
# ANALYSIS 15: TOP AIRPORTS BY DELAY RATE
# ==========================================

airport_analysis = (
    flights_with_airports[
        flights_with_airports["ARRIVAL_DELAY"].notna()
    ]
    .groupby([
        "DESTINATION_AIRPORT",
        "DESTINATION_AIRPORT_NAME",
        "DESTINATION_CITY"
    ])
    .agg(
        Flight_Count=("ARRIVAL_DELAY", "count"),
        Average_Delay=("ARRIVAL_DELAY", "mean"),
        Delay_Rate=("ARRIVAL_DELAY", lambda x: (x > 0).mean() * 100)
    )
    .reset_index()
)

# Keep airports with at least 500 flights
airport_analysis = airport_analysis[
    airport_analysis["Flight_Count"] >= 500
]

top_airports = (
    airport_analysis
    .sort_values("Delay_Rate", ascending=False)
    .head(20)
)

print("\nTop Airports by Delay Rate:")
print(
    top_airports[
        [
            "DESTINATION_AIRPORT",
            "DESTINATION_AIRPORT_NAME",
            "DESTINATION_CITY",
            "Flight_Count",
            "Average_Delay",
            "Delay_Rate"
        ]
    ].round(2)
)

plt.figure(figsize=(12, 7))

sns.barplot(
    data=top_airports,
    x="Delay_Rate",
    y="DESTINATION_AIRPORT"
)

plt.title("Top Airports by Flight Delay Rate")
plt.xlabel("Delay Rate (%)")
plt.ylabel("Airport")

plt.tight_layout()
plt.show()

# ==========================================
# ANALYSIS 16: FINAL PROJECT KPI SUMMARY
# ==========================================

total_flights = len(flights)

delayed_flights = (
    flights["ARRIVAL_DELAY"] > 0
).sum()

cancelled_flights = (
    flights["CANCELLED"] == 1
).sum()

delay_rate = (
    delayed_flights / total_flights
) * 100

cancellation_rate = (
    cancelled_flights / total_flights
) * 100

average_delay = (
    flights["ARRIVAL_DELAY"].mean()
)

maximum_delay = (
    flights["ARRIVAL_DELAY"].max()
)

print("\n==========================================")
print("FINAL PROJECT KPI SUMMARY")
print("==========================================")

print(f"Total Flights: {total_flights:,}")
print(f"Delayed Flights: {delayed_flights:,}")
print(f"Delay Rate: {delay_rate:.2f}%")
print(f"Cancelled Flights: {cancelled_flights:,}")
print(f"Cancellation Rate: {cancellation_rate:.2f}%")
print(f"Average Arrival Delay: {average_delay:.2f} minutes")
print(f"Maximum Arrival Delay: {maximum_delay:.2f} minutes")

print("==========================================")


import sqlite3

conn = sqlite3.connect("sql/flight_delay.db")

print("SQLite database opened successfully!")

conn.close()