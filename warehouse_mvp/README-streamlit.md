# Streamlit Warehouse Layout Configurator

## Purpose

A simple Streamlit UI for defining:
- warehouse layout size
- number of forklifts
- blocked/unreachable cells

## Run

From `warehouse_mvp/`:

```bash
pip install -r requirements-streamlit.txt
streamlit run streamlit_app.py
```

## Output

When saved, the app writes:
- `output/warehouse_layout_config.json`

## Notes

This is an MVP grid-based editor.
It is intended to be a simple front-end for later graph/simulation conversion.
