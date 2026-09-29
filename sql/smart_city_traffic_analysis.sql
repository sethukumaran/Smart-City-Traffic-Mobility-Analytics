-- Smart City Traffic & Mobility Analysis
-- SQL dialect: PostgreSQL / ANSI-style SQL
-- Load the CSV into a table named smart_city_traffic_mobility.

-- 1. Dataset overview
SELECT COUNT(*) AS total_records,
       COUNT(DISTINCT city_zone) AS zones,
       COUNT(DISTINCT road_id) AS roads,
       COUNT(DISTINCT intersection_id) AS intersections,
       MIN(timestamp) AS start_time,
       MAX(timestamp) AS end_time
FROM smart_city_traffic_mobility;

-- 2. Data quality checks
SELECT
    COUNT(*) AS total_rows,
    COUNT(*) - COUNT(record_id) AS missing_record_id,
    COUNT(DISTINCT record_id) AS unique_record_ids
FROM smart_city_traffic_mobility;

SELECT record_id, COUNT(*) AS duplicate_count
FROM smart_city_traffic_mobility
GROUP BY record_id
HAVING COUNT(*) > 1;

-- 3. Overall KPIs
SELECT
    ROUND(AVG(vehicle_count),2) AS avg_vehicle_count,
    ROUND(AVG(average_speed),2) AS avg_speed,
    ROUND(AVG(congestion_score),2) AS avg_congestion_score,
    ROUND(AVG(average_wait_time),2) AS avg_wait_minutes,
    ROUND(AVG(emission_estimate),2) AS avg_emission_estimate,
    ROUND(AVG(fuel_waste_estimate),2) AS avg_fuel_waste,
    ROUND(100.0 * AVG(accident_reported),2) AS accident_rate_pct
FROM smart_city_traffic_mobility;

-- 4. Congestion by city zone
SELECT city_zone,
       COUNT(*) AS records,
       ROUND(AVG(congestion_score),2) AS avg_congestion,
       ROUND(AVG(average_speed),2) AS avg_speed,
       ROUND(AVG(average_wait_time),2) AS avg_wait,
       ROUND(AVG(emission_estimate),2) AS avg_emission
FROM smart_city_traffic_mobility
GROUP BY city_zone
ORDER BY avg_congestion DESC;

-- 5. Congestion by road type
SELECT road_type,
       COUNT(*) AS records,
       ROUND(AVG(congestion_score),2) AS avg_congestion,
       ROUND(AVG(average_speed),2) AS avg_speed,
       ROUND(AVG(traffic_flow_rate),2) AS avg_flow,
       ROUND(AVG(emission_estimate),2) AS avg_emission
FROM smart_city_traffic_mobility
GROUP BY road_type
ORDER BY avg_congestion DESC;

-- 6. Hourly congestion profile
SELECT hour,
       ROUND(AVG(congestion_score),2) AS avg_congestion,
       ROUND(AVG(average_speed),2) AS avg_speed,
       ROUND(AVG(average_wait_time),2) AS avg_wait,
       ROUND(AVG(traffic_flow_rate),2) AS avg_flow
FROM smart_city_traffic_mobility
GROUP BY hour
ORDER BY hour;

-- 7. Peak-period performance
SELECT peak_period,
       COUNT(*) AS records,
       ROUND(AVG(congestion_score),2) AS avg_congestion,
       ROUND(AVG(average_speed),2) AS avg_speed,
       ROUND(AVG(average_wait_time),2) AS avg_wait,
       ROUND(AVG(emission_estimate),2) AS avg_emission
FROM smart_city_traffic_mobility
GROUP BY peak_period
ORDER BY avg_congestion DESC;

-- 8. Rush-hour impact
SELECT
    CASE WHEN rush_hour = 1 THEN 'Rush Hour' ELSE 'Non-Rush Hour' END AS period,
    COUNT(*) AS records,
    ROUND(AVG(congestion_score),2) AS avg_congestion,
    ROUND(AVG(average_speed),2) AS avg_speed,
    ROUND(AVG(average_wait_time),2) AS avg_wait,
    ROUND(AVG(emission_estimate),2) AS avg_emission
FROM smart_city_traffic_mobility
GROUP BY rush_hour
ORDER BY rush_hour;

