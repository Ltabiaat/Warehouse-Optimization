import unittest

from warehouse_mvp.layout_loader import warehouse_config_from_dict
from warehouse_mvp.order_task_models import TaskSequence
from warehouse_mvp.task_sequence_adapter import sequence_to_navigation_task


class TestTaskSequenceAdapter(unittest.TestCase):
    def test_sequence_to_navigation_task_extracts_zone_steps(self):
        config = warehouse_config_from_dict(
            {
                "warehouse_name": "Demo",
                "width": 5,
                "height": 5,
                "forklift_count": 1,
                "blocked_cells": [],
                "zone_cells": [
                    {"x": 1, "y": 1, "zone": "A"},
                    {"x": 4, "y": 4, "zone": "OUT"},
                ],
                "start_cells": [{"x": 0, "y": 0}],
                "inbound_docks": [],
                "outbound_docks": [],
            }
        )
        seq = TaskSequence(task_id="t1", steps=("pickup:A", "process:QC", "dropoff:OUT"))
        nav = sequence_to_navigation_task(config, seq)
        self.assertEqual((nav.start.x, nav.start.y), (0, 0))
        self.assertEqual(nav.target_zones, ("A", "QC", "OUT"))


if __name__ == "__main__":
    unittest.main()
