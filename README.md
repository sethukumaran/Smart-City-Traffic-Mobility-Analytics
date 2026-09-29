# Smart-City-Traffic-Mobility-Analytics

## Project Overview
This project analyzes a smart-city traffic and mobility dataset containing **204,000 traffic observations across 47 variables**. The analysis is designed from a Senior Data Analyst / Business Intelligence perspective, combining data-quality assessment, exploratory data analysis, SQL business questions, statistical relationships, operational insights, and visualization.

The objective is to identify:
- Where congestion is concentrated
- When congestion is highest
- Which road and city-zone characteristics are associated with traffic pressure
- How congestion affects speed, waiting time, emissions, and fuel waste
- The operational impact of accidents and weather
- Potential areas for traffic-signal optimization and mobility intervention

## Dataset

**File:** `smart_city_traffic_mobility.csv`

### Dataset profile

| Metric | Value |
|---|---:|
| Records | 204,000 |
| Columns | 47 |
| City zones | 6 |
| Roads | 94 |
| Intersections | 100 |
| Time coverage | 2026-01-01 to 2026-03-26 |
| Missing values | 0 |
| Duplicate rows | 0 |

### Important fields

- `city_zone` — geographic/business zone
- `road_type` — Highway, Arterial, Collector, Local Street
- `vehicle_count` — observed traffic volume
- `average_speed` — observed average vehicle speed
- `traffic_density` — traffic density indicator
- `queue_length` — queue length
- `average_wait_time` — estimated waiting time
- `peak_period` — Night, Off-Peak, Morning Peak, Midday, Evening Peak
- `congestion_score` — 0–100 congestion indicator
- `congestion_level` — Low, Moderate, High, Severe
- `emission_estimate` — traffic-related emissions estimate
- `fuel_waste_estimate` — estimated fuel waste
- `accident_reported` — accident indicator
- `weather_condition` — weather category
- `road_condition` — Good, Wet, Poor
- `signal_cycle_seconds` / `green_light_duration` — traffic signal characteristics
- `iot_sensor_health` — sensor health status

## Business Questions

1. What is the overall congestion level?
2. Which city zones experience the highest congestion?
3. Which hours create the greatest operational pressure?
4. How different are rush-hour and non-rush-hour conditions?
5. Which road types experience the most congestion?
6. What is the relationship between traffic density and congestion?
7. How does congestion affect emissions and fuel waste?
8. How much does an accident change waiting time and speed?
9. How do weather and road conditions relate to congestion?
10. Which intersections should be considered for operational review?

## Key Findings

### 1. Midday is the strongest congestion window

Average congestion reaches approximately **99–100 during late morning and midday hours**, especially around hours 10–14. Average speed falls substantially during these hours while traffic flow and waiting time increase.

**Business implication:** Traffic-control resources should not focus only on traditional morning/evening commuting windows. The dataset indicates a major **midday traffic-management requirement**.

### 2. Rush hour materially worsens traffic conditions

| Metric | Non-rush | Rush hour |
|---|---:|---:|
| Avg congestion | 44.38 | 71.25 |
| Avg speed | 44.15 | 35.02 |
| Avg wait | 10.00 | 20.28 |
| Avg emissions | 217.69 | 407.47 |
| Avg fuel waste | 60.28 | 118.64 |

Rush-hour congestion is roughly **61% higher** than non-rush congestion in this dataset, while average waiting time is roughly doubled.

**Business implication:** Dynamic signal timing, demand management, incident response, and route diversion strategies should be evaluated for high-pressure periods.

### 3. Downtown Core and Financial District have the highest zone-level congestion

| Zone | Avg congestion | Avg speed | Avg wait |
|---|---:|---:|---:|
| Downtown Core | 52.48 | 39.31 | 15.89 |
| Financial District | 52.45 | 42.18 | 15.85 |
| Suburban North | 47.94 | 41.48 | 8.98 |
| Residential West | 47.93 | 42.59 | 8.76 |
| Tech Park | 47.88 | 48.37 | 9.20 |
| Industrial East | 47.87 | 44.05 | 8.91 |

**Business implication:** Downtown and Financial District corridors deserve priority for intersection-level diagnostics, signal optimization, parking/loading management, and incident-response planning.

### 4. Traffic density is the strongest observed numerical driver

Correlation with congestion score:

| Variable | Correlation |
|---|---:|
| Traffic density | 0.946 |
| Vehicle count | 0.885 |
| Green-light duration | 0.884 |
| Emission estimate | 0.766 |
| Fuel waste estimate | 0.697 |
| Queue length | 0.595 |
| Average wait time | 0.590 |
| Average speed | -0.680 |

These are **associations, not causal estimates**. In particular, the strong relationship involving green-light duration should not be interpreted as proof that longer green times cause congestion; signal timing may itself be adjusted in response to traffic conditions.

### 5. Severe congestion is operationally expensive

Severe congestion observations show approximately:

- Congestion score: **98.99**
- Average speed: **21.67**
- Average wait: **31.87**
- Traffic flow: **1,629**
- Emission estimate: **611.59**

Compared with low congestion, severe conditions are associated with much lower speed and substantially higher emissions.

**Business implication:** A congestion-management program should track both mobility and environmental KPIs rather than congestion score alone.

### 6. Accidents create a major disruption signal

| Metric | No accident | Accident |
|---|---:|---:|
| Avg congestion | 49.76 | 62.47 |
| Avg speed | 42.50 | 29.21 |
| Avg wait | 11.12 | 63.06 |

Accident observations have approximately **5.7× the average waiting time** of non-accident observations.