-- 9. Accident impact
SELECT
    CASE WHEN accident_reported = 1 THEN 'Accident' ELSE 'No Accident' END AS accident_status,
    COUNT(*) AS records,
    ROUND(AVG(congestion_score),2) AS avg_congestion,
    ROUND(AVG(average_speed),2) AS avg_speed,
    ROUND(AVG(average_wait_time),2) AS avg_wait
FROM smart_city_traffic_mobility
GROUP BY accident_reported;

-- 10. Weather impact
SELECT weather_condition,
       COUNT(*) AS records,
       ROUND(AVG(congestion_score),2) AS avg_congestion,
       ROUND(AVG(average_speed),2) AS avg_speed,
       ROUND(AVG(average_wait_time),2) AS avg_wait
FROM smart_city_traffic_mobility
GROUP BY weather_condition
ORDER BY avg_congestion DESC;

-- 11. Road-condition impact
SELECT road_condition,
       COUNT(*) AS records,
       ROUND(AVG(congestion_score),2) AS avg_congestion,
       ROUND(AVG(average_speed),2) AS avg_speed,
       ROUND(AVG(average_wait_time),2) AS avg_wait,
       ROUND(AVG(emission_estimate),2) AS avg_emission
FROM smart_city_traffic_mobility
GROUP BY road_condition
ORDER BY avg_congestion DESC;

-- 12. Weekend vs weekday
SELECT
    CASE WHEN is_weekend = 1 THEN 'Weekend' ELSE 'Weekday' END AS day_type,
    COUNT(*) AS records,
    ROUND(AVG(congestion_score),2) AS avg_congestion,
    ROUND(AVG(average_speed),2) AS avg_speed,
    ROUND(AVG(average_wait_time),2) AS avg_wait,
    ROUND(AVG(traffic_flow_rate),2) AS avg_flow
FROM smart_city_traffic_mobility
GROUP BY is_weekend;

-- 13. Top 15 congestion hotspots
SELECT intersection_id,
       city_zone,
       ROUND(AVG(congestion_score),2) AS avg_congestion,
       ROUND(AVG(average_wait_time),2) AS avg_wait,
       ROUND(AVG(traffic_flow_rate),2) AS avg_flow,
       SUM(accident_reported) AS accident_events,
       ROUND(AVG(emission_estimate),2) AS avg_emission
FROM smart_city_traffic_mobility
GROUP BY intersection_id, city_zone
ORDER BY avg_congestion DESC
LIMIT 15;

-- 14. High-congestion observations
SELECT *
FROM smart_city_traffic_mobility
WHERE congestion_level IN ('High','Severe')
ORDER BY congestion_score DESC;

-- 15. Congestion share by level
SELECT congestion_level,
       COUNT(*) AS records,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),2) AS pct_of_records
FROM smart_city_traffic_mobility
GROUP BY congestion_level
ORDER BY records DESC;

-- 16. Traffic density vs congestion correlation (PostgreSQL)
SELECT ROUND(CORR(traffic_density, congestion_score)::numeric,3)
       AS density_congestion_correlation
FROM smart_city_traffic_mobility;

-- 17. Vehicle volume vs congestion correlation
SELECT ROUND(CORR(vehicle_count, congestion_score)::numeric,3)
       AS vehicle_congestion_correlation
FROM smart_city_traffic_mobility;

-- 18. Speed vs congestion correlation
SELECT ROUND(CORR(average_speed, congestion_score)::numeric,3)
       AS speed_congestion_correlation
FROM smart_city_traffic_mobility;

-- 19. Operational risk: accident + severe congestion
SELECT city_zone,
       COUNT(*) AS severe_accident_records,
       ROUND(AVG(average_wait_time),2) AS avg_wait
FROM smart_city_traffic_mobility
WHERE accident_reported = 1
  AND congestion_level = 'Severe'
GROUP BY city_zone
ORDER BY severe_accident_records DESC;

-- 20. Sensor quality monitoring
SELECT iot_sensor_health,
       COUNT(*) AS records,
       ROUND(AVG(traffic_flow_rate),2) AS avg_flow,
       ROUND(AVG(congestion_score),2) AS avg_congestion
FROM smart_city_traffic_mobility
GROUP BY iot_sensor_health;
