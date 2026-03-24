# Warehouse Event Schema MVP

Project: Warehouse optimization proof of concept
WMS direction: ERPNext-first
Purpose: Define the normalized event schema to build from the current source columns.

## MVP Goal

Use the provided warehouse movement export to test whether a useful optimization signal can be extracted before investing in a broader integration.

This MVP is intentionally narrow.
It prioritizes:
- event reconstruction
- descriptive analytics
- baseline heuristics
- lightweight simulation

It does not require a perfect digital twin.

## Recommended MVP Use Case

Primary use case:
- movement-event analysis and simple task-prioritization proxy modeling

Secondary use case:
- location-level flow analysis

Deferred until later:
- accurate route optimization
- worker path optimization
- full warehouse graph simulation
- live decision automation

## Normalized Event Table

Recommended table name:
- `fact_warehouse_event`

### Required fields

| Field | Type | Source | Description |
|---|---|---|---|
| event_id | string | derived | Stable unique event key |
| inventory_slip_no | string | 入出庫伝票№ | Transaction/slip group identifier |
| event_date | date | ﾀｲﾑｽﾀﾝﾌﾟ（日付） | Operational event date |
| event_time | string/time | ﾀｲﾑｽﾀﾝﾌﾟ（時間） | Operational event time |
| event_ts | timestamp | derived | Combined event datetime |
| transaction_date | date | 伝票日付 | Business transaction date |
| transaction_type | string | 取引区分略称 | Movement category |
| item_code | string | 商品コード | SKU/item identifier |
| lot_no | string | ロット№ | Lot/batch identifier |
| location_no | string | ロケーション№ | Location identifier |
| unit_name | string | 単位名 | Unit of measure |
| qty_in | numeric | 入庫数量 | Quantity moved in |
| qty_out | numeric | 出庫数量 | Quantity moved out |
| movement_qty | numeric | derived | Signed movement quantity |
| operator_code | string | 担当者コード | Operator identifier |
| client_id | string | クライアントＩＤ | Client/account identifier |

### Recommended optional fields

| Field | Type | Source | Description |
|---|---|---|---|
| item_name | string | 商品名１ | Product label |
| expiration_date | date | 消費期限 | Expiry for FEFO/perishables |
| receipt_date | date | 入荷日 | Receipt date |
| floor_code | string | フロアコード | Zone/floor grouping |
| qty_in_each | numeric | 入庫数（バラ） | Inbound each-level quantity |
| qty_out_each | numeric | 出庫数（バラ） | Outbound each-level quantity |
| operator_name | string | 担当者名 | Operator label |
| last_operator_code | string | 最終作業者コード | Final operator |
| vehicle_no | string | 車番 | Vehicle/loading identifier |
| data_ts | timestamp | data timestamp fields | System-recorded timestamp |
| program_name | string | プログラム名 | Source program/process |
| internal_notes | string | 社内備考 | Internal notes |
| remarks | string | 備考 | Remarks |
| pack_size_b | numeric/string | 入数B | Pack-size reference |

## Derived Fields

| Field | Logic | Reason |
|---|---|---|
| event_id | hash/slip+line/time/item/location | Stable event identity |
| event_ts | combine event_date + event_time | Primary time field |
| data_ts | combine data timestamp date + time | Audit/latency analysis |
| movement_qty | qty_in - qty_out | Single signed quantity field |
| movement_direction | if movement_qty > 0 then IN else OUT | Easier analytics |
| is_perishable | expiration_date is not null | Useful flag |
| location_group | floor_code or parsed location prefix | Useful fallback zone feature |

## Minimum Viable Dimensions

Even for a test, add small dimensions where possible:

### dim_item
- item_code
- item_name
- default_unit_name
- pack_size_b (if meaningful)
- is_perishable

### dim_location
- location_no
- floor_code
- location_group (derived if needed)

### dim_operator
- operator_code
- operator_name

### dim_client
- client_id

## What We Do NOT Need for This MVP

To test the core idea, we do not strictly need:
- full order hierarchy
- customer delivery promise times
- exact worker travel paths
- detailed warehouse graph geometry
- real-time API integration
- perfect ERPNext document mapping on day one

We can begin with a clean event-history model and still learn something useful.

## Workarounds for Missing Ideal Fields

### 1. No order context
Problem:
- Harder to optimize true pick priority by customer/order urgency

Workaround:
- Use transaction groups, timestamps, and item movement intensity as proxy signals
- Build a first model around movement volume and recency, not strict order urgency

Result:
- Good enough for proof-of-concept analytics and simple prioritization heuristics

### 2. No warehouse graph / travel distance
Problem:
- Hard to do real route optimization

Workaround:
- Use floor_code and location prefix/group as coarse spatial proxies
- Estimate travel cost using location changes rather than exact distances

Result:
- Enough for zone-level flow analysis, not enough for true route optimization

### 3. No explicit task table
Problem:
- Hard to simulate picker task queues directly

Workaround:
- Treat movement events as proxy tasks
- Group events by slip number, time window, operator, and location

Result:
- Enough for replay and baseline heuristics

### 4. No stock snapshot balance
Problem:
- Hard to reconstruct exact inventory state at all moments

Workaround:
- Rebuild approximate net position from movement history for selected items/locations
- Scope the MVP to movement patterns and relative ranking instead of exact inventory truth

Result:
- Acceptable for idea validation if framed honestly

### 5. No exact event completion duration
Problem:
- Hard to model task service time precisely

Workaround:
- Approximate duration from timestamp spacing between nearby events by the same operator
- Use simple constant-time or category-based heuristics where needed

Result:
- Good enough for baseline simulation, not for labor planning accuracy

### 6. No explicit source/destination location pair
Problem:
- Hard to model transfers cleanly

Workaround:
- Start with single-location event modeling
- Infer probable flows only where transaction types strongly imply inbound/outbound direction

Result:
- Fine for event analysis; transfer-path modeling deferred

## MVP Decision

For testing the idea, this dataset is sufficient if we frame the MVP correctly:
- not a full warehouse optimizer
- not a live control system
- yes for movement analytics
- yes for baseline prioritization heuristics
- yes for lightweight simulation assumptions

## Recommended Next Build Artifacts

1. Raw-to-normalized field mapping file
2. Example CSV header template
3. Bronze/silver/gold transformation spec
4. Baseline KPI list
5. Simple simulator assumptions doc
