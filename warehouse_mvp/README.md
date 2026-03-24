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

## Next steps
- add CSV ingestion CLI
- add dataframe/batch processing
- add KPI generation
- add heuristic scoring
