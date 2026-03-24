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


@dataclass
class StepResult:
    observation: dict[str, Any]
    reward: float
    terminated: bool
    truncated: bool
    info: dict[str, Any]


class WarehouseNavigationEnv(gym.Env if gym is not None else object):
    metadata = {"render_modes": ["ansi"]}

    def __init__(
        self,
        config: WarehouseConfig,
        task: NavigationTask,
        max_steps: int = 200,
    ) -> None:
        if gym is None or spaces is None:
            raise ImportError("gymnasium is required to use WarehouseNavigationEnv")

        super().__init__()
        self.config = config
        self.task = task
        self.topology: WarehouseTopology = build_topology(config)
        self.max_steps = max_steps

        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Dict(
            {
                "forklift_position": spaces.Box(low=0, high=max(config.width, config.height), shape=(2,), dtype=int),
                "current_target_index": spaces.Discrete(max(1, len(task.target_zones))),
                "blocked_mask": spaces.Box(low=0, high=1, shape=(config.height, config.width), dtype=int),
                "zone_mask": spaces.Box(low=0, high=1, shape=(config.height, config.width), dtype=int),
            }
        )

        self.current_position: Cell = task.start
        self.current_target_index = 0
        self.steps_taken = 0

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
        info = self._info()

        dx, dy = ACTION_TO_DELTA[action]
        candidate = Cell(self.current_position.x + dx, self.current_position.y + dy)

        if action == 4:
            reward -= 0.5
        elif candidate not in self.topology.reachable_cells:
            reward -= 5.0
            info["invalid_move"] = True
        else:
            self.current_position = candidate
            info["invalid_move"] = False

        if self._is_in_current_target_zone():
            reward += 10.0
            self.current_target_index += 1
            info["zone_reached"] = True
        else:
            info["zone_reached"] = False

        if self.current_target_index >= len(self.task.target_zones):
            reward += 50.0
            terminated = True

        if self.steps_taken >= self.max_steps:
            truncated = True

        return self._observation(), reward, terminated, truncated, self._info() | info

    def render(self):
        rows: list[str] = []
        blocked = {(c.x, c.y) for c in self.config.blocked_cells}
        zone_lookup = {(zc.x, zc.y): zc.zone for zc in self.config.zone_cells}

        for y in range(self.config.height):
            row = []
            for x in range(self.config.width):
                if (x, y) == (self.current_position.x, self.current_position.y):
                    row.append("F")
                elif (x, y) in blocked:
                    row.append("X")
                elif (x, y) in zone_lookup:
                    row.append(zone_lookup[(x, y)])
                else:
                    row.append(".")
            rows.append(" ".join(row))
        return "\n".join(rows)

    def _observation(self) -> dict[str, Any]:
        return {
            "forklift_position": [self.current_position.x, self.current_position.y],
            "current_target_index": min(self.current_target_index, max(0, len(self.task.target_zones) - 1)),
            "blocked_mask": self._blocked_mask(),
            "zone_mask": self._current_zone_mask(),
        }

    def _blocked_mask(self) -> list[list[int]]:
        blocked = {(c.x, c.y) for c in self.config.blocked_cells}
        return [[1 if (x, y) in blocked else 0 for x in range(self.config.width)] for y in range(self.config.height)]

    def _current_zone_mask(self) -> list[list[int]]:
        if self.current_target_index >= len(self.task.target_zones):
            return [[0 for _ in range(self.config.width)] for _ in range(self.config.height)]
        zone = self.task.target_zones[self.current_target_index]
        zone_cells = {(c.x, c.y) for c in self.topology.zone_to_cells.get(zone, ())}
        return [[1 if (x, y) in zone_cells else 0 for x in range(self.config.width)] for y in range(self.config.height)]

    def _is_in_current_target_zone(self) -> bool:
        if self.current_target_index >= len(self.task.target_zones):
            return False
        zone = self.task.target_zones[self.current_target_index]
        target_cells = {(c.x, c.y) for c in self.topology.zone_to_cells.get(zone, ())}
        return (self.current_position.x, self.current_position.y) in target_cells

    def _info(self) -> dict[str, Any]:
        target_zone = None
        if self.current_target_index < len(self.task.target_zones):
            target_zone = self.task.target_zones[self.current_target_index]
        return {
            "steps_taken": self.steps_taken,
            "current_position": {"x": self.current_position.x, "y": self.current_position.y},
            "current_target_zone": target_zone,
        }
