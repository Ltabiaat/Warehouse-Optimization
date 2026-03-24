# Layout Environment Demo

Purpose: describe the first runnable demo that connects saved layout JSON to the Gymnasium environment.

## Script
- `warehouse_mvp/scripts/run_layout_env_demo.py`

## What it does
1. loads a saved Streamlit layout JSON if one exists
2. otherwise creates a fallback demo layout JSON
3. converts the layout into a canonical warehouse config
4. creates a simple task with a zone sequence (`A -> C`)
5. instantiates `WarehouseNavigationEnv`
6. resets the environment
7. runs a short hard-coded action sequence
8. prints observations, rewards, and the rendered grid

## Why it matters
This is the fastest way to prove the path:
- Streamlit-style layout config
- internal config loading
- topology/task generation
- Gymnasium environment execution

## Run
From `warehouse_mvp/`:

```bash
source .venv/bin/activate
PYTHONPATH=src python scripts/run_layout_env_demo.py
```

## Expected outcome
You should see:
- the loaded layout path
- the target zone sequence
- an ASCII grid render
- step-by-step rewards and info
- the forklift moving toward zones
