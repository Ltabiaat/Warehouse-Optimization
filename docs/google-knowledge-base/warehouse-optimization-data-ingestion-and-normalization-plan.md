Warehouse Optimization Data Ingestion and Normalization Plan

Purpose  
This document defines how the system should ingest, validate, normalize, and prepare warehouse telemetry data and WMS data for downstream analytics and optimization.

Scope  
This phase focuses on:  
\- forklift trajectory CSV ingestion  
\- forklift state CSV ingestion  
\- normalization into internal canonical models  
\- quality filtering and validation  
\- preparation for later joins with ERPNext demand and warehouse data

Guiding Principles  
\- Keep raw data untouched and traceable.  
\- Normalize format before deriving insights.  
\- Separate parsing, validation, normalization, and derived metrics.  
\- Prefer explicit internal models over loose dictionaries.  
\- Use test-driven development for all ingestion logic.  
\- Preserve uncertainty and quality information rather than hiding it.

1\. Objectives  
The ingestion layer should:  
1\. read raw CSV exports safely and repeatably  
2\. validate required columns and data types  
3\. convert rows into typed canonical internal models  
4\. flag low-quality or suspicious telemetry rows  
5\. preserve enough metadata for auditability and debugging  
6\. expose clean data structures for later analytics and optimization

2\. Input Files  
Current telemetry inputs:  
\- tracker unit index CSV  
\- trajectory CSV: \<device\_id\>.csv  
\- state CSV: \<device\_id\>\_STATE.csv

Later inputs:  
\- ERPNext sales/order data  
\- ERPNext warehouse/inventory data

3\. Ingestion Architecture  
Recommended stages:  
1\. file discovery  
2\. schema validation  
3\. row parsing  
4\. type conversion  
5\. normalization into canonical models  
6\. quality scoring / bad-data flagging  
7\. derived event generation  
8\. export to downstream modules

4\. Canonical Telemetry Models  
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

5\. Validation Rules  
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

6\. Quality and Filtering Rules  
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

7\. Derived Signals  
After normalization, derive a first layer of signals:  
\- moving vs stopped classification  
\- route segment continuity  
\- stop duration windows  
\- high-traffic path counts  
\- candidate hotspots  
\- load-present vs load-absent movement windows  
\- driver-associated movement windows where beacon data is usable

These should be derived in a separate module after base normalization is complete.

8\. ERPNext/WMS Readiness  
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

9\. Proposed Module Boundaries  
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

10\. Test-Driven Development Approach  
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

11\. Immediate Implementation Plan  
Step 1:  
Create canonical telemetry dataclasses.

Step 2:  
Implement trajectory CSV parser.

Step 3:  
Implement state CSV parser.

Step 4:  
Implement quality scoring and uncertainty thresholds.

Step 5:  
Add tests for clean rows, malformed rows, and high-uncertainty rows.

Step 6:  
Build the first normalized telemetry batch output.

Step 7:  
Prepare join points for ERPNext demand data later.

12\. Key Rule  
Do not let optimization or analytics modules read raw CSV directly.

All downstream logic should consume normalized internal telemetry models.

13\. Why This Matters  
This approach gives the project:  
\- cleaner code boundaries  
\- better debugging  
\- safer use of sensitive data later  
\- easier ERPNext integration  
\- stronger confidence in recommendations  
\- a repeatable engineering process  
