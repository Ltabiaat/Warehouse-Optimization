# Generated Task Demo

Purpose: demonstrate the architecture path where operational data generates forklift tasks that are then executed inside the Gymnasium environment.

## Script
- `warehouse_mvp/scripts/run_generated_task_demo.py`

## What it does
1. creates/loads a demo warehouse layout with starts, zones, and docks
2. loads the sample warehouse export
3. normalizes the export rows
4. generates outbound forklift tasks from the normalized rows
5. converts the top generated task into a task sequence
6. adapts the task sequence into a Gymnasium navigation task
7. runs the environment against that generated task

## Why it matters
This proves the architecture chain:
- operational data -> forklift task generation -> task sequence -> environment execution

## Current limitation
The adapter currently only turns zone-addressable sequence steps into navigation targets.
That is enough for the MVP path, but later the environment should consume richer task semantics more directly.

## Run
From `warehouse_mvp/`:

```bash
source .venv/bin/activate
PYTHONPATH=src python scripts/run_generated_task_demo.py
```
