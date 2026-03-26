# Warehouse Optimization

Warehouse Optimization is a warehouse analysis and decision-support system for improving routes, layouts, and throughput over time.

The current project direction is maintained in Google Docs, not in this repository. Repo code should implement the current agreed specs, while planning/spec documents live in Google Drive.

## Vision

Build a system that:
- captures warehouse configuration and machinery context
- integrates WMS sales and operational data
- models the warehouse as a graph
- runs simulation / optimization workflows to improve routes and layouts
- exposes KPIs and recommendations through a BI-friendly interface

## Initial Architecture Areas

The current repository scaffold is organized around the major architecture domains:
- `config` — warehouse setup and configuration management
- `wms` — WMS ingestion and normalization
- `modeling` — warehouse graph generation and model artifacts
- `optimization` — simulation and optimization workflows
- `analytics` — KPI calculation and reporting datasets
- `recommendations` — recommendation generation and presentation logic
- `orchestration` — scheduled and on-demand workflow coordination
- `api` — interfaces for configuration, run triggers, and results

## Repo Structure

```text
.
├── docs/
│   └── (reserved for implementation-adjacent technical notes only)
├── src/
│   └── warehouse_optimization/
│       ├── analytics/
│       ├── api/
│       ├── config/
│       ├── modeling/
│       ├── optimization/
│       ├── orchestration/
│       ├── recommendations/
│       └── wms/
├── tests/
└── pyproject.toml
```

## Specification Source of Truth

Specification and planning documents should live in Google Docs / Google Drive, not in the repository.

Use the repo for:
- implementation code
- tests
- sample data
- implementation-adjacent technical notes

Use Google Docs for:
- product specs
- PRDs
- architecture docs
- research writeups
- prompt-engineering and planning docs

## Immediate Next Steps

1. Finalize the canonical warehouse configuration model
2. Define the initial WMS ingestion schema
3. Build the graph model representation
4. Implement an MVP optimization run pipeline
5. Produce dashboard-ready KPI outputs

## Development Workflow

A lightweight Makefile is included for common test-first development tasks.

Examples:

```bash
make test
make test-verbose
make clean-pyc
```

## Development Status

This repository is currently in the project setup and architecture phase.
