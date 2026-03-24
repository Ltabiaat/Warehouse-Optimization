# Route RL Layer

Purpose: define the first reinforcement-learning training layer for fixed-layout route execution.

## Scope now
- fixed warehouse layout
- generated outbound tasks
- Gymnasium navigation environment
- trainable RL loop

## Added pieces
- `warehouse_mvp/src/warehouse_mvp/rl_env_factory.py`
- `warehouse_mvp/scripts/train_route_agent.py`

## Current training path
1. load warehouse layout JSON
2. load and normalize warehouse export CSV
3. generate outbound tasks
4. convert selected task into a sequence
5. adapt sequence into a navigation task
6. instantiate `WarehouseNavigationEnv`
7. train PPO on the environment
8. save model and evaluation artifacts

## Current algorithm choice
- PPO via Stable-Baselines3

Why:
- stable and common baseline
- works with discrete actions
- works with the environment's dict observation via `MultiInputPolicy`

## Current outputs
Training script writes:
- trained model artifact
- evaluation summary JSON
- evaluation trace JSON

## Important note
This is the route RL layer only.
It assumes a fixed layout and fixed zones for the duration of an episode.

Layout-change optimization remains a later layer.
