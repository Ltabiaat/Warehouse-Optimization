Warehouse Optimization Technical Architecture

1\. Purpose  
This document defines a technical architecture for the Warehouse Optimization system described in the PRD. The architecture is designed to support warehouse configuration, WMS integration, graph-based warehouse modeling, simulation and optimization workflows, KPI analytics, and a Power BI-facing reporting layer.

2\. Architecture Goals  
\- Support a clear flow from warehouse inputs to optimization outputs  
\- Separate data ingestion, modeling, optimization, and visualization concerns  
\- Allow periodic re-optimization as warehouse conditions evolve  
\- Keep the initial system practical to implement while leaving room for deeper simulation and analytics later  
\- Provide traceability between source data, optimization runs, and user-facing recommendations

3\. High-Level Architecture  
The system is composed of the following major layers:  
\- Configuration and input layer  
\- Data integration layer  
\- Core warehouse model layer  
\- Simulation and optimization layer  
\- Analytics and KPI layer  
\- Recommendation and output layer  
\- Visualization and user interface layer  
\- Scheduling and orchestration layer

4\. Logical Components  
4.1 Configuration Service  
Responsibilities:  
\- Capture warehouse metadata and setup information  
\- Store layout, dimensions, zones, constraints, and machinery definitions  
\- Manage WMS connection metadata  
\- Version configuration changes over time

Suggested inputs:  
\- Warehouse size and geometry  
\- Storage zones and pathways  
\- Dock locations  
\- Machinery inventory  
\- Operational assumptions

Outputs:  
\- Canonical warehouse configuration record  
\- Versioned configuration snapshots for modeling and optimization

4.2 WMS Integration Service  
Responsibilities:  
\- Connect to the WMS or export source  
\- Ingest relevant operational and sales data  
\- Normalize source data into a canonical schema  
\- Support scheduled refreshes and historical retention

Expected data domains:  
\- Orders  
\- SKUs or product categories  
\- Pick frequency  
\- Throughput metrics  
\- Inventory movement signals  
\- Time-windowed operational summaries

Outputs:  
\- Cleaned operational datasets  
\- Historical time-series data for KPI analysis  
\- Inputs for optimization triggers and dashboards

4.3 Warehouse Graph Modeling Engine  
Responsibilities:  
\- Transform warehouse configuration into a graph representation  
\- Encode zones, nodes, edges, paths, constraints, and traversal costs  
\- Represent machinery capabilities and movement restrictions

Graph model concepts:  
\- Nodes: storage points, docks, staging areas, intersections, work cells  
\- Edges: traversable paths between nodes  
\- Costs: time, congestion, distance, equipment limitations  
\- Constraints: one-way paths, blocked areas, capacity limits, restricted zones

Outputs:  
\- Warehouse graph model  
\- Route-ready topology for simulation  
\- Scenario-specific graph variants for experimentation

4.4 Simulation and Optimization Engine  
Responsibilities:  
\- Run operational simulations using the graph model  
\- Evaluate route and layout alternatives  
\- Apply reinforcement learning or heuristic optimization methods  
\- Score candidate solutions against objective functions

Candidate approaches:  
\- Reinforcement learning for route policy improvement  
\- Search and heuristic methods for layout variants  
\- Hybrid simulation where deterministic modeling and learned policies coexist

Possible optimization objectives:  
\- Minimize travel time  
\- Minimize congestion  
\- Maximize throughput  
\- Balance equipment utilization  
\- Reduce bottlenecks at high-traffic nodes

Outputs:  
\- Ranked route recommendations  
\- Ranked layout recommendations  
\- Scenario comparison metrics  
\- Run artifacts and optimization metadata

4.5 Analytics and KPI Service  
Responsibilities:  
\- Define KPI calculations and metric pipelines  
\- Aggregate operational and optimization outputs  
\- Compare baseline vs recommended scenarios  
\- Expose BI-ready datasets

Potential KPIs:  
\- Average travel time  
\- Throughput per period  
\- Pick path efficiency  
\- Congestion hotspots  
\- Equipment utilization  
\- Estimated productivity uplift

