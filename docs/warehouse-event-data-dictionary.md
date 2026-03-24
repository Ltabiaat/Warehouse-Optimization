# Warehouse Event Data Dictionary

Project: Warehouse optimization MVP
WMS direction: ERPNext-first
Purpose: Define a practical translation and retention policy for the source warehouse movement columns provided by Lancelot.

## Usage

This source dataset should be treated as the initial movement-event feed for MVP testing.
It is not the whole warehouse model.
It is the first operational table used to:
- reconstruct inventory movement events
- analyze operator activity
- derive simple location-level flows
- build baseline heuristics and a lightweight simulator

## Column Dictionary

| Japanese | Recommended English | Meaning | Keep Class | Notes |
|---|---|---|---|---|
| 商品コード | item_code | Product/SKU code | Core | Primary item identifier |
| 商品名１ | item_name | Product name | Optional | Useful for readability and reporting |
| 伝票日付 | transaction_date | Business transaction/slip date | Core | Use with event timestamps |
| 入出庫伝票№ | inventory_slip_no | Inventory in/out slip number | Core | Document/event grouping key |
| プログラム名 | program_name | Source program/process name | Optional | Useful for audit/debugging |
| 取引区分略称 | transaction_type | Transaction type abbreviation | Core | Important for event classification |
| ロット№ | lot_no | Lot/batch number | Core | Important for traceability |
| 入荷日 | receipt_date | Receipt/arrival date | Optional | Useful for FIFO/FEFO |
| 消費期限 | expiration_date | Expiration/use-by date | Core | Important if inventory is perishable |
| フロアコード | floor_code | Floor/zone code | Optional | Useful if multi-floor or zoned |
| ロケーション№ | location_no | Location number | Core | Key warehouse location field |
| 単位名 | unit_name | Unit of measure | Core | Required to interpret quantities |
| 入庫数量 | qty_in | Quantity moved in | Core | Core movement value |
| 出庫数量 | qty_out | Quantity moved out | Core | Core movement value |
| 入数B | pack_size_b | Pack/case size reference | Clarify | Keep only if it affects operational logic |
| 入庫数（バラ） | qty_in_each | Inbound quantity in individual units | Optional | Useful when cases and eaches mix |
| 出庫数（バラ） | qty_out_each | Outbound quantity in individual units | Optional | Useful when cases and eaches mix |
| ﾀｲﾑｽﾀﾝﾌﾟ（時間） | event_time | Event time | Core | Operational time |
| ﾀｲﾑｽﾀﾝﾌﾟ（日付） | event_date | Event date | Core | Operational date |
| 担当者コード | operator_code | Operator/staff code | Core | Needed for worker-level analysis |
| 担当者名 | operator_name | Operator/staff name | Optional | Readable label |
| 車番 | vehicle_no | Vehicle/truck number | Optional | Relevant for dispatch/load workflows |
| ﾃﾞｰﾀ・ﾀｲﾑｽﾀﾝﾌﾟ（日付） | data_timestamp_date | System-recorded data date | Optional | Useful to compare event time vs data-entry time |
| ﾃﾞｰﾀ･ﾀｲﾑｽﾀﾝﾌﾟ（時間） | data_timestamp_time | System-recorded data time | Optional | Useful to compare event time vs data-entry time |
| タイムスタンプ2桁 | timestamp_2digit | Derived timestamp helper | Drop for MVP | Likely formatting convenience only |
| タイムスタンプ4桁 | timestamp_4digit | Derived timestamp helper | Drop for MVP | Likely formatting convenience only |
| 社内備考 | internal_notes | Internal notes | Optional | Unstructured but may explain anomalies |
| 備考 | remarks | Remarks/notes | Optional | Unstructured but potentially useful |
| クライアントＩＤ | client_id | Client/account identifier | Core | Important for multi-client operations |
| 最終作業者コード | last_operator_code | Final/last operator code | Optional | Useful if distinct from operator_code |

## Keep Policy

### Core MVP fields
These should be retained in the first cleaned dataset:
- item_code
- transaction_date
- inventory_slip_no
- transaction_type
- lot_no
- expiration_date
- location_no
- unit_name
- qty_in
- qty_out
- event_date
- event_time
- operator_code
- client_id

### Strongly recommended optional fields
Keep these if present and reasonably clean:
- item_name
- receipt_date
- floor_code
- qty_in_each
- qty_out_each
- operator_name
- last_operator_code
- vehicle_no
- data_timestamp_date
- data_timestamp_time
- internal_notes
- remarks

### Drop for MVP
- timestamp_2digit
- timestamp_4digit

### Needs clarification
- pack_size_b
- difference between operator_code and last_operator_code
- difference between event timestamp and data timestamp

## Interpretation Notes

### event timestamp vs data timestamp
If both are available:
- `event_date` + `event_time` should represent when the warehouse action happened
- `data_timestamp_date` + `data_timestamp_time` should represent when the system recorded or updated the event

For MVP, keep both if available, but treat event timestamp as primary.

### qty_in / qty_out strategy
For normalization, prefer a single signed movement value later:
- movement_qty = qty_in - qty_out

But preserve the original columns in bronze/raw storage.

### notes fields
Do not rely on notes for core logic.
Use them only for:
- anomaly review
- debugging
- explainability

## Recommendation

This dataset is enough to test the idea for:
- inventory movement replay
- simple operator activity analysis
- simple location flow analysis
- a first baseline optimization prototype

It is not enough by itself for a full closed-loop warehouse optimizer.
That is fine for MVP testing.
