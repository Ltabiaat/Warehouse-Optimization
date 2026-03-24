# Streamlit Warehouse Layout Configurator

## Purpose

A cleaner Streamlit UI for defining:
- warehouse layout size
- number of forklifts
- blocked/unreachable cells
- named zones on the grid

## Run

From `warehouse_mvp/`:

```bash
source .venv/bin/activate
streamlit run streamlit_app.py
```

## How to use

- Resize the grid in the sidebar
- Edit cells directly in the table-style grid
- Use:
  - `X` for blocked cells
  - `A-F` for named zones
  - blank for normal reachable cells
- Save the configuration to JSON

## Output

When saved, the app writes:
- `output/warehouse_layout_config.json`

The JSON includes:
- dimensions
- forklift count
- blocked cells
- zone cell assignments

## Notes

This is an MVP grid-based editor intended as a front-end for later graph/simulation conversion.
