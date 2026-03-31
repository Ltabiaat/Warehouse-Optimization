from __future__ import annotations

from dataclasses import dataclass
from typing import Any

try:
    import gymnasium as gym
    from gymnasium import spaces
except ImportError:  # pragma: no cover
    gym = None
    spaces = None

from .layout_models import Cell, NavigationTask, WarehouseConfig
from .topology import WarehouseTopology, build_topology


ACTION_TO_DELTA = {
    0: (0, -1),  # up
    1: (0, 1),   # down
    2: (-1, 0),  # left
    3: (1, 0),   # right
    4: (0, 0),   # stay
}

# Forklift footprint: 2×2 cells (position = top-left corner)
FORKLIFT_W = 2
FORKLIFT_H = 2

# Distinct colours for up to 12 named zones
_ZONE_PALETTE = [
    (173, 216, 230),
    (144, 238, 144),
    (255, 255, 153),
    (255, 178, 102),
    (204, 153, 255),
    (255, 153, 204),
    (102, 205, 170),
    (255, 218, 185),
    (176, 224, 230),
    (240, 230, 140),
    (221, 160, 221),
    (152, 251, 152),
]


def _zone_color(zone: str, zone_index_map: dict[str, int]) -> tuple[int, int, int]:
    idx = zone_index_map.get(zone, 0)
    return _ZONE_PALETTE[idx % len(_ZONE_PALETTE)]


@dataclass
class StepResult:
    observation: dict[str, Any]
    reward: float
    terminated: bool
    truncated: bool
    info: dict[str, Any]


