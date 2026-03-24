from __future__ import annotations

import json
from pathlib import Path

from warehouse_mvp.gym_env import WarehouseNavigationEnv
from warehouse_mvp.layout_loader import load_layout_config
from warehouse_mvp.tasks import make_simple_zone_task

BASE = Path(__file__).resolve().parents[1]
LAYOUT_PATH = BASE / "output" / "warehouse_layout_config.json"
SAMPLE_LAYOUT_PATH = BASE / "output" / "warehouse_layout_config.demo.json"


def ensure_demo_layout_exists() -> Path:
    if LAYOUT_PATH.exists():
        return LAYOUT_PATH

    sample_payload = {
        "warehouse_name": "Demo Warehouse",
        "width": 6,
        "height": 5,
        "forklift_count": 2,
        "blocked_cells": [
            {"x": 2, "y": 1},
            {"x": 2, "y": 2},
            {"x": 2, "y": 3},
        ],
        "zone_cells": [
            {"x": 5, "y": 0, "zone": "A"},
            {"x": 5, "y": 4, "zone": "C"},
        ],
        "start_cells": [{"x": 0, "y": 0}],
        "inbound_docks": [{"x": 0, "y": 4}],
        "outbound_docks": [{"x": 5, "y": 4}],
    }
    SAMPLE_LAYOUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SAMPLE_LAYOUT_PATH.write_text(json.dumps(sample_payload, indent=2), encoding="utf-8")
    return SAMPLE_LAYOUT_PATH


def main() -> None:
    layout_path = ensure_demo_layout_exists()
    config = load_layout_config(layout_path)
    task = make_simple_zone_task(config, ["A", "C"])
    env = WarehouseNavigationEnv(config, task, max_steps=50)

    obs, info = env.reset()
    print(f"Loaded layout: {layout_path}")
    print(f"Warehouse: {config.warehouse_name}")
    print(f"Starts: {config.start_cells}")
    print(f"Inbound docks: {config.inbound_docks}")
    print(f"Outbound docks: {config.outbound_docks}")
    print(f"Task target sequence: {task.target_zones}")
    print("\nInitial grid:")
    print(env.render())
    print("\nInitial observation:")
    print(obs)
    print("Initial info:")
    print(info)

    demo_actions = [3, 3, 3, 3, 3, 1, 1, 1, 1]
    print("\nRunning demo actions:")
    print("Actions: right,right,right,right,right,down,down,down,down")

    for step_num, action in enumerate(demo_actions, start=1):
        obs, reward, terminated, truncated, info = env.step(action)
        print(f"\nStep {step_num}")
        print(f"Action: {action}")
        print(f"Reward: {reward}")
        print(f"Terminated: {terminated} | Truncated: {truncated}")
        print(f"Info: {info}")
        print(env.render())
        if terminated or truncated:
            break


if __name__ == "__main__":
    main()
