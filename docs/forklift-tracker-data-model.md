# Forklift Tracker Data Model

Purpose: Define the forklift tracker CSV inputs needed for the Power BI MVP.

## Current dashboard scope

For now, the reporting MVP is limited to:
1. top-selling items by outbound quantity
2. most-used forklifts

That means the project uses two different data families:
- warehouse movement export -> sales/outbound reporting
- forklift tracker files -> forklift usage reporting

## Forklift tracker input files

### 1. Tracker master file
File pattern:
- `GR FL Tracker Units Case Study D.csv`

Purpose:
- lists forklift tracker device IDs
- provides the set of known units/devices for the case study
- acts as the device master / lookup file

Expected use in MVP:
- build `dim_forklift`
- validate which device trajectory and state files should exist

### 2. Trajectory file per device
File pattern:
- `<device_id>.csv`
- example: `gr-fl-v3-0033.csv`

Purpose:
- 1Hz position and orientation data for a forklift tracker device

Format:
- `device_id,timestamp,x,y,z,q_x,q_y,q_z,q_w,std_x,std_y,std_z,std_R,std_P,std_Y`

Meaning:
- position: `x,y,z`
- orientation: quaternion `q_x,q_y,q_z,q_w`
- uncertainty: `std_x,std_y,std_z,std_R,std_P,std_Y`

Important quality rule:
- if `sqrt(std_x^2 + std_y^2)` is very high (>2 to 3m), the point may be bad data

### 3. Device state file per device
File pattern:
- `<device_id>_STATE.csv`
- example: `gr-fl-v3-0033_STATE.csv`

Purpose:
- device readiness and beacon context
- load/pallet beacon detection
- driver beacon detection

Format:
- `device_id,timestamp,ready,load_beacon_timestamp,load_beacon_minor_id,load_beacon_tx_power,driver_beacon_timestamp_1,driver_beacon_minor_id_1,driver_beacon_rssi_1,...`

Meaning:
- `ready` indicates readiness/active state
- load beacon fields indicate possible pallet/load context
- driver beacon fields indicate nearby driver beacon detections

## Power BI use of forklift files

### MVP usage metrics
For now, forklift usage should be derived from tracker files, not from warehouse movement rows.

Recommended first metrics:
- active point count
- ready-state count
- total distance traveled from valid trajectory points
- load-detected count
- driver-detected count
- percentage of valid positioning points

## Derived data quality fields

### position_uncertainty_2d
Formula:
- `sqrt(std_x^2 + std_y^2)`

### valid_position_flag
Rule:
- `true` when `position_uncertainty_2d <= threshold`
- threshold should be configurable, defaulting to 2.5m for MVP

### distance_increment
Rule:
- distance between consecutive valid points for the same device

## Power BI-ready summary output

Recommended summary table:
- `fact_forklift_usage_summary`

Suggested fields:
- device_id
- total_points
- valid_points
- valid_point_ratio
- ready_points
- load_detect_count
- driver_detect_count
- total_distance_m
- first_seen_ts
- last_seen_ts

## Current implementation direction

The warehouse export ingestion remains useful for sales reporting.
The forklift tracker ingestion should now be added as a parallel pipeline for usage reporting.