Outputs:  
\- KPI fact tables  
\- Scenario comparison tables  
\- Time-series performance datasets

4.6 Recommendation Service  
Responsibilities:  
\- Translate optimization outputs into human-readable recommendations  
\- Package route and layout improvements with supporting evidence  
\- Track recommendation provenance by optimization run and source inputs

Recommendation structure:  
\- Recommendation type  
\- Target area or route  
\- Expected benefit  
\- Confidence or support indicators  
\- Related assumptions and dependencies

Outputs:  
\- Recommendation records  
\- Recommendation summaries for dashboards and reports

4.7 Visualization Layer  
Responsibilities:  
\- Present KPIs, trends, and recommendations to users  
\- Expose business-facing dashboards in Power BI or similar tooling  
\- Support filtering by warehouse, time period, scenario, and recommendation type

Suggested Power BI views:  
\- Warehouse overview dashboard  
\- Throughput and sales trend dashboard  
\- Bottleneck and congestion dashboard  
\- Scenario comparison dashboard  
\- Recommendations dashboard

4.8 Scheduling and Orchestration Layer  
Responsibilities:  
\- Run periodic data refreshes  
\- Trigger optimization runs  
\- Support event-driven or time-based re-optimization  
\- Maintain workflow observability and failure handling

Examples:  
\- Nightly WMS ingestion  
\- Weekly KPI refresh  
\- Monthly or quarterly optimization rerun  
\- On-demand rerun after layout change or machinery update

5\. Data Flow  
Step 1: Warehouse setup data is entered into the configuration service.  
Step 2: WMS integration pulls operational and sales data into normalized storage.  
Step 3: Warehouse configuration is transformed into a graph model.  
Step 4: Simulation and optimization jobs consume the graph model plus operational context.  
Step 5: Optimization outputs are stored as run artifacts and recommendation candidates.  
Step 6: KPI pipelines combine operational and optimization data into BI-facing datasets.  
Step 7: Power BI consumes curated datasets and presents dashboards and recommendations.  
Step 8: Scheduling logic triggers future refreshes and reruns.

6\. Suggested Data Architecture  
Core storage domains:  
\- Configuration store  
\- Operational data store  
\- Graph/model artifacts store  
\- Optimization run store  
\- KPI/reporting store

Suggested logical entities:  
\- Warehouse  
\- WarehouseConfigurationVersion  
\- Zone  
\- PathEdge  
\- Equipment  
\- WMSConnection  
\- OrderSummary  
\- ThroughputMetric  
\- OptimizationRun  
\- SimulationScenario  
\- Recommendation  
\- KPIResult

Storage pattern suggestion:  
\- Relational database for operational metadata and core entities  
\- Object/file storage for layout files, graph artifacts, and simulation outputs  
\- Analytics-friendly tables or warehouse views for BI consumption

7\. Interface Boundaries  
Configuration API:  
\- Create/update warehouse configuration  
\- Retrieve active and historical warehouse definitions

WMS ingestion interface:  
\- Pull or receive source operational data  
\- Validate and normalize inbound data

Modeling interface:  
\- Generate graph from a warehouse configuration version  
\- Retrieve graph metadata and scenario variants

Optimization interface:  
\- Submit optimization run  
\- Retrieve run status and outputs  
\- Compare scenarios

Analytics interface:  
\- Retrieve KPI aggregates and scenario metrics  
\- Expose dashboard-ready datasets

Recommendation interface:  
\- Retrieve active recommendations  
\- Filter by warehouse, scenario, and time period

8\. Execution Model  
Recommended execution types:  
\- Synchronous APIs for configuration management and result retrieval  
\- Asynchronous jobs for ingestion, graph generation, simulation, and optimization  
\- Scheduled workflows for recurring refreshes and reruns

Suggested workflow pattern:  
\- User or scheduler triggers run  
\- Configuration snapshot is locked  
\- WMS data window is selected  
\- Graph is generated or reused  
\- Optimization job executes  
\- Results are persisted  
\- KPI materialization refreshes dashboard datasets  
\- Recommendations become visible in the BI layer

