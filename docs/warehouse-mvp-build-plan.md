# Warehouse MVP Build Plan

## Objective

Validate the warehouse optimization idea using the available movement-event dataset before investing in full ERPNext integration or broader warehouse modeling.

## Scope

### In scope
- translate and normalize the current warehouse movement export
- create a clean movement-event fact table
- derive simple dimensions for item, location, operator, and client
- produce baseline KPIs
- build simple heuristic prioritization logic
- define lightweight simulator assumptions

### Out of scope for MVP
- real-time ERPNext integration
- exact route optimization
- full order-level orchestration
- precise labor scheduling
- closed-loop warehouse automation

## Workstreams

### 1. Data modeling
Deliverables:
- data dictionary
- normalized event schema
- field mapping rules

### 2. Data ingestion
Deliverables:
- raw CSV ingestion path
- cleaning rules
- timestamp normalization
- quantity normalization

### 3. Baseline analytics
Deliverables:
- movement volume by item/location/operator
- in/out trend summaries
- simple dwell/velocity proxies
- perishable stock risk indicators if expiry is reliable

### 4. Heuristic MVP
Deliverables:
- simple prioritization heuristic based on recency, movement volume, expiry pressure, and location grouping
- transparent scoring formula

### 5. Documentation
Deliverables:
- process documentation updates
- Google Doc sync checkpoints

## Recommended immediate coding order

1. create the normalized schema and data dictionary
2. build a parser/cleaner for the export
3. generate an analysis-ready table
4. define 3-5 baseline KPIs
5. implement one simple prioritization heuristic
6. review whether the signal looks useful before building simulation/RL

## Decision rule

If the cleaned dataset cannot support a meaningful baseline heuristic or useful operational insight, stop before building the RL layer.
That is a successful MVP outcome too because it prevents wasted engineering.
