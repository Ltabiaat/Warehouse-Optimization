import unittest

from warehouse_mvp.layout_loader import warehouse_config_from_dict
from warehouse_mvp.tasks import make_simple_zone_task

try:
    from warehouse_mvp.gym_env import WarehouseNavigationEnv
    GYM_AVAILABLE = True
except ImportError:
    GYM_AVAILABLE = False


@unittest.skipUnless(GYM_AVAILABLE, "gymnasium not installed")
class TestLayoutEnvDemo(unittest.TestCase):
    def test_demo_like_task_can_reach_target_sequence(self):
        config = warehouse_config_from_dict(
            {
                "warehouse_name": "Demo Warehouse",
                "width": 6,
                "height": 5,
                "forklift_count": 2,
                "blocked_cells": [
                    {"x": 2, "y": 1},
                    {"x": 2, "y": 2},
                    {"x": 2, "y": 3},
                ],
                "zone_cells": [
                    {"x": 5, "y": 0, "zone": "A"},
                    {"x": 5, "y": 4, "zone": "C"},
                ],
                "start_cells": [{"x": 0, "y": 0}],
                "inbound_docks": [{"x": 0, "y": 4}],
                "outbound_docks": [{"x": 5, "y": 4}],
            }
        )
        task = make_simple_zone_task(config, ["A", "C"])
        env = WarehouseNavigationEnv(config, task, max_steps=50)
        env.reset()

        actions = [3, 3, 3, 3, 3, 1, 1, 1, 1]
        terminated = False
        for action in actions:
            _, _, terminated, truncated, _ = env.step(action)
            if terminated or truncated:
                break

        self.assertTrue(terminated)


if __name__ == "__main__":
    unittest.main()
