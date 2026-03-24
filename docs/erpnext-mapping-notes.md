# ERPNext Mapping Notes

Purpose: Explain how the current warehouse export can fit an ERPNext-first architecture without pretending ERPNext already contains every ideal optimization field.

## Honest framing

For this MVP, ERPNext is the architectural direction.
The current warehouse export is the immediate test dataset.
Those are not the same thing, and that is okay.

We should treat the current file as:
- legacy/real-world operational evidence
- an MVP input dataset for testing the optimization idea
- a guide for what ERPNext-side entities and custom fields may matter later

## Mapping philosophy

Do not force a perfect 1:1 mapping too early.
Instead, map into three buckets:

1. ERPNext-native concepts
2. likely custom/extended concepts
3. optimization-only derived fields

## Likely ERPNext-native concepts

| Current field | ERPNext-like concept |
|---|---|
| item_code | Item / Item Code |
| item_name | Item Name |
| transaction_date | Posting Date / Transaction Date |
| inventory_slip_no | Stock Entry / Delivery Note / Purchase Receipt / inventory transaction reference |
| transaction_type | Stock movement type / voucher type / business transaction type |
| lot_no | Batch |
| expiration_date | Batch expiry / expiry date |
| receipt_date | Receipt-related posting/receipt date |
| location_no | Warehouse / Bin / storage location mapping |
| unit_name | UOM |
| qty_in / qty_out | Actual Qty / movement quantity |
| client_id | Customer/client/account reference depending on process |

## Likely extension/custom concepts

| Current field | Why it may need extension |
|---|---|
| floor_code | ERPNext may need a warehouse hierarchy or custom location taxonomy |
| operator_code | Worker/operator identity may live outside standard stock docs or require custom linkage |
| operator_name | Same as above |
| last_operator_code | Likely custom audit field |
| vehicle_no | Likely logistics/custom transport field |
| internal_notes / remarks | May map to remarks/custom text fields |
| pack_size_b | Depends on packaging/UOM modeling choice |

## Optimization-only derived concepts

These do not need to exist in ERPNext first:
- movement_qty
- event_ts
- data_ts
- movement_direction
- location_group
- event_id
- inferred_task_group
- estimated_service_time
- zone_transition_flag

These belong in the analytics/simulation layer.

## Practical MVP conclusion

We do not need perfect ERPNext conformance to test the concept.
For MVP, do this instead:
- treat the source export as the historical event layer
- normalize it into analytics tables
- design the ERPNext mapping in parallel
- delay strict ERPNext integration until the concept proves useful

That keeps the project honest and fast.
