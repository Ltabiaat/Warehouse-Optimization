from __future__ import annotations

from dataclasses import dataclass

from .layout_models import Cell, WarehouseConfig, ZoneCell


@dataclass(frozen=True)
class WarehouseTopology:
    reachable_cells: frozenset[Cell]
    blocked_cells: frozenset[Cell]
    zone_to_cells: dict[str, tuple[Cell, ...]]
    adjacency_map: dict[Cell, tuple[Cell, ...]]


def build_topology(config: WarehouseConfig) -> WarehouseTopology:
    blocked = config.blocked_cells
    all_cells = {Cell(x, y) for y in range(config.height) for x in range(config.width)}
    reachable = frozenset(cell for cell in all_cells if cell not in blocked)

    zone_to_cells: dict[str, list[Cell]] = {}
    for zc in config.zone_cells:
        zone_to_cells.setdefault(zc.zone, []).append(Cell(zc.x, zc.y))

    adjacency_map: dict[Cell, tuple[Cell, ...]] = {}
    for cell in reachable:
        neighbors = []
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            n = Cell(cell.x + dx, cell.y + dy)
            if n in reachable:
                neighbors.append(n)
        adjacency_map[cell] = tuple(neighbors)

    return WarehouseTopology(
        reachable_cells=reachable,
        blocked_cells=blocked,
        zone_to_cells={k: tuple(v) for k, v in sorted(zone_to_cells.items())},
        adjacency_map=adjacency_map,
    )


def first_reachable_cell(config: WarehouseConfig) -> Cell:
    for y in range(config.height):
        for x in range(config.width):
            cell = Cell(x, y)
            if cell not in config.blocked_cells:
                return cell
    raise ValueError("No reachable cells in warehouse config")
