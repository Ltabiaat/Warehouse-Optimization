from __future__ import annotations

from .layout_models import NavigationTask, WarehouseConfig
from .order_task_models import TaskSequence
from .topology import first_reachable_cell


PREFIX_TO_ZONE = {
    "pickup": True,
    "process": True,
    "dropoff": True,
}


def sequence_to_navigation_task(config: WarehouseConfig, sequence: TaskSequence) -> NavigationTask:
    target_zones: list[str] = []
    for step in sequence.steps:
        prefix, _, value = step.partition(":")
        if prefix in PREFIX_TO_ZONE and value:
            target_zones.append(value.upper())

    if not target_zones:
        raise ValueError(f"Task sequence {sequence.task_id} has no zone-addressable steps")

    start = config.start_cells[0] if config.start_cells else first_reachable_cell(config)
    return NavigationTask(start=start, target_zones=tuple(target_zones))
