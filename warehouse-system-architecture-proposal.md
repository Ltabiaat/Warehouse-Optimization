# Warehouse Optimization System Proposal

Prepared for: Lancelot Tabiaat  
Date: 2026-03-20  
Author: Squire

## 1. Goal

Design a practical, policy-safe system for warehouse optimization that combines:
- an open-source warehouse management system (WMS) as the operational source of truth
- a Gymnasium-based reinforcement learning environment for optimization experimentation and decision support
- Power BI for business-facing reporting and operational dashboards

The goal is not to let an RL agent directly control a live warehouse on day one. The safer and more realistic path is:
1. capture operational data from the WMS
2. build a simulation environment that reflects warehouse flows
3. train and evaluate RL policies offline
4. expose recommendations and KPIs through dashboards
5. optionally move toward human-in-the-loop decision support before any live automation

## 2. Recommended System Shape

### Core principle
Treat the WMS as the operational system of record, the RL layer as an optimization engine, and Power BI as the decision interface.

### Recommended high-level architecture
1. Open-source WMS
   - stores inventory, locations, pick tasks, stock moves, replenishment events, orders, shipments, and operator activity
2. Data extraction / integration layer
   - pulls WMS events and master data via API, database replica, or scheduled exports
3. Operational data store / feature layer
   - cleans and standardizes warehouse data for analytics and simulation input
4. Gymnasium simulation environment
   - models warehouse state, actions, rewards, and transition logic
5. RL training + evaluation pipeline
   - trains agents offline and compares them against rules-based baselines
6. Recommendation service
   - generates suggested routing, task assignment, slotting, batching, or replenishment decisions
7. Power BI dashboards
   - shows KPIs, scenario comparisons, bottlenecks, and model-vs-baseline outcomes
8. Human approval / operations review loop
   - warehouse operators or managers review recommendations before operational adoption

## 3. Best Open-Source WMS Candidates

### Option A: Odoo Inventory / WMS
Best if you want:
- a broad, mature business system
- inventory, routes, replenishment, multi-step receiving/shipping, putaway, cycle counts, reporting
- a platform that can later connect to purchasing, sales, and manufacturing workflows

Why it fits:
- Odoo documents support for replenishment, routes, warehouses, locations, inventory adjustments, cycle counts, reporting, and multi-step shipping/receiving flows.
- That makes it a realistic event source for warehouse simulation and optimization.

Tradeoffs:
- modular, but can grow complex
- customization discipline matters

### Option B: ERPNext Inventory / Stock
Best if you want:
- a more ERP-oriented open-source stack with solid inventory/stock foundations
- a Python-friendly environment that some teams find easier to self-host and adapt

Tradeoffs:
- depending on the exact warehouse complexity, you may need more custom workflow logic than with a richer WMS-first setup

### Current project decision
For this project, the selected initial WMS is:
- **ERPNext Inventory / Stock**

Reason:
- start with a single practical open-source system of record now
- keep the first implementation path focused and easier to execute
- leave room to add broader capabilities or alternative WMS layers later if needed

## 4. What the RL Layer Should Actually Optimize

Do not start by trying to optimize everything at once.

### Strong first use cases
1. Pick path / routing optimization
   - reduce travel distance and time
2. Task prioritization
   - choose which picks, putaways, or replenishment tasks should be executed first
3. Batch / wave grouping
   - cluster orders to improve throughput
4. Slotting recommendations
   - place high-frequency items in better locations
5. Replenishment timing support
   - recommend replenishment timing to reduce stockouts and congestion

### Best MVP target
Start with:
- **pick routing + task prioritization**

Why:
- measurable impact
- easier to simulate than full warehouse autonomy
- easier to compare against heuristics or human rules

## 5. Gymnasium-Based RL Design

Gymnasium is a maintained RL environment API and is a good fit for representing warehouse state/action/reward loops in Python.

### Environment design
Your custom Gymnasium environment should define:

#### Observation space
Examples:
- current warehouse zone occupancy
- picker location(s)
- pending picks / orders
- SKU locations
- task backlog
- travel distances
- current inventory levels
- congestion indicators
- replenishment status
- time remaining for urgent orders

#### Action space
Examples:
- next task assignment
- next aisle/zone routing decision
- batch selection choice
- replenishment trigger decision
- slotting recommendation action

#### Reward function
Examples:
- positive reward for completed picks/orders
- penalty for long travel distance
- penalty for delayed urgent orders
- penalty for congestion or unnecessary movement
- penalty for stockout or replenishment failure
- optional reward for balance across workers or zones

#### Episode design
Examples:
- one shift
- one day of operations
- one order wave
- one warehouse scenario replay

### Important design rule
Build the simulation from **real warehouse event patterns**, not toy assumptions. Otherwise the RL agent may optimize the wrong thing.

## 6. Data Pipeline Recommendation

### Ingestion layer
Possible sources from the WMS:
- orders
- stock moves
- inventory snapshots
- pick tickets / transfer records
- replenishment events
- operator actions
- timestamps by step
- location master data
- SKU metadata

### Processing layer
Use Python pipelines to:
- validate records
- normalize timestamps and location IDs
- derive movement paths and task durations
- engineer features for simulation and reporting
- store training datasets and scenario snapshots

