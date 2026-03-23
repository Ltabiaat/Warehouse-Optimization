# Warehouse Optimization Tech Stack

## Purpose
This document defines the recommended technology stack for the current Warehouse Optimization MVP, based on the project outline, PRD, technical architecture, and the repository scaffold already in place.

## Guiding Principles
For the MVP, the stack should:
- be fast to prototype with
- handle structured data and analytics well
- support simulation and optimization workflows
- integrate cleanly with CSV-based source data first
- leave room for later WMS integrations, APIs, and BI delivery

## Recommended MVP Stack

### 1. Core Language
**Python 3.11+**

Why:
- strong ecosystem for data processing, analytics, simulation, and optimization
- well suited for CSV ingestion and rapid prototyping
- flexible enough for domain modeling, batch jobs, and API development
- already matches the repo scaffold

Primary use:
- domain models
- ingestion pipeline
- graph modeling
- optimization logic
- KPI generation
- orchestration scripts/services

### 2. Data Modeling and Validation
**Python dataclasses initially**

Current repo direction:
- the repository already uses Python dataclasses for core domain models

Near-term recommendation:
- start with `dataclasses` while the schema is still fluid
- introduce **Pydantic** later if/when strict API contracts and input validation become a priority

Why:
- low friction for early development
- keeps the MVP lightweight
- easy to refactor once real data patterns are better understood

### 3. Data Ingestion and Transformation
**Python standard library `csv` + `datetime` first**

Optional next step:
- **pandas** for heavier batch analysis and transformations

Why:
- current input format is CSV
- standard library is enough for initial parsing and validation
- avoids overcomplicating the first ingestion layer
- pandas can be added later once we start doing larger-scale analysis and aggregation

Initial responsibilities:
- parse tracker unit index CSV
- parse trajectory CSVs
- parse state CSVs
- validate required columns
- type conversion for timestamps, numeric fields, and booleans
- calculate 2D position uncertainty
- flag poor-quality data rows

### 4. Optimization and Simulation
**Python-first custom optimization layer**

MVP recommendation:
- begin with heuristic optimization and scoring
- add reinforcement learning only after baseline simulation and scoring work reliably

Potential libraries later:
- **NetworkX** for graph operations
- **NumPy** for numeric computation
- **SciPy** for optimization support
- **Ray RLlib**, **Stable-Baselines3**, or similar only if RL becomes necessary

Why:
- the PRD allows practical optimization, not necessarily RL-first
- heuristics are faster to validate with real operational data
- RL is expensive to get right without mature simulation inputs

### 5. Graph Modeling
**Python domain models first, with likely upgrade to NetworkX**

Current repo direction:
- custom graph primitives already exist in `src/warehouse_optimization/modeling/graph.py`

Recommendation:
- keep internal node/edge domain models
- use **NetworkX** if pathfinding, graph analytics, and scenario comparison start growing in complexity

Why:
- custom models keep business meaning explicit
- NetworkX can accelerate route/path algorithms when needed

### 6. API Layer
**FastAPI**

Use when:
- exposing warehouse configuration endpoints
- triggering optimization runs
- retrieving results and recommendations
- providing BI-facing or frontend-facing service endpoints

Why:
- modern Python API framework
- good type support and documentation generation
- strong fit for internal APIs and MVP services

Status:
- not yet added to the repo
- should be introduced once domain models and ingestion are stable enough to expose

### 7. Storage
**MVP option: file-based fixtures + lightweight relational database**

Recommended path:
- start with CSV fixtures and local file artifacts
- add **PostgreSQL** as the main relational store once core entities stabilize

Suggested storage split:
- CSV/files for raw ingested fixture data
- PostgreSQL for:
  - warehouse configuration
  - equipment/zones metadata
  - normalized operational records
  - optimization run metadata
  - recommendation records
- file/object storage later for graph artifacts and simulation outputs if needed

Why:
- keeps early development simple
- PostgreSQL gives a strong long-term foundation without being overkill

### 8. Analytics and BI Output
**Power BI**

Why:
- already identified in the project docs as the likely user-facing reporting layer
- good fit for KPI dashboards and recommendation summaries
- suitable for business stakeholders and operations teams

Recommended backend role:
- Python generates curated reporting tables / CSV exports / database views
- Power BI consumes those outputs

### 9. Scheduling and Orchestration
**Python scripts first, scheduler later**

MVP approach:
- manual CLI or script-driven runs first
- scheduled recurring runs later

Likely future options:
- cron
- APScheduler
- Prefect
- Airflow (only if workflows become much more complex)

Why:
- don’t introduce workflow infrastructure too early
- first prove the ingestion → graph → optimization → recommendation flow

### 10. Testing
**unittest initially**

Current repo direction:
- repository already uses `unittest`

Recommendation:
- keep `unittest` for early tests
- optionally move to `pytest` later for richer fixtures and better developer ergonomics

Testing targets:
- CSV parsing
- schema validation
- uncertainty filtering
- graph generation
- optimization scoring
- recommendation formatting

### 11. Packaging and Environment
**pyproject.toml-based Python project**

Current repo direction:
- already in place

Recommended additions later:
- virtual environment (`.venv`)
- dependency locking if deployment starts soon
- linting and formatting tools such as:
  - `ruff`
  - `black`
  - `mypy` (optional when types mature)

## Proposed MVP Stack Summary

### Immediate stack
- **Language:** Python 3.11+
- **Modeling:** dataclasses
- **Parsing:** csv, datetime, math
- **Testing:** unittest
- **Storage:** CSV fixtures + local files
- **Docs:** Markdown in repo + Google Docs for planning
- **BI:** Power BI

### Near-term additions
- **Database:** PostgreSQL
- **API:** FastAPI
- **Graph library:** NetworkX
- **Data analysis:** pandas, NumPy
- **Lint/format:** ruff, black

### Later-stage additions if justified
- **Optimization/RL:** SciPy, Stable-Baselines3, RLlib, or similar
- **Workflow orchestration:** APScheduler / Prefect / Airflow
- **Artifact storage:** object storage for graph and simulation outputs

## Recommended Implementation Order for Stack Adoption
1. Build CSV ingestion with the Python standard library
2. Add validation and uncertainty filtering
3. Build graph generation from parsed warehouse/tracker data
4. Implement heuristic optimization and recommendation outputs
5. Introduce PostgreSQL for normalized storage
6. Add FastAPI for service endpoints
7. Add Power BI-facing exports/views
8. Evaluate whether RL is actually needed

## Key Technical Decision
The most important stack choice is this:

**Do not start with reinforcement learning just because it sounds impressive.**

The best MVP path is:
- Python
- CSV ingestion
- clean domain models
- graph representation
- heuristic optimization
- KPI/recommendation output

Then add RL only if the simpler system cannot produce useful warehouse decisions.
