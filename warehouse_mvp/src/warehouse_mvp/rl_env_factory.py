from __future__ import annotations

from typing import Callable

from .gym_env import WarehouseNavigationEnv
from .layout_loader import load_layout_config
from .order_task_generator import generate_outbound_tasks, task_to_sequence
from .task_sequence_adapter import sequence_to_navigation_task
from .io_csv import normalize_rows, read_raw_rows


def build_route_env(
    layout_path: str,
    warehouse_csv_path: str,
    location_to_zone: dict[str, str] | None = None,
    processing_zone_by_item: dict[str, str] | None = None,
    default_dropoff_zone: str | None = None,
    task_index: int = 0,
    max_steps: int = 100,
    render_mode: str | None = None,
) -> WarehouseNavigationEnv:
    config = load_layout_config(layout_path)
    raw_rows = read_raw_rows(warehouse_csv_path)
    normalized = normalize_rows(raw_rows)
    tasks = generate_outbound_tasks(
        normalized,
        location_to_zone=location_to_zone or {},
        processing_zone_by_item=processing_zone_by_item or {},
        default_dropoff_zone=default_dropoff_zone,
    )
    if not tasks:
        raise ValueError("No outbound tasks generated from operational data")

    task = tasks[min(task_index, len(tasks) - 1)]
    sequence = task_to_sequence(task)
    nav_task = sequence_to_navigation_task(config, sequence)
    return WarehouseNavigationEnv(config, nav_task, max_steps=max_steps, render_mode=render_mode)


def make_env_factory(**kwargs) -> Callable[[], WarehouseNavigationEnv]:
    return lambda: build_route_env(**kwargs)