### Storage options
For MVP:
- PostgreSQL for structured warehouse and simulation data
- parquet files or object storage for training datasets and logs

### Orchestration
Good options:
- simple cron/Airflow/Prefect style scheduling
- dbt optional if analytics transformations grow

## 7. Power BI Role

Power BI should not be the optimization engine. It should be the business-facing lens.

### Best use of Power BI here
1. Operations dashboard
   - throughput
   - order aging
   - average pick time
   - distance proxy metrics
   - stockout risk
   - replenishment backlog
2. Optimization dashboard
   - baseline vs RL comparison
   - route efficiency changes
   - time saved
   - service-level improvements
   - simulation scenario results
3. Executive dashboard
   - cost impact
   - productivity impact
   - warehouse utilization trends
   - operational bottlenecks by area/time

### Important Power BI constraint
Power BI is excellent for dashboards, but model training and core simulation should stay in Python/data infrastructure rather than being embedded into Power BI logic.

## 8. Recommended MVP Architecture

### Phase 1: Data foundation
- use ERPNext as the initial WMS
- define warehouse entities and event schema
- build extraction pipeline into PostgreSQL
- establish baseline operational KPIs

### Phase 2: Simulation layer
- create Gymnasium environment from historical warehouse data
- implement heuristic baselines:
  - nearest-task rule
  - priority-based queueing
  - simple batch heuristics
- validate simulation realism with stakeholders

### Phase 3: RL experimentation
- train RL agent offline
- compare against heuristics across historical or synthetic scenarios
- evaluate stability, not just best-case performance

### Phase 4: Decision-support product
- produce recommended actions or scenario outputs
- send outputs to a reviewed recommendation table/API
- display results in Power BI
- keep a human in the loop

### Phase 5: Limited operational rollout
- start with advisory mode only
- measure whether recommendations outperform existing process
- only consider automation after repeated safe wins

## 9. Suggested Tech Stack

### Core platform
- **WMS:** ERPNext Inventory / Stock
- **Backend / data services:** Python
- **RL environment:** Gymnasium
- **RL libraries:** Stable-Baselines3 or Ray RLlib (depending on scale/experimentation needs)
- **Database:** PostgreSQL
- **Data processing:** Pandas / Polars as needed
- **Scheduling / orchestration:** cron, Prefect, or Airflow depending on complexity
- **Visualization:** Microsoft Power BI
- **Containerization:** Docker / Docker Compose for local or pilot deployment

## 10. API / Integration Strategy

Use official, documented integration patterns only.

Preferred order:
1. official WMS APIs
2. database read replica / controlled ETL
3. scheduled exports if APIs are too limited

Avoid:
- UI scraping
- browser automation against business systems as the primary integration path
- anything that looks like bypassing platform controls or terms

## 11. Policy-Safe / Terms-Safe Operating Approach

To stay on the safe side of platform and account policies:
- use OAuth and official APIs where available
- avoid browser automation against signed-in consumer tabs as the core operating model
- keep automation human-scale and transparent
- avoid scraping or anti-bot evasion
- prefer system-to-system integrations over pretending to be a human in the UI

This matters especially if Google Docs, Sheets, or dashboards are used in the surrounding workflow.

## 12. Risks

### Technical risks
- simulation does not reflect real warehouse operations closely enough
- reward function optimizes the wrong KPI
- poor historical data quality
- warehouse constraints are under-modeled
- model works in simulation but not in operations

### Organizational risks
- operators do not trust recommendations
- dashboards are interesting but not actionable
- no clear baseline comparison
- too much ambition too early

### Integration risks
- WMS customization grows too complex
- brittle connectors
- unclear event definitions across teams

## 13. What I Would Build First

If I were building this with you, I would do this in order:

1. Use ERPNext as the initial WMS
2. Define a warehouse event schema and KPI list
3. Build a simple extraction pipeline into PostgreSQL
4. Create a Gymnasium environment for one narrow use case:
   - pick routing or task prioritization
5. Build heuristic baselines first
6. Train an RL agent offline
7. Expose baseline-vs-agent comparisons in Power BI
8. Keep the first release firmly in decision-support mode

## 14. Deliverables for a Strong First Proposal

1. Architecture diagram
2. WMS entity model
3. Data pipeline spec
4. Gymnasium environment spec
5. Reward design draft
6. Baseline heuristics definition
7. KPI dashboard wireframe for Power BI
8. rollout plan from offline simulation to human-reviewed recommendations

## 15. Final Recommendation

The stack you are thinking about is directionally good.

My refined recommendation is:
- **Open-source WMS:** ERPNext Inventory / Stock
- **Optimization layer:** Python + Gymnasium custom environment
- **Modeling path:** offline RL with strong heuristic baselines
- **Reporting layer:** Power BI
- **Operating model:** human-in-the-loop recommendations first, not direct live control

That gives you a system that is technically credible, operationally safer, and easier to explain to stakeholders.

## Sources Used
- Gymnasium documentation: maintained RL environment API for Python
- ERPNext documentation for inventory/stock concepts and integration planning
- Microsoft Learn / Power BI documentation: Python package support and role of Power BI in analytics workflows
flows