9\. Observability and Reliability  
The system should provide:  
\- Run status tracking for ingestion and optimization jobs  
\- Error logging and retry policies for external integrations  
\- Metadata linking outputs to input versions and source time windows  
\- Monitoring of data freshness for BI outputs  
\- Basic audit history of configuration changes and optimization runs

10\. Security and Access Considerations  
\- Restrict access to WMS credentials and connection settings  
\- Separate configuration editing permissions from dashboard viewing permissions  
\- Log changes to warehouse setup and optimization triggers  
\- Apply least-privilege access for integrations  
\- Ensure Power BI datasets expose only appropriate operational fields

11\. Deployment Considerations  
An MVP-friendly deployment could include:  
\- Backend services for configuration, ingestion, modeling orchestration, and optimization  
\- A database for metadata and operational records  
\- Scheduled jobs or workflow runner for recurring tasks  
\- Object storage for graph and simulation artifacts  
\- Power BI connected to curated reporting tables or exports

12\. MVP Technical Recommendation  
For the initial implementation, prioritize:  
\- A simple but stable canonical warehouse configuration model  
\- A normalized operational data ingestion pipeline  
\- A graph generation component with explicit cost modeling  
\- A practical optimization engine, even if it begins with heuristics before advanced RL  
\- A small set of trustworthy KPIs in Power BI  
\- A recommendation output that is easy to interpret and validate

13\. Open Technical Questions  
\- What WMS systems must be supported first?  
\- What input format should define warehouse layouts initially?  
\- Is the first graph generated manually, semi-automatically, or from structured layout data?  
\- Should RL be part of MVP, or should the system begin with heuristic optimization and add RL later?  
\- What latency expectations exist for optimization runs?  
\- How should recommendation confidence be calculated and displayed?  
\- How much historical data is required for useful reruns and comparisons?

14\. Suggested Next Technical Artifacts  
\- System context diagram  
\- Container/component diagram  
\- Data model draft  
\- API contract draft  
\- Optimization run lifecycle spec  
\- Power BI dataset schema  
\- Infrastructure and deployment plan

15\. Data Ingestion and Normalization Architecture  
This section defines how telemetry and WMS data should be ingested and normalized before downstream analytics and optimization.

15.1 Purpose  
The ingestion layer must turn raw source data into typed, validated, canonical internal models.

This phase focuses on:  
\- forklift trajectory CSV ingestion  
\- forklift state CSV ingestion  
\- normalization into internal canonical models  
\- quality filtering and validation  
\- preparation for later joins with ERPNext demand and warehouse data

15.2 Guiding Principles  
\- Keep raw data untouched and traceable.  
\- Normalize format before deriving insights.  
\- Separate parsing, validation, normalization, and derived metrics.  
\- Prefer explicit internal models over loose dictionaries.  
\- Use test-driven development for ingestion logic.  
\- Preserve uncertainty and quality information rather than hiding it.

15.3 Objectives  
The ingestion layer should:  
\- read raw CSV exports safely and repeatably  
\- validate required columns and data types  
\- convert rows into typed canonical internal models  
\- flag low-quality or suspicious telemetry rows  
\- preserve enough metadata for auditability and debugging  
\- expose clean data structures for later analytics and optimization

15.4 Input Files  
Current telemetry inputs:  
\- tracker unit index CSV  
\- trajectory CSV: \<device\_id\>.csv  
\- state CSV: \<device\_id\>\_STATE.csv

Later inputs:  
\- ERPNext sales/order data  
\- ERPNext warehouse/inventory data

15.5 Ingestion Stages  
Recommended stages:  
1\. file discovery  
2\. schema validation  
3\. row parsing  
4\. type conversion  
5\. normalization into canonical models  
6\. quality scoring / bad-data flagging  
7\. derived event generation  
8\. export to downstream modules

15.6 Canonical Telemetry Models  
Core internal models should include:  
\- TelemetryPoint  
\- DeviceStateEvent  
\- BeaconObservation  
\- TelemetryQualityFlag  
\- TelemetryBatchMetadata

