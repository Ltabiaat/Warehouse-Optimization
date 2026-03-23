# Warehouse Optimization

Warehouse Optimization is a warehouse analysis and decision-support system for improving routes, layouts, and throughput over time.

The current project direction is based on three foundation documents:
- `docs/project-outline.md`
- `docs/product-requirements.md`
- `docs/technical-architecture.md`

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
│   ├── implementation-plan.md
│   ├── product-requirements.md
│   ├── project-outline.md
│   ├── tech-stack.md
│   └── technical-architecture.md
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

## Immediate Next Steps

1. Finalize the canonical warehouse configuration model
2. Define the initial WMS ingestion schema
3. Build the graph model representation
4. Implement an MVP optimization run pipeline
5. Produce dashboard-ready KPI outputs

## Development Status

This repository is currently in the project setup and architecture phase.
