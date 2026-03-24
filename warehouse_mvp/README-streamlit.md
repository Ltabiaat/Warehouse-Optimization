# Streamlit Warehouse Layout Configurator

## Purpose

A simple Streamlit UI for defining:
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

## Output

When saved, the app writes:
- `output/warehouse_layout_config.json`

The JSON includes:
- dimensions
- forklift count
- blocked cells
- zone cell assignments

## Notes

This is an MVP grid-based editor.
It is intended to be a simple front-end for later graph/simulation conversion.
Blocked cells represent places forklifts cannot traverse.
Zones represent places forklifts may need to reach.
