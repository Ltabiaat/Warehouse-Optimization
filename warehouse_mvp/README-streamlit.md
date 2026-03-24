# Streamlit Warehouse Layout Configurator

## Purpose

A cleaner Streamlit UI for defining:
- warehouse layout size
- number of forklifts
- blocked/unreachable cells
- named zones on the grid
- forklift start positions
- inbound and outbound dock markers

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
  - `S` for forklift starts
  - `I` for inbound docks
  - `O` for outbound docks
  - `A-F` for named zones
  - blank for normal reachable cells
- Click **Apply grid edits**
- Save the configuration to JSON

## Output

When saved, the app writes:
- `output/warehouse_layout_config.json`

The JSON includes:
- dimensions
- forklift count
- blocked cells
- zone cell assignments
- start cells
- inbound docks
- outbound docks