**Business implication:** Faster incident detection, emergency-response coordination, and automated diversion messaging could have substantial operational value.

### 7. Weather matters, but its effect is smaller than traffic volume

Heavy rain has the highest average congestion among weather categories, while clear conditions have lower congestion on average. However, the overall correlations of rainfall and visibility with congestion are comparatively weak in this dataset.

**Business implication:** Weather should be included in operational models, but traffic demand and density appear more directly associated with congestion.

### 8. Weekends have materially lighter traffic

Weekend observations show:

- Lower congestion
- Higher average speed
- Lower waiting time
- Lower traffic flow

This indicates a clear weekday/weekend mobility pattern.

## Recommended Business Actions

### A. Traffic signal optimization

Prioritize signal-timing analysis around:

- Downtown Core
- Financial District
- Midday high-congestion windows
- Rush-hour periods
- High-congestion intersections

Use traffic volume, queue length, average speed, and waiting time together rather than optimizing for a single KPI.

### B. Incident management

Create a rapid-response workflow for accident events:

1. Detect incident
2. Validate through traffic cameras/sensors
3. Adjust nearby signals
4. Publish diversion guidance
5. Monitor queue clearance
6. Measure recovery time

### C. Congestion hotspot program

Create a recurring intersection scorecard containing:

- Average congestion
- 95th percentile congestion
- Average wait
- Queue length
- Accident frequency
- Emission estimate
- Traffic volume
- Sensor health

### D. Environmental monitoring

Use congestion and emissions together to identify corridors where mobility improvements may also reduce environmental impact.

### E. Smart-city KPI dashboard

A production dashboard could include:

**Executive KPIs**
- Average congestion
- Average speed
- Average wait
- Vehicle volume
- Severe congestion %
- Accident rate
- Emission estimate
- Fuel waste estimate

**Operational views**
- Hourly congestion heatmap
- Zone ranking
- Intersection hotspot table
- Accident impact
- Weather impact
- Signal performance
- Sensor health

## SQL Analysis

See:

`sql/smart_city_traffic_analysis.sql`

The SQL file includes:

- Data-quality checks
- KPI calculations
- Zone analysis
- Road-type analysis
- Hourly analysis
- Peak-period analysis
- Rush-hour comparison
- Accident impact
- Weather impact
- Road-condition analysis
- Weekend/weekday analysis
- Hotspot identification
- Correlation analysis
- Sensor monitoring

## Python Analysis

See:

`python/smart_city_traffic_analysis.py`

The Python workflow covers:

1. Dataset loading
2. Data types
3. Missing-value checks
4. Duplicate checks
5. Date-range validation
6. Descriptive statistics
7. KPI calculation
8. Categorical distributions
9. Grouped business analysis
10. Correlation analysis
11. Visualization generation

## Visualizations

The `visualizations/` folder contains:

1. Congestion by city zone
2. Hourly congestion
3. Hourly speed
4. Congestion-level distribution
5. Congestion by road type
6. Congestion by weather
7. Rush-hour comparison
8. Accident impact
9. Traffic density vs congestion
10. Congestion vs emissions
11. Weekday vs weekend
12. Correlation heatmap

## Data Quality Notes

The supplied dataset contains **204,000 records with zero missing values and zero duplicate rows**. Record IDs are unique.

There are also unusually large maximum values for some operational fields such as queue length and average waiting time. These should be investigated as potential extreme observations before using the data for predictive modeling or automated operational thresholds.

## Analytical Limitations

- The dataset appears structured for smart-city analytics and should not automatically be treated as a direct real-world traffic sensor feed.
- Correlation does not establish causation.
- Emission and fuel-waste fields are estimates rather than direct measurements.
- The dataset covers approximately three months, so longer-term seasonal effects cannot be assessed.
- City zones and road/intersection IDs are anonymized.
- Business recommendations should be validated against actual traffic-control constraints, infrastructure capacity, and local operating procedures.

## Key business insights
- 204,000 records, 47 columns, covering Jan 1–Mar 26, 2026.
- No missing values and no duplicate rows.
- Midday is the major congestion window: congestion reaches roughly 99–100 around hours 10–14.
- Rush-hour congestion averages 71.25 vs 44.38 during non-rush periods.
- Rush-hour average waiting time is 20.28 vs 10.00 minutes.
- Downtown Core and Financial District have the highest average zone-level congestion.
- Traffic density has a very strong association with congestion (r ≈ 0.946).
- Vehicle count is also strongly associated with congestion (r ≈ 0.885).
- Average speed has a negative relationship with congestion (r ≈ -0.680).
- Accident observations have approximately 63.06 minutes average waiting time vs 11.12 minutes when no accident is reported.
- Severe congestion is associated with much higher estimated emissions and lower average speed.
- Weekends show materially lower congestion and waiting times than weekdays.
- Heavy rain is associated with higher congestion, although traffic-volume variables show much stronger relationships.

## Conclusion

This project demonstrates an end-to-end analytics workflow for smart-city traffic management. The strongest analytical signal is the relationship between **traffic density, vehicle volume, speed, congestion, and downstream environmental impact**.

The dataset indicates that congestion is not simply an evening commuting problem. **Late-morning and midday periods show extremely high congestion**, while Downtown Core and Financial District observations show elevated zone-level pressure. Accident events are associated with substantially higher waiting times and lower speeds, making incident management an important operational lever.

From a senior analyst perspective, the next step would be to move from descriptive analytics toward a **traffic operations dashboard and predictive congestion model**, with particular emphasis on hotspot detection, signal optimization, incident response, and environmental impact monitoring.

