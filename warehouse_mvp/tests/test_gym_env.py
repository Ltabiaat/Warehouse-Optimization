import unittest

from warehouse_mvp.layout_loader import warehouse_config_from_dict
from warehouse_mvp.tasks import make_simple_zone_task

try:
    from warehouse_mvp.gym_env import WarehouseNavigationEnv
    GYM_AVAILABLE = True
except ImportError:
    GYM_AVAILABLE = False


@unittest.skipUnless(GYM_AVAILABLE, "gymnasium not installed")
class TestWarehouseNavigationEnv(unittest.TestCase):
    def test_reset_returns_initial_observation(self):
        config = warehouse_config_from_dict(
            {
                "warehouse_name": "Demo",
                "width": 4,
                "height": 3,
                "forklift_count": 1,
                "blocked_cells": [{"x": 1, "y": 1}],
                "zone_cells": [{"x": 3, "y": 2, "zone": "A"}],
                "start_cells": [{"x": 0, "y": 0}],
                "inbound_docks": [],
                "outbound_docks": [],
            }
        )
        task = make_simple_zone_task(config, ["A"])
        env = WarehouseNavigationEnv(config, task, max_steps=20)
        obs, info = env.reset()
        self.assertEqual(obs["forklift_position"], [0, 0])
        self.assertEqual(info["current_target_zone"], "A")

    def test_invalid_move_gets_penalty_and_no_position_change(self):
        config = warehouse_config_from_dict(
            {
                "warehouse_name": "Demo",
                "width": 3,
                "height": 3,
                "forklift_count": 1,
                "blocked_cells": [],
                "zone_cells": [{"x": 2, "y": 2, "zone": "A"}],
                "start_cells": [{"x": 0, "y": 0}],
                "inbound_docks": [],
                "outbound_docks": [],
            }
        )
        task = make_simple_zone_task(config, ["A"])
        env = WarehouseNavigationEnv(config, task, max_steps=20)
        env.reset()
        obs, reward, terminated, truncated, info = env.step(0)
        self.assertEqual(obs["forklift_position"], [0, 0])
        self.assertLess(reward, -1)
        self.assertFalse(terminated)
        self.assertFalse(truncated)
        self.assertTrue(info["invalid_move"])

    def test_reaching_zone_terminates_single_target_task(self):
        config = warehouse_config_from_dict(
            {
                "warehouse_name": "Demo",
                "width": 3,
                "height": 3,
                "forklift_count": 1,
                "blocked_cells": [],
                "zone_cells": [{"x": 1, "y": 0, "zone": "A"}],
                "start_cells": [{"x": 0, "y": 0}],
                "inbound_docks": [],
                "outbound_docks": [],
            }
        )
        task = make_simple_zone_task(config, ["A"])
        env = WarehouseNavigationEnv(config, task, max_steps=20)
        env.reset()
        obs, reward, terminated, truncated, info = env.step(3)
        self.assertEqual(obs["forklift_position"], [1, 0])
        self.assertTrue(terminated)
        self.assertFalse(truncated)
        self.assertTrue(info["zone_reached"])
        self.assertGreaterEqual(reward, 50)

    def test_render_returns_text_grid(self):
        config = warehouse_config_from_dict(
            {
                "warehouse_name": "Demo",
                "width": 2,
                "height": 2,
                "forklift_count": 1,
                "blocked_cells": [{"x": 1, "y": 1}],
                "zone_cells": [{"x": 1, "y": 0, "zone": "A"}],
                "start_cells": [{"x": 0, "y": 0}],
                "inbound_docks": [{"x": 0, "y": 1}],
                "outbound_docks": [],
            }
        )
        task = make_simple_zone_task(config, ["A"])
        env = WarehouseNavigationEnv(config, task, max_steps=20)
        env.reset()
        rendered = env.render()
        self.assertIn("F", rendered)
        self.assertIn("A", rendered)
        self.assertIn("X", rendered)


if __name__ == "__main__":
    unittest.main()
