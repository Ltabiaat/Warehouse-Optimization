# ERPNext Integration Plan

## Purpose
This document defines how the Warehouse Optimization project should integrate with ERPNext as the first real WMS / ERP data source.

The goal is to validate the product idea quickly by combining:
- sales and order demand data from ERPNext
- inventory and warehouse context from ERPNext
- forklift telemetry CSV data from local tracker exports

## Why ERPNext First
ERPNext is the best first integration target for this project because it can provide both:
- sales-side demand signals
- warehouse and stock-side operational signals

That makes it a good system for validating whether changing demand patterns can drive better warehouse route and layout recommendations.

## Integration Principles
- ERPNext is the first adapter, not the permanent center of the architecture.
- Internal models must stay vendor-neutral.
- CSV telemetry ingestion remains a parallel input path.
- The optimization engine should consume normalized internal entities, not raw ERPNext responses.

## Data Domains We Need from ERPNext

### 1. Sales / Demand
These entities help us understand what demand is changing over time.

Needed concepts:
- sales orders
- sales order lines
- item / SKU references
- order dates and fulfillment timing
- ordered quantities
- customer or order class (optional later)

Questions to answer with this data:
- which items are moving more often?
- which item mixes are changing over time?
- what demand patterns may justify layout changes?

### 2. Warehouse / Inventory Context
These entities help us understand the physical and stock context in which demand is being served.

Needed concepts:
- warehouses
- storage locations / bins if available
- stock balances
- stock movement / inventory transactions
- item master data

Questions to answer with this data:
- where is stock stored?
- how are items moving between warehouse states?
- which areas are likely high traffic based on demand and replenishment patterns?

### 3. Operational Time Context
This helps us align ERPNext records with telemetry.

Needed concepts:
- document timestamps
- posting dates / transaction times
- status transitions
- time windows for fulfillment and stock movement

Questions to answer with this data:
- can we relate periods of high item movement to forklift movement patterns?
- can we detect recurring operational bottlenecks by time window?

## Proposed Internal Canonical Entities
The optimizer should not depend on ERPNext-specific field names. Instead, we normalize ERPNext data into these internal entities:

- `Product`
- `WarehouseSite`
- `StorageLocation`
- `SalesOrder`
- `SalesOrderLine`
- `InventoryBalance`
- `StockMovement`
- `DemandSnapshot`

These entities will later allow additional adapters for other WMS systems.

## Proposed Adapter Structure

```text
src/warehouse_optimization/wms/
├── adapters/
│   ├── __init__.py
│   ├── base.py
│   ├── csv.py
│   └── erpnext.py
├── models.py
└── erpnext_models.py
```

### Adapter responsibilities
- `base.py`
  - defines the abstract WMS adapter contract
- `csv.py`
  - handles local CSV fixture ingestion and later real tracker file ingestion
- `erpnext.py`
  - handles ERPNext API interactions and normalization
- `models.py`
  - canonical internal warehouse / sales entities
- `erpnext_models.py`
  - raw ERPNext-oriented request/response mapping helpers where useful

## Suggested First ERPNext Scope
For MVP validation, keep the ERPNext scope narrow.

### Phase 1
Pull and normalize:
- products/items
- warehouses
- sales orders
- sales order lines

### Phase 2
Add:
- inventory balances
- stock ledger / stock movement records

### Phase 3
Join with local telemetry data:
- forklift trajectory data
- forklift state / beacon data
- time-window aggregations

## Suggested Initial Output for the Product
Once ERPNext data is normalized, the first useful derived outputs are:
- item demand by time period
- top-moving SKUs
- demand concentration by warehouse zone or mapped storage area
- candidate high-traffic paths inferred from sales + stock movement + forklift traces
- recommendations for layout review when demand patterns drift

## MVP Integration Strategy
1. Define canonical internal models.
2. Build an abstract adapter interface.
3. Implement an ERPNext adapter skeleton.
4. Build fixture-based tests against normalized entities.
5. Add real ERPNext connectivity only after internal models are stable.

## Open Questions
- Which exact ERPNext doctypes should be treated as the source of truth for stock movement?
- How much location granularity is available in the target ERPNext environment?
- Will warehouse zones need to be maintained separately from ERPNext?
- How will telemetry devices map to warehouse sites, areas, or forklifts in ERPNext?
- What time windows should be used for demand snapshots in optimization runs?

## Recommendation
Proceed with an ERPNext-first architecture, but keep the core models and optimization logic vendor-neutral.
