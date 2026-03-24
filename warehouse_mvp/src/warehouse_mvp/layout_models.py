from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Cell:
    x: int
    y: int


@dataclass(frozen=True)
class ZoneCell:
    x: int
    y: int
    zone: str


@dataclass(frozen=True)
class WarehouseConfig:
    warehouse_name: str
    width: int
    height: int
    forklift_count: int
    blocked_cells: frozenset[Cell]
    zone_cells: tuple[ZoneCell, ...]
    start_cells: tuple[Cell, ...]
    inbound_docks: tuple[Cell, ...]
    outbound_docks: tuple[Cell, ...]


@dataclass(frozen=True)
class NavigationTask:
    start: Cell
    target_zones: tuple[str, ...]
