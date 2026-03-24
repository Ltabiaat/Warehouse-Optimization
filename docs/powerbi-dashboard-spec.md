# Power BI Dashboard Spec

Project: Warehouse dashboard MVP
Current scope:
1. what has the most sales
2. which forklift is being used the most

## Dashboard principle

Keep the first dashboard simple and defensible.
Do not imply we have revenue if we only have outbound quantity.
Do not imply exact utilization if we only have tracker-based proxy metrics.

## Data sources

### Sales source
File:
- `warehouse_mvp/output/sales_summary.csv`

Definition:
- Sales is currently defined as outbound quantity from the warehouse movement export.

Key fields:
- `item_code`
- `item_name`
- `total_qty_out`
- `outbound_event_count`
- `distinct_clients`
- `distinct_locations`

### Forklift usage source
File:
- `warehouse_mvp/output/forklift_usage_summary.csv`

Definition:
- Forklift usage is currently defined using tracker trajectory and state data.

Key fields:
- `device_id`
- `total_points`
- `valid_points`
- `valid_point_ratio`
- `total_distance_m`
- `ready_points`
- `load_detect_count`
- `driver_detect_count`
- `first_seen_ts`
- `last_seen_ts`

## Page 1: Top-selling items

### Goal
Show which items have the highest outbound quantity.

### Recommended visuals

#### Visual 1: Bar chart
Title:
- Top Items by Outbound Quantity

Axis:
- `item_name` (or `item_code` if names are unreliable)

Values:
- `total_qty_out`

Sort:
- descending by `total_qty_out`

#### Visual 2: Table
Columns:
- `item_code`
- `item_name`
- `total_qty_out`
- `outbound_event_count`
- `distinct_clients`
- `distinct_locations`

### Recommended KPI card
- Total Outbound Quantity = sum of `total_qty_out`

## Page 2: Most-used forklifts

### Goal
Show which forklifts appear most used based on tracker data.

### Recommended visuals

#### Visual 1: Bar chart
Title:
- Forklifts by Distance Traveled

Axis:
- `device_id`

Values:
- `total_distance_m`

Sort:
- descending by `total_distance_m`

#### Visual 2: Bar chart
Title:
- Forklifts by Ready-State Count

Axis:
- `device_id`

Values:
- `ready_points`

#### Visual 3: Table
Columns:
- `device_id`
- `total_distance_m`
- `ready_points`
- `load_detect_count`
- `driver_detect_count`
- `valid_point_ratio`
- `first_seen_ts`
- `last_seen_ts`

### Recommended KPI cards
- Total Distance Traveled = sum of `total_distance_m`
- Average Valid Point Ratio = average of `valid_point_ratio`

## Labeling guidance

Use labels carefully:
- say **Top-selling items (by outbound quantity)** instead of implying revenue
- say **Most-used forklifts (by distance / ready-state activity)** instead of implying exact utilization

## Import flow

1. import `sales_summary.csv`
2. import `forklift_usage_summary.csv`
3. set numeric field types properly in Power BI
4. build visuals directly from summary tables

## Nice-to-have later
- date filtering once time-grain summary tables are added
- trend charts over time
- device master join from tracker master file
- operator/driver cross-analysis if beacon identity mapping becomes available
