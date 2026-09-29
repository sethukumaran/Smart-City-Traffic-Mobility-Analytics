"""
Smart City Traffic & Mobility Analysis
Senior Data Analyst Portfolio Project
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

DATA_PATH = "smart_city_traffic_mobility.csv"
OUTPUT_DIR = Path("visualizations")
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_PATH, parse_dates=["timestamp"])

# =========================
# 1. BASIC EDA
# =========================
print("="*80)
print("SMART CITY TRAFFIC & MOBILITY — BASIC EDA")
print("="*80)
print("Shape:", df.shape)
print("\nData types:\n", df.dtypes)
print("\nMissing values:\n", df.isna().sum().sort_values(ascending=False))
print("\nDuplicate rows:", df.duplicated().sum())
print("\nDescriptive statistics:\n", df.describe(include="all").T)

# Data quality checks
print("\nUnique record IDs:", df["record_id"].nunique())
print("Date range:", df["timestamp"].min(), "to", df["timestamp"].max())

# Derived fields
df["date"] = df["timestamp"].dt.date
df["month"] = df["timestamp"].dt.to_period("M").astype(str)
df["day_name"] = df["timestamp"].dt.day_name()

# =========================
# 2. KPI SUMMARY
# =========================
kpis = {
    "records": len(df),
    "unique_intersections": df["intersection_id"].nunique(),
    "unique_roads": df["road_id"].nunique(),
    "avg_vehicle_count": df["vehicle_count"].mean(),
    "avg_speed": df["average_speed"].mean(),
    "avg_congestion_score": df["congestion_score"].mean(),
    "avg_wait_minutes": df["average_wait_time"].mean(),
    "avg_emission_estimate": df["emission_estimate"].mean(),
    "avg_fuel_waste": df["fuel_waste_estimate"].mean(),
    "accident_rate_pct": df["accident_reported"].mean()*100,
}
print("\nKPI SUMMARY")
for k,v in kpis.items():
    print(f"{k}: {v:.2f}" if isinstance(v,(float,np.floating)) else f"{k}: {v}")

# =========================
# 3. CATEGORY DISTRIBUTIONS
# =========================
for col in ["city_zone","road_type","congestion_level","peak_period",
            "weather_condition","road_condition","iot_sensor_health"]:
    print(f"\n--- {col} ---")
    print(df[col].value_counts())

# =========================
# 4. BUSINESS AGGREGATIONS
# =========================
zone = df.groupby("city_zone").agg(
    records=("record_id","count"),
    avg_congestion=("congestion_score","mean"),
    avg_speed=("average_speed","mean"),
    avg_wait=("average_wait_time","mean"),
    avg_flow=("traffic_flow_rate","mean"),
    avg_emission=("emission_estimate","mean")
).sort_values("avg_congestion", ascending=False)
print("\nZONE PERFORMANCE\n", zone.round(2))

hour = df.groupby("hour").agg(
    congestion=("congestion_score","mean"),
    speed=("average_speed","mean"),
    wait=("average_wait_time","mean"),
    flow=("traffic_flow_rate","mean")
)
print("\nHOURLY PROFILE\n", hour.round(2))

road = df.groupby("road_type").agg(
    records=("record_id","count"),
    avg_congestion=("congestion_score","mean"),
    avg_speed=("average_speed","mean"),
    avg_wait=("average_wait_time","mean"),
    avg_flow=("traffic_flow_rate","mean"),
    avg_emission=("emission_estimate","mean")
).sort_values("avg_congestion", ascending=False)
print("\nROAD TYPE PERFORMANCE\n", road.round(2))

# =========================
# 5. CORRELATION ANALYSIS
# =========================
numeric_cols = [
    "vehicle_count","average_speed","traffic_density","queue_length",
    "average_wait_time","parking_occupancy","congestion_score",
    "emission_estimate","fuel_waste_estimate","air_quality_index",
    "rainfall_mm","visibility_km","green_light_duration"
]
corr = df[numeric_cols].corr()["congestion_score"].sort_values(ascending=False)
print("\nCORRELATION WITH CONGESTION SCORE\n", corr.round(3))

# =========================
# 6. VISUALIZATIONS
# =========================
sns.set_theme(style="whitegrid")

# 1 Congestion by zone
plt.figure(figsize=(10,6))
zone["avg_congestion"].plot(kind="bar")
plt.title("Average Congestion Score by City Zone")
plt.ylabel("Average congestion score")
plt.xlabel("City zone")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(OUTPUT_DIR/"01_congestion_by_zone.png", dpi=180)
plt.close()

# 2 Hourly congestion
plt.figure(figsize=(11,6))
plt.plot(hour.index, hour["congestion"], marker="o")
plt.title("Hourly Congestion Profile")
plt.xlabel("Hour of day")
plt.ylabel("Average congestion score")
plt.xticks(range(24))
plt.tight_layout()
plt.savefig(OUTPUT_DIR/"02_hourly_congestion.png", dpi=180)
plt.close()

# 3 Hourly speed
plt.figure(figsize=(11,6))
plt.plot(hour.index, hour["speed"], marker="o")
plt.title("Hourly Average Speed")
plt.xlabel("Hour of day")
plt.ylabel("Average speed")
plt.xticks(range(24))
plt.tight_layout()
plt.savefig(OUTPUT_DIR/"03_hourly_speed.png", dpi=180)
plt.close()

# 4 Congestion levels
plt.figure(figsize=(8,5))
df["congestion_level"].value_counts().plot(kind="bar")
plt.title("Distribution of Congestion Levels")
plt.xlabel("Congestion level")
plt.ylabel("Records")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT_DIR/"04_congestion_levels.png", dpi=180)
plt.close()

# 5 Road type
plt.figure(figsize=(9,6))
road["avg_congestion"].plot(kind="bar")
plt.title("Average Congestion by Road Type")
plt.ylabel("Average congestion score")
plt.xlabel("Road type")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(OUTPUT_DIR/"05_congestion_by_road_type.png", dpi=180)
plt.close()

# 6 Weather
weather = df.groupby("weather_condition")["congestion_score"].mean().sort_values(ascending=False)
plt.figure(figsize=(8,5))
weather.plot(kind="bar")
plt.title("Congestion by Weather Condition")
plt.ylabel("Average congestion score")
plt.xlabel("Weather")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(OUTPUT_DIR/"06_congestion_by_weather.png", dpi=180)
plt.close()

# 7 Rush hour comparison
rush = df.groupby("rush_hour")["congestion_score"].mean()
plt.figure(figsize=(7,5))
rush.index = ["Non-rush","Rush hour"]
rush.plot(kind="bar")
plt.title("Rush Hour vs Non-Rush Hour Congestion")
plt.ylabel("Average congestion score")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT_DIR/"07_rush_hour_comparison.png", dpi=180)
plt.close()

# 8 Accident impact
acc = df.groupby("accident_reported").agg(
    congestion=("congestion_score","mean"),
    wait=("average_wait_time","mean"),
    speed=("average_speed","mean")
)
acc.index = ["No accident","Accident"]
ax=acc.plot(kind="bar", figsize=(9,6))
ax.set_title("Traffic Impact When an Accident Is Reported")
ax.set_ylabel("Average value")
ax.set_xlabel("")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT_DIR/"08_accident_impact.png", dpi=180)
plt.close()

# 9 Density vs congestion
sample = df.sample(min(10000,len(df)), random_state=42)
plt.figure(figsize=(9,6))
plt.scatter(sample["traffic_density"], sample["congestion_score"], alpha=0.25)
plt.title("Traffic Density vs Congestion Score")
plt.xlabel("Traffic density")
plt.ylabel("Congestion score")
plt.tight_layout()
plt.savefig(OUTPUT_DIR/"09_density_vs_congestion.png", dpi=180)
plt.close()

# 10 Emission vs congestion
plt.figure(figsize=(9,6))
plt.scatter(sample["congestion_score"], sample["emission_estimate"], alpha=0.25)
plt.title("Congestion vs Emission Estimate")
plt.xlabel("Congestion score")
plt.ylabel("Emission estimate")
plt.tight_layout()
plt.savefig(OUTPUT_DIR/"10_congestion_vs_emissions.png", dpi=180)
plt.close()

# 11 Weekend comparison
week = df.groupby("is_weekend").agg(
    congestion=("congestion_score","mean"),
    speed=("average_speed","mean"),
    wait=("average_wait_time","mean"),
    flow=("traffic_flow_rate","mean")
)
week.index=["Weekday","Weekend"]
week.plot(kind="bar", figsize=(10,6))
plt.title("Weekday vs Weekend Traffic Profile")
plt.ylabel("Average value")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT_DIR/"11_weekday_vs_weekend.png", dpi=180)
plt.close()

# 12 Correlation heatmap
plt.figure(figsize=(12,9))
sns.heatmap(df[numeric_cols].corr(), cmap="coolwarm", center=0)
plt.title("Traffic & Mobility Correlation Matrix")
plt.tight_layout()
plt.savefig(OUTPUT_DIR/"12_correlation_heatmap.png", dpi=180)
plt.close()

print(f"\nSaved visualizations to: {OUTPUT_DIR.resolve()}")
