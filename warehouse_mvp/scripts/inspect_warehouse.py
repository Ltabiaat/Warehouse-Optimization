"""
Inspect a warehouse layout in the Gymnasium environment.

Usage:
    python inspect_warehouse.py [--layout PATH]

Defaults to the Case Study D layout. Press Q or close the window to exit.
"""
from __future__ import annotations

import argparse
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DEFAULT_LAYOUT = BASE / "output" / "case_study_d_layout.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect a warehouse layout")
    parser.add_argument(
        "--layout",
        default=str(DEFAULT_LAYOUT),
        help="Path to layout JSON (default: case_study_d_layout.json)",
    )
    args = parser.parse_args()

    import sys
    sys.path.insert(0, str(BASE / "src"))

    from warehouse_mvp.layout_loader import load_layout_config
    from warehouse_mvp.layout_models import Cell, NavigationTask
    from warehouse_mvp.gym_env import WarehouseNavigationEnv

    config = load_layout_config(args.layout)

    # Find a valid 2×2 start position (top-left corner must be free)
    from warehouse_mvp.topology import build_topology
    topology = build_topology(config)
    start = Cell(2, 2)
    for cell in sorted(topology.reachable_cells, key=lambda c: (c.x, c.y)):
        if (
            Cell(cell.x + 1, cell.y) in topology.reachable_cells
            and Cell(cell.x, cell.y + 1) in topology.reachable_cells
            and Cell(cell.x + 1, cell.y + 1) in topology.reachable_cells
        ):
            start = cell
            break

    # No task — pure layout inspection
    task = NavigationTask(start=start, target_zones=())
    env = WarehouseNavigationEnv(config, task, max_steps=999_999, render_mode="human")
    env.reset()

    print(f"Warehouse : {config.warehouse_name}")
    print(f"Grid      : {config.width} x {config.height}  ({config.width * config.height:,} cells = sq m)")
    print(f"Blocked   : {len(config.blocked_cells):,} cells (walls)")
    open_cells = config.width * config.height - len(config.blocked_cells)
    print(f"Open floor: {open_cells:,} m²")
    print(f"Forklift  : 2×2 footprint, starting at ({start.x},{start.y})")
    print("Close the window or press Q to exit.")

    import pygame
    running = True
    while running:
        env.render()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                # Arrow keys let you nudge the forklift for visual inspection
                elif event.key == pygame.K_UP:
                    env.step(0)
                elif event.key == pygame.K_DOWN:
                    env.step(1)
                elif event.key == pygame.K_LEFT:
                    env.step(2)
                elif event.key == pygame.K_RIGHT:
                    env.step(3)

    env.close()


if __name__ == "__main__":
    main()
