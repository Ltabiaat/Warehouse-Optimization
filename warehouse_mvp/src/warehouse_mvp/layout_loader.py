from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .layout_models import Cell, WarehouseConfig, ZoneCell


class LayoutValidationError(ValueError):
    pass


def load_layout_config(path: str | Path) -> WarehouseConfig:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return warehouse_config_from_dict(data)


def warehouse_config_from_dict(data: dict[str, Any]) -> WarehouseConfig:
    required = ["warehouse_name", "width", "height", "forklift_count", "blocked_cells", "zone_cells"]
    missing = [field for field in required if field not in data]
    if missing:
        raise LayoutValidationError(f"Missing required fields: {missing}")

    width = int(data["width"])
    height = int(data["height"])
    forklift_count = int(data["forklift_count"])
    if width <= 0 or height <= 0:
        raise LayoutValidationError("width and height must be positive")
    if forklift_count <= 0:
        raise LayoutValidationError("forklift_count must be positive")

    blocked_cells = frozenset(_parse_cell(cell, width, height) for cell in data["blocked_cells"])
    zone_cells = tuple(_parse_zone_cell(cell, width, height) for cell in data["zone_cells"])

    blocked_xy = {(c.x, c.y) for c in blocked_cells}
    for zc in zone_cells:
        if (zc.x, zc.y) in blocked_xy:
            raise LayoutValidationError(f"Zone cell overlaps blocked cell at {(zc.x, zc.y)}")

    return WarehouseConfig(
        warehouse_name=str(data["warehouse_name"]),
        width=width,
        height=height,
        forklift_count=forklift_count,
        blocked_cells=blocked_cells,
        zone_cells=zone_cells,
    )


def _parse_cell(cell: dict[str, Any], width: int, height: int) -> Cell:
    x = int(cell["x"])
    y = int(cell["y"])
    _validate_bounds(x, y, width, height)
    return Cell(x=x, y=y)


def _parse_zone_cell(cell: dict[str, Any], width: int, height: int) -> ZoneCell:
    x = int(cell["x"])
    y = int(cell["y"])
    zone = str(cell["zone"]).strip().upper()
    if not zone:
        raise LayoutValidationError("Zone cell must have non-empty zone")
    _validate_bounds(x, y, width, height)
    return ZoneCell(x=x, y=y, zone=zone)


def _validate_bounds(x: int, y: int, width: int, height: int) -> None:
    if not (0 <= x < width and 0 <= y < height):
        raise LayoutValidationError(f"Cell {(x, y)} out of bounds for {width}x{height}")
