# First Gymnasium Environment Spec

Purpose: define the first runnable Gymnasium environment built from Streamlit-generated warehouse layout data.

## Environment name
- `WarehouseNavigationEnv`

## Initial scope
- single forklift
- 2D grid warehouse
- blocked cells
- named zones
- ordered target zone sequence

## Inputs
- `WarehouseConfig`
- `NavigationTask`
- `max_steps`

## Action space
Discrete actions:
- 0 = up
- 1 = down
- 2 = left
- 3 = right
- 4 = stay

## Observation space
Dictionary observation with:
- `forklift_position`
- `current_target_index`
- `blocked_mask`
- `zone_mask`

## Reward design
- base step penalty: `-1`
- invalid move penalty: `-5` additional
- stay penalty: `-0.5` additional
- reaching current target zone: `+10`
- completing full target sequence: `+50`

## Termination
Episode ends when:
- all target zones in the sequence are reached, or
- max step count is exceeded (truncated)

## Why this is a good MVP
- simple enough to test and debug
- directly connected to Streamlit input data
- useful for early route-learning experiments
- can later be extended toward multiple forklifts, richer tasks, and better cost modeling

## Deferred features
- multi-agent coordination
- congestion modeling
- travel-time costs beyond step count
- one-way aisles
- forklift-specific capabilities
- dynamic tasks from real ERPNext/WMS demand data
