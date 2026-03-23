# Open-Source WMS Research for Warehouse Optimization

## Purpose
This document evaluates open-source warehouse management system (WMS) options for the Warehouse Optimization project.

The goal is not just to find a WMS with warehouse features. The goal is to find a system that helps this project ingest both:
- warehouse / operational data
- sales / order data

That matters because this product is intended to detect how warehouse needs change over time and use that to drive route and layout recommendations.

## What This Project Actually Needs
Based on the outline, PRD, architecture, and current CSV ingestion direction, the WMS side of this project should ideally provide:

### Required capabilities
- access to warehouse operations data
- access to sales or order demand data
- stable APIs or export paths
- support for historical data retrieval
- enough structure to map orders, products, stock movement, and warehouse locations
- practical self-hosting or sandboxability for development

### Strongly preferred capabilities
- open-source core
- active maintenance
- Python-friendly or straightforward integration path
- REST API or documented integration model
- ability to model multiple warehouses, locations, and stock movement
- enough ecosystem maturity that we are not building around an abandoned niche tool

### Important product-level constraint
For this project, the WMS should be treated as a data source and operational system of record, not the place where the optimization product itself lives.

That means our architecture should remain adapter-based:
- our product ingests from the WMS
- normalizes the data
- runs optimization
- outputs recommendations and KPI views

We should avoid tightly coupling the optimizer to one WMS implementation too early.

## Candidates Reviewed

### 1. ERPNext
Repo: `frappe/erpnext`
- GitHub stars: ~32k
- Primary language: Python
- License: GPL-3.0
- Recently updated

Why it is relevant:
- broad ERP platform with stock, inventory, sales, purchasing, and operations data
- much stronger business process coverage than a narrow warehouse-only tool
- good candidate if we want both warehouse context and sales/order context in one open-source platform

Strengths:
- likely the best fit for combining sales + warehouse data in one system
- Python ecosystem alignment is favorable for this repo
- large community and active development
- strong chance of usable APIs and structured entities for orders, products, warehouses, and stock movements

Weaknesses:
- it is an ERP first, not a specialized best-in-class WMS
- could bring more system complexity than needed if we only want warehouse telemetry + orders
- integration surface may be broad enough that scoping discipline matters

Best use in this project:
- strongest candidate if we want an open-source system to serve as a realistic upstream source for both sales and warehouse data
- very good as a reference integration target for MVP and demos

### 2. Odoo
Repo: `odoo/odoo`
- GitHub stars: ~49k
- Primary language: Python
- License: mixed / "Other" on GitHub (important licensing nuance)
- Recently updated

Why it is relevant:
- strong inventory app, sales modules, and broad business coverage
- widely used and likely practical in real businesses

Strengths:
- mature ecosystem
- broad operational coverage across sales, inventory, procurement, and accounting
- likely easier to find users, examples, and deployment knowledge for than smaller WMS projects
- supports routes, picking strategies, replenishment logic, and warehouse processes

Weaknesses:
- licensing/commercial packaging nuance is less clean than a straightforward permissive or copyleft OSS choice
- product complexity is high
- more of a business platform than a focused warehouse optimization integration target

Best use in this project:
- good real-world integration target
- not my first recommendation for the project’s anchor open-source WMS if we want a cleaner OSS story and simpler architecture decisions

### 3. OpenBoxes
Repo: `openboxes/openboxes`
- GitHub stars: ~834
- Primary language: Groovy
- License: EPL-1.0
- Recently updated

Why it is relevant:
- purpose-built supply chain / inventory system with explicit warehouse and stock movement focus
- active product site and current releases

Strengths:
- more warehouse-specific than broad ERP suites
- explicit support for inventory, shipments, stock movement, cycle counts, and multi-facility visibility
- likely a good source of operational warehouse events and inventory flows

Weaknesses:
- healthcare and distribution roots may bias the model toward inventory control rather than commercial sales + warehouse analytics
- less ideal if we want rich native sales-order context inside the same platform
- smaller ecosystem than ERPNext/Odoo
- Groovy/Grails stack is less aligned with our Python repo

Best use in this project:
- good candidate if the product later focuses more on warehouse operations than upstream sales integration
- not the best single-system choice if sales data is central to optimization

### 4. OpenWMS
Repo: `openwms/org.openwms`
- GitHub stars: ~669
- Primary language: Java
- License: Apache-2.0
- Recently updated

Why it is relevant:
- highly technical warehouse management system with a microservice architecture
- explicitly designed to interact with ERP systems and lower-level automation / material flow systems

