from __future__ import annotations

from pathlib import Path

from warehouse_mvp.gym_env import WarehouseNavigationEnv
from warehouse_mvp.io_csv import normalize_rows, read_raw_rows
from warehouse_mvp.layout_loader import load_layout_config
from warehouse_mvp.order_task_generator import generate_outbound_tasks, task_to_sequence
from warehouse_mvp.task_sequence_adapter import sequence_to_navigation_task

BASE = Path(__file__).resolve().parents[1]
LAYOUT_PATH = BASE / "output" / "warehouse_layout_config.demo.generated.json"
RAW_EXPORT = BASE / "data" / "sample_warehouse_export.csv"


DEMO_LAYOUT = {
    "warehouse_name": "Generated Task Demo Warehouse",
    "width": 8,
    "height": 6,
    "forklift_count": 2,
    "blocked_cells": [
        {"x": 3, "y": 1},
        {"x": 3, "y": 2},
        {"x": 3, "y": 3},
    ],
    "zone_cells": [
        {"x": 1, "y": 1, "zone": "A"},
        {"x": 1, "y": 3, "zone": "B"},
        {"x": 5, "y": 2, "zone": "QC"},
        {"x": 7, "y": 5, "zone": "OUT"},
    ],
    "start_cells": [{"x": 0, "y": 0}],
    "inbound_docks": [{"x": 0, "y": 5}],
    "outbound_docks": [{"x": 7, "y": 5}],
}


def ensure_demo_layout() -> Path:
    import json

    LAYOUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    LAYOUT_PATH.write_text(json.dumps(DEMO_LAYOUT, indent=2), encoding="utf-8")
    return LAYOUT_PATH


def main() -> None:
    layout_path = ensure_demo_layout()
    config = load_layout_config(layout_path)

    raw_rows = read_raw_rows(RAW_EXPORT)
    normalized = normalize_rows(raw_rows)

    tasks = generate_outbound_tasks(
        normalized,
        location_to_zone={
            "F1-A-01": "A",
            "F1-B-02": "B",
            "F1-B-05": "B",
            "F2-A-07": "A",
            "F3-F-02": "A",
        },
        processing_zone_by_item={
            "SKU-005": "QC",
            "SKU-002": "QC",
        },
        default_dropoff_zone="OUT",
    )

    task = tasks[0]
    sequence = task_to_sequence(task)
    nav_task = sequence_to_navigation_task(config, sequence)
    env = WarehouseNavigationEnv(config, nav_task, max_steps=60)

    obs, info = env.reset()
    print(f"Loaded layout: {layout_path}")
    print(f"Selected generated task: {task}")
    print(f"Task sequence: {sequence.steps}")
    print(f"Navigation targets: {nav_task.target_zones}")
    print("\nInitial grid:")
    print(env.render())
    print("\nInitial observation:")
    print(obs)
    print("Initial info:")
    print(info)

    # Route: from (0,0) to B at (1,3), then QC at (5,2), then OUT at (7,5)
    demo_actions = [1, 3, 1, 1, 3, 3, 3, 0, 3, 1, 1, 1, 3]
    print("\nRunning generated-task demo actions:")
    print(demo_actions)

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
