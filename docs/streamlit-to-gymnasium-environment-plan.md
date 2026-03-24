# Streamlit to Gymnasium Environment Plan

Purpose: define how the Streamlit warehouse layout input becomes a custom Gymnasium environment.

## Core idea

The Streamlit app is the human-facing configuration layer.
It should not be the environment itself.

Instead, the conversion path should be:

1. Streamlit saves a warehouse layout JSON
2. the JSON is parsed into a canonical warehouse configuration model
3. the canonical config is converted into a traversable graph/grid topology
4. the topology becomes the basis for a custom Gymnasium environment
5. scenario/task generation defines what forklifts are trying to do inside that environment

## Proposed pipeline

### Step 1: Streamlit output
Current output fields:
- warehouse_name
- width
- height
- forklift_count
- blocked_cells
- zone_cells

This is enough to define the first warehouse topology.

### Step 2: Canonical warehouse configuration model
Convert the raw JSON into an internal model such as:
- WarehouseConfig
- GridCell
- ZoneDefinition
- ForkliftSpec

This avoids having downstream code depend directly on raw JSON dictionaries.

### Step 3: Topology generation
From the canonical model, generate:
- reachable cells
- blocked cells
- zone lookup
- adjacency between reachable cells

For MVP, use 4-neighbor movement:
- up
- down
- left
- right

This turns the layout into a route-ready graph.

### Step 4: Task/scenario definition
The environment still needs a task.
The layout alone is not enough.

For MVP, define a simple task family such as:
- forklift starts at a reachable cell
- target zone sequence is provided, e.g. A -> C
- agent must navigate while avoiding blocked cells
- reward encourages short valid paths and task completion

### Step 5: Gymnasium environment
The custom environment should encapsulate:
- warehouse topology
- forklift count (initially likely one-agent simplification)
- current forklift position(s)
- target zone(s)
- step logic
- reward logic
- termination logic

## Recommended MVP environment scope

To stay practical, start with:
- single forklift
- grid-based navigation
- blocked cells
- named zones
- one target zone at a time or a small ordered zone list

Defer:
- multi-agent forklift coordination
- congestion between forklifts
- dynamic traffic rules
- stochastic delays
- rich task assignment

## Proposed internal models

### WarehouseConfig
Fields:
- warehouse_name
- width
- height
- forklift_count
- blocked_cells: set[(x, y)]
- zone_cells: dict[(x, y)] -> zone_label

### WarehouseTopology
Fields:
- reachable_cells
- blocked_cells
- zone_cells
- adjacency_map
- zone_to_cells

### NavigationTask
Fields:
- start_cell
- target_zones
- current_target_index

## Proposed observation model

For the first Gymnasium environment, observation can be simple and explicit.

Example observation:
- current forklift x, y
- current target zone label
- blocked-cell mask
- zone-cell mask(s)
- optionally visited zones / progress index

Possible implementations:
- dictionary observation space
- flattened vector observation
- grid tensor later if needed

For MVP, a dictionary observation is easier to debug.

## Proposed action space

Initial discrete actions:
- 0 = up
- 1 = down
- 2 = left
- 3 = right
- 4 = stay

This is enough for first route-learning experiments.

## Proposed reward model

First simple reward design:
- +10 for reaching the current target zone
- +50 for finishing the full target sequence
- -1 per step
- -5 for invalid move into blocked/out-of-bounds area
- small penalty for staying still without reason

This keeps the environment interpretable.

## Proposed termination conditions

Episode ends when:
- all target zones have been reached in order
- max step count is reached

## How zones should work

Zones are important because they convert a plain map into task-relevant destinations.

Example:
- Zone A = inbound dock
- Zone C = picking area
- Zone F = outbound staging

A task can then be:
- start somewhere reachable
- go to A
- then C
- then F

This is much more useful than trying to navigate to arbitrary coordinates.

## Conversion modules to create

Recommended modules:
- `src/warehouse_mvp/layout_models.py`
- `src/warehouse_mvp/layout_loader.py`
- `src/warehouse_mvp/topology.py`
- `src/warehouse_mvp/tasks.py`
- `src/warehouse_mvp/gym_env.py`

Responsibilities:
- layout_models.py: typed config dataclasses
- layout_loader.py: load/validate Streamlit JSON
- topology.py: build adjacency and zone lookup
- tasks.py: define target-zone tasks
- gym_env.py: custom Gymnasium environment

## Immediate implementation order

1. create canonical layout dataclasses
2. create JSON loader/validator
3. create topology builder
4. create task definition helper
5. create first custom Gymnasium environment
6. test with a saved Streamlit config fixture

## Key design rule

Do not let the Gymnasium environment read raw Streamlit JSON directly.
Always convert Streamlit output into canonical internal models first.