Strengths:
- architecturally serious
- strong fit if the target environment is industrial automation-heavy
- conceptually compatible with event-driven warehouse systems and complex device interactions

Weaknesses:
- likely too heavyweight and infrastructure-intensive for this project’s MVP
- better for deep warehouse systems engineering than for quick product iteration
- may be overkill for the current CSV/sales/optimization product path
- Java/Spring microservice complexity does not match the current repo stage

Best use in this project:
- strong architectural reference
- probably not the best first implementation target

### 5. GreaterWMS
Repo: `GreaterWMS/GreaterWMS`
- GitHub stars: ~4.2k
- Primary language: Python
- License: Apache-2.0
- Recently updated

Why it is relevant:
- open-source WMS with stronger Python alignment than some alternatives
- appears oriented around warehousing workflows rather than broad ERP functions

Strengths:
- Python-friendly ecosystem alignment
- stronger warehouse focus than general ERP platforms
- active project and decent community interest

Weaknesses:
- product direction appears to be evolving significantly, including rewrites / framework changes
- repository messaging suggests architectural transition and reconstruction, which adds execution risk
- less proven than ERPNext or Odoo as a broad source of both sales and warehouse business data

Best use in this project:
- interesting candidate for warehouse-specific integration experiments
- not my first choice as the main reference platform for the product

## Comparison by Project Fit

### Best if we want both sales and warehouse data in one open-source system
1. **ERPNext**
2. **Odoo**
3. OpenBoxes
4. GreaterWMS
5. OpenWMS

### Best if we want a warehouse-specific operational system
1. **OpenBoxes**
2. **GreaterWMS**
3. OpenWMS
4. ERPNext
5. Odoo

### Best fit for our current Python-heavy MVP repo
1. **ERPNext**
2. **GreaterWMS**
3. Odoo
4. OpenBoxes
5. OpenWMS

### Best fit for long-term product realism without overcomplicating the MVP
1. **ERPNext**
2. **OpenBoxes**
3. Odoo
4. GreaterWMS
5. OpenWMS

## Recommendation

## Primary recommendation: ERPNext
If we want one open-source upstream system that can provide both:
- warehouse/inventory context
- sales/order context

then **ERPNext is the best fit for this project right now**.

Why:
- it aligns well with the product requirement to incorporate sales data over time
- it is active and widely used
- it is Python-based, which fits our repo and likely simplifies integration work
- it avoids forcing us into a warehouse-only tool that then still needs a second system for sales context

In other words:
- if the optimizer needs to learn from changing demand, order mix, throughput, and stock movement,
- ERPNext gives us a more complete business data surface than warehouse-only tools.

## Secondary recommendation: OpenBoxes
If the product direction shifts toward:
- warehouse operations first
- inventory movement first
- less dependence on upstream sales process data

then **OpenBoxes** becomes a very reasonable second choice.

It looks more warehouse-native than ERPNext, but less ideal as a single source for both sales and warehouse demand signals.

## Not recommended as the first anchor target
- **OpenWMS**: too heavy and infrastructure-rich for MVP
- **GreaterWMS**: interesting, but architecture/product direction seems less stable
- **Odoo**: powerful, but I’d prefer ERPNext first for cleaner fit and OSS simplicity in this project

## Architectural Recommendation for the Repo
Even if we choose ERPNext as the first target, we should not hard-code the system around ERPNext-specific models.

Recommended pattern:
- `wms/adapters/base.py` — abstract adapter interface
- `wms/adapters/csv.py` — current CSV ingestion path
- `wms/adapters/erpnext.py` — first real system adapter
- optional later adapters:
  - `wms/adapters/openboxes.py`
  - `wms/adapters/odoo.py`

Canonical internal data models should represent:
- orders
- order lines
- products/SKUs
- warehouse locations/zones
- stock movement
- forklift/device telemetry
- operational events

This lets us combine:
- WMS sales/order data
- warehouse movement data
- forklift trajectory/state CSV data

without tying the optimization engine to one vendor/system.

## Practical Next Step
The next best engineering move is:
1. create a **WMS integration strategy doc** in the repo,
2. define **canonical internal entities** for orders, products, stock movement, and telemetry,
3. keep the current CSV ingestion path as one adapter,
4. target **ERPNext as the first real WMS integration**.

## Bottom Line
If you want a single open-source system that best supports this project’s need to combine warehouse data with sales data over time:

**Pick ERPNext as the first WMS integration target.**

If you want the most warehouse-specialized operational system instead:

**Keep OpenBoxes as the backup/secondary target.**
