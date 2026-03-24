from __future__ import annotations

from .layout_models import NavigationTask, WarehouseConfig
from .topology import first_reachable_cell


def make_simple_zone_task(config: WarehouseConfig, target_zones: list[str]) -> NavigationTask:
    start = config.start_cells[0] if config.start_cells else first_reachable_cell(config)
    return NavigationTask(start=start, target_zones=tuple(zone.upper() for zone in target_zones))