class WarehouseNavigationEnv(gym.Env if gym is not None else object):
    metadata = {"render_modes": ["ansi", "human"]}

    def __init__(
        self,
        config: WarehouseConfig,
        task: NavigationTask,
        max_steps: int = 200,
        render_mode: str | None = None,
    ) -> None:
        if gym is None or spaces is None:
            raise ImportError("gymnasium is required to use WarehouseNavigationEnv")

        super().__init__()
        self.config = config
        self.task = task
        self.topology: WarehouseTopology = build_topology(config)
        self.max_steps = max_steps
        self.render_mode = render_mode

        unique_zones = list(dict.fromkeys(zc.zone for zc in config.zone_cells))
        self._zone_index_map: dict[str, int] = {z: i for i, z in enumerate(unique_zones)}

        # Pygame state — lazily initialised on first human render
        self._screen: Any = None
        self._clock: Any = None
        self._font: Any = None
        self._cell_size: int = 0  # computed once on first render

        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Dict(
            {
                "forklift_position": spaces.Box(
                    low=0, high=max(config.width, config.height), shape=(2,), dtype=int
                ),
                "current_target_index": spaces.Discrete(max(1, len(task.target_zones))),
                "blocked_mask": spaces.Box(
                    low=0, high=1, shape=(config.height, config.width), dtype=int
                ),
                "zone_mask": spaces.Box(
                    low=0, high=1, shape=(config.height, config.width), dtype=int
                ),
            }
        )

        self.current_position: Cell = task.start
        self.current_target_index = 0
        self.steps_taken = 0

    # ------------------------------------------------------------------
    # Footprint helpers
    # ------------------------------------------------------------------

    def _footprint(self, pos: Cell) -> frozenset[tuple[int, int]]:
        """Return the 4 grid cells occupied by the 2×2 forklift at pos."""
        return frozenset(
            (pos.x + dx, pos.y + dy)
            for dx in range(FORKLIFT_W)
            for dy in range(FORKLIFT_H)
        )

    def _footprint_valid(self, pos: Cell) -> bool:
        """True if every cell of the 2×2 footprint is reachable."""
        return all(Cell(x, y) in self.topology.reachable_cells for x, y in self._footprint(pos))

    # ------------------------------------------------------------------
    # Gym interface
    # ------------------------------------------------------------------

    def reset(self, *, seed: int | None = None, options: dict[str, Any] | None = None):
        super().reset(seed=seed)
        self.current_position = self.task.start
        self.current_target_index = 0
        self.steps_taken = 0
        return self._observation(), self._info()

    def step(self, action: int):
        if action not in ACTION_TO_DELTA:
            raise ValueError(f"Invalid action: {action}")

        self.steps_taken += 1
        reward = -1.0
        terminated = False
        truncated = False
        extra_info: dict[str, Any] = {}

        dx, dy = ACTION_TO_DELTA[action]
        candidate = Cell(self.current_position.x + dx, self.current_position.y + dy)

        if action == 4:
            reward -= 0.5
        elif not self._footprint_valid(candidate):
            reward -= 5.0
            extra_info["invalid_move"] = True
        else:
            self.current_position = candidate
            extra_info["invalid_move"] = False

        if self._is_in_current_target_zone():
            reward += 10.0
            self.current_target_index += 1
            extra_info["zone_reached"] = True
        else:
            extra_info["zone_reached"] = False

        if self.current_target_index >= len(self.task.target_zones):
            reward += 50.0
            terminated = True

        if self.steps_taken >= self.max_steps:
            truncated = True

        return self._observation(), reward, terminated, truncated, self._info() | extra_info

    # ------------------------------------------------------------------
    # Render
    # ------------------------------------------------------------------

    def render(self):
        if self.render_mode == "human":
            self._render_human()
            return
        return self._render_ansi()

    def _render_ansi(self) -> str:
        rows: list[str] = []
        blocked = {(c.x, c.y) for c in self.config.blocked_cells}
        zone_lookup = {(zc.x, zc.y): zc.zone for zc in self.config.zone_cells}
        footprint = self._footprint(self.current_position)

        for y in range(self.config.height):
            row = []
            for x in range(self.config.width):
                if (x, y) in footprint:
                    row.append("F")
                elif (x, y) in blocked:
                    row.append("X")
                elif (x, y) in zone_lookup:
                    row.append(zone_lookup[(x, y)])
                else:
                    row.append(".")
            rows.append(" ".join(row))
        return "\n".join(rows)

    def _render_human(self) -> None:
        try:
            import pygame
        except ImportError as exc:
            raise ImportError(
                "pygame is required for render_mode='human'. Run: pip install pygame"
            ) from exc

        # Compute cell size once: fit the grid in ~1400×900 px
        if self._cell_size == 0:
            self._cell_size = max(
                4,
                min(64, min(1400 // self.config.width, 900 // self.config.height)),
            )

        CELL = self._cell_size
        PANEL_H = 72
        W = self.config.width * CELL
        H = self.config.height * CELL + PANEL_H

        C_FLOOR    = (245, 245, 245)
        C_WALL     = (55,  55,  55)
        C_GRID     = (180, 180, 180)
        C_TARGET   = (255, 140,  0)
        C_DONE     = (160, 210, 160)
        C_DOCK_IN  = (100, 180, 255)
        C_DOCK_OUT = (255, 100, 100)
        C_AGENT    = (255, 220,  0)
        C_PANEL    = (30,  30,  30)
        C_TEXT     = (255, 255, 255)
        C_SUBTEXT  = (180, 180, 180)

        if self._screen is None:
            pygame.init()
            self._screen = pygame.display.set_mode((W, H))
            pygame.display.set_caption(f"Warehouse: {self.config.warehouse_name}")
            self._font  = pygame.font.SysFont("monospace", max(9, CELL - 2))
            self._clock = pygame.time.Clock()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
                return

        self._screen.fill(C_WALL)  # default background = wall colour

        blocked     = {(c.x, c.y) for c in self.config.blocked_cells}
        zone_lookup = {(zc.x, zc.y): zc.zone for zc in self.config.zone_cells}
        inbound     = {(c.x, c.y) for c in self.config.inbound_docks}
        outbound    = {(c.x, c.y) for c in self.config.outbound_docks}
        footprint   = self._footprint(self.current_position)

        current_zone = (
            self.task.target_zones[self.current_target_index]
            if self.current_target_index < len(self.task.target_zones)
            else None
        )
        target_cells = {
            (c.x, c.y) for c in self.topology.zone_to_cells.get(current_zone, ())
        } if current_zone else set()
        completed_zones = set(self.task.target_zones[: self.current_target_index])

        # Draw every cell
        for y in range(self.config.height):
            for x in range(self.config.width):
                if (x, y) in blocked:
                    continue  # already wall-coloured background
                rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)

                if (x, y) in target_cells:
                    color = C_TARGET
                elif (x, y) in inbound:
                    color = C_DOCK_IN
                elif (x, y) in outbound:
                    color = C_DOCK_OUT
                elif (x, y) in zone_lookup:
                    zone = zone_lookup[(x, y)]
                    color = C_DONE if zone in completed_zones else _zone_color(zone, self._zone_index_map)
                else:
                    color = C_FLOOR

                pygame.draw.rect(self._screen, color, rect)

                # Grid lines only if cells are large enough to benefit
                if CELL >= 8:
                    pygame.draw.rect(self._screen, C_GRID, rect, 1)

                # Labels only if cells are big enough to read
                if CELL >= 14:
                    label_text = None
                    if (x, y) in zone_lookup:
                        label_text = zone_lookup[(x, y)]
                    if (x, y) in inbound:
                        label_text = "IN"
                    elif (x, y) in outbound:
                        label_text = "OUT"
                    if label_text:
                        lbl = self._font.render(label_text, True, (60, 60, 60))
                        self._screen.blit(lbl, (x * CELL + 2, y * CELL + 2))

        # Draw 2×2 forklift
        fx, fy = self.current_position.x, self.current_position.y
        pad = max(1, CELL // 8)
        agent_rect = pygame.Rect(
            fx * CELL + pad,
            fy * CELL + pad,
            FORKLIFT_W * CELL - pad * 2,
            FORKLIFT_H * CELL - pad * 2,
        )
        pygame.draw.rect(self._screen, C_AGENT, agent_rect, border_radius=max(2, CELL // 6))
        if CELL >= 8:
            lbl = self._font.render("F", True, (0, 0, 0))
            cx = fx * CELL + FORKLIFT_W * CELL // 2 - lbl.get_width() // 2
            cy = fy * CELL + FORKLIFT_H * CELL // 2 - lbl.get_height() // 2
            self._screen.blit(lbl, (cx, cy))

        # Info panel
        panel_top = self.config.height * CELL
        pygame.draw.rect(self._screen, C_PANEL, pygame.Rect(0, panel_top, W, PANEL_H))

        if self.task.target_zones:
            parts: list[str] = []
            for i, z in enumerate(self.task.target_zones):
                if i < self.current_target_index:
                    parts.append(f"[{z}]")
                elif i == self.current_target_index:
                    parts.append(f">{z}<")
                else:
                    parts.append(z)
            task_str = " -> ".join(parts)
        else:
            task_str = "Inspection mode — no task assigned"

        self._screen.blit(
            self._font.render(f"Task:  {task_str}", True, C_TEXT),
            (10, panel_top + 10),
        )
        self._screen.blit(
            self._font.render(
                f"Step: {self.steps_taken}/{self.max_steps}   "
                f"Position: ({self.current_position.x},{self.current_position.y})   "
                f"Target: {current_zone or 'DONE'}",
                True, C_SUBTEXT,
            ),
            (10, panel_top + 36),
        )

        pygame.display.flip()
        self._clock.tick(30)

    def close(self) -> None:
        if self._screen is not None:
            try:
                import pygame
                pygame.quit()
            except Exception:
                pass
            self._screen = None
            self._clock = None
            self._font = None
            self._cell_size = 0

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _observation(self) -> dict[str, Any]:
        return {
            "forklift_position": [self.current_position.x, self.current_position.y],
            "current_target_index": min(
                self.current_target_index, max(0, len(self.task.target_zones) - 1)
            ),
            "blocked_mask": self._blocked_mask(),
            "zone_mask": self._current_zone_mask(),
        }

    def _blocked_mask(self) -> list[list[int]]:
        blocked = {(c.x, c.y) for c in self.config.blocked_cells}
        return [
            [1 if (x, y) in blocked else 0 for x in range(self.config.width)]
            for y in range(self.config.height)
        ]

    def _current_zone_mask(self) -> list[list[int]]:
        if self.current_target_index >= len(self.task.target_zones):
            return [[0] * self.config.width for _ in range(self.config.height)]
        zone = self.task.target_zones[self.current_target_index]
        zone_cells = {(c.x, c.y) for c in self.topology.zone_to_cells.get(zone, ())}
        return [
            [1 if (x, y) in zone_cells else 0 for x in range(self.config.width)]
            for y in range(self.config.height)
        ]

    def _is_in_current_target_zone(self) -> bool:
        if self.current_target_index >= len(self.task.target_zones):
            return False
        zone = self.task.target_zones[self.current_target_index]
        target_cells = {(c.x, c.y) for c in self.topology.zone_to_cells.get(zone, ())}
        return bool(self._footprint(self.current_position) & target_cells)

    def _info(self) -> dict[str, Any]:
        target_zone = None
        if self.current_target_index < len(self.task.target_zones):
            target_zone = self.task.target_zones[self.current_target_index]
        return {
            "steps_taken": self.steps_taken,
            "current_position": {"x": self.current_position.x, "y": self.current_position.y},
            "current_target_zone": target_zone,
        }
