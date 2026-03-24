# Warehouse MVP

A small, test-first data pipeline for normalizing real warehouse movement exports into an analysis-ready event table.

## Initial scope
- parse raw warehouse export rows
- map Japanese column names into normalized English fields
- normalize timestamps and quantities
- generate derived event fields
- support baseline KPI and heuristic work later

## Layout
- `warehouse_mvp/schema.py` - source column names and mapping definitions
- `warehouse_mvp/normalizer.py` - row normalization logic
- `tests/test_normalizer.py` - initial unit tests

## Sample data
- `data/sample_warehouse_export.csv` contains a realistic sample export using the original Japanese headers.
- It includes inbound, outbound, transfer, and inventory-count style rows for MVP testing.

## Current outputs
- `output/sample_warehouse_normalized.csv` - normalized version of the sample export
- `output/sample_kpi_summary.json` - first KPI summary generated from the sample export

## Current status
- sample CSV ingestion works
- row normalization works
- KPI summary generation works
- built-in unit tests pass

## Next steps
- add CLI argument support for arbitrary input/output files
- add heuristic scoring
- add anomaly/validation reporting
- test against a real warehouse extract