TelemetryPoint should include:  
\- device\_id  
\- timestamp  
\- x, y, z  
\- quaternion orientation  
\- std\_x, std\_y, std\_z  
\- std\_R, std\_P, std\_Y  
\- derived 2D uncertainty  
\- quality status  
\- source file / source row identifier

DeviceStateEvent should include:  
\- device\_id  
\- timestamp  
\- ready  
\- load beacon fields  
\- zero to five driver beacon observations  
\- source file / source row identifier

15.7 Validation Rules  
Trajectory CSV validation:  
\- required columns must be present  
\- timestamp must parse cleanly  
\- x, y, z and std fields must parse as numbers where present  
\- rows with missing essential location fields should be rejected or flagged

State CSV validation:  
\- required columns must be present  
\- timestamp must parse cleanly  
\- ready must parse to a boolean  
\- beacon IDs and RSSI fields should parse when present  
\- partially populated beacon groups should be preserved but flagged if malformed

15.8 Quality and Filtering Rules  
Initial telemetry quality rules:  
\- compute 2D uncertainty as sqrt(std\_x^2 \+ std\_y^2)  
\- if 2D uncertainty \> 2 to 3 meters, mark row as low confidence  
\- define explicit thresholds such as:  
  \- good: \<= 1.0 m  
  \- review: \> 1.0 m and \<= 2.5 m  
  \- poor: \> 2.5 m  
\- preserve poor rows for audit/debug purposes even if excluded from route analysis

Additional possible quality checks:  
\- impossible jumps between adjacent timestamps  
\- repeated duplicate timestamps for the same device  
\- missing or malformed quaternion fields  
\- unexpected gaps in 1 Hz sequences

15.9 Derived Signals  
After normalization, derive a first layer of signals:  
\- moving vs stopped classification  
\- route segment continuity  
\- stop duration windows  
\- high-traffic path counts  
\- candidate hotspots  
\- load-present vs load-absent movement windows  
\- driver-associated movement windows where beacon data is usable

These should be derived in a separate module after base normalization is complete.

15.10 ERPNext Readiness  
The ingestion layer should prepare for later joins with ERPNext by making sure telemetry data can be grouped by:  
\- device\_id  
\- warehouse/site identifier  
\- time window  
\- movement session

Later, normalized ERPNext entities should include:  
\- products  
\- warehouses  
\- sales orders  
\- sales order lines  
\- inventory balances  
\- stock movement records

15.11 Proposed Module Boundaries  
Suggested modules:  
\- telemetry/models.py  
\- telemetry/parser.py  
\- telemetry/validation.py  
\- telemetry/quality.py  
\- telemetry/derived.py  
\- telemetry/io.py

Responsibilities:  
\- parser.py: raw CSV parsing and type conversion  
\- validation.py: schema and required-field validation  
\- quality.py: uncertainty and quality rules  
\- derived.py: movement summaries and analytics-ready signals  
\- io.py: file loading and batch orchestration

15.12 TDD Implementation Approach  
The ingestion layer should be built with TDD.

Test order:  
1\. schema validation tests  
2\. row parsing tests  
3\. timestamp / numeric / boolean conversion tests  
4\. uncertainty calculation tests  
5\. bad-data flagging tests  
6\. full sample-file ingestion tests  
7\. derived signal tests

Testing principles:  
\- start from sample fixture CSVs  
\- add targeted edge-case fixtures for malformed rows  
\- assert both accepted rows and flagged rows  
\- keep parsing deterministic and reproducible  
\- test on small fixtures first before real client data

15.13 Immediate Implementation Plan  
1\. Create canonical telemetry dataclasses.  
2\. Implement trajectory CSV parser.  
3\. Implement state CSV parser.  
4\. Implement quality scoring and uncertainty thresholds.  
5\. Add tests for clean rows, malformed rows, and high-uncertainty rows.  
6\. Build the first normalized telemetry batch output.  
7\. Prepare join points for ERPNext demand data later.

15.14 Key Rule  
Do not let optimization or analytics modules read raw CSV directly.

All downstream logic should consume normalized internal telemetry models.