import json
import tempfile
import unittest
from pathlib import Path

from warehouse_mvp.layout_loader import LayoutValidationError, load_layout_config, warehouse_config_from_dict
from warehouse_mvp.tasks import make_simple_zone_task
from warehouse_mvp.topology import build_topology, first_reachable_cell


class TestLayoutPipeline(unittest.TestCase):
    def test_layout_loader_parses_valid_config(self):
        data = {
            "warehouse_name": "Demo",
            "width": 4,
            "height": 3,
            "forklift_count": 2,
            "blocked_cells": [{"x": 1, "y": 1}],
            "zone_cells": [{"x": 3, "y": 2, "zone": "A"}],
        }
        config = warehouse_config_from_dict(data)
        self.assertEqual(config.width, 4)
        self.assertEqual(config.height, 3)
        self.assertEqual(config.forklift_count, 2)
        self.assertEqual(len(config.blocked_cells), 1)
        self.assertEqual(len(config.zone_cells), 1)

    def test_layout_loader_rejects_zone_on_blocked_cell(self):
        data = {
            "warehouse_name": "Demo",
            "width": 4,
            "height": 3,
            "forklift_count": 2,
            "blocked_cells": [{"x": 1, "y": 1}],
            "zone_cells": [{"x": 1, "y": 1, "zone": "A"}],
        }
        with self.assertRaises(LayoutValidationError):
            warehouse_config_from_dict(data)

    def test_topology_builder_creates_adjacency(self):
        config = warehouse_config_from_dict(
            {
                "warehouse_name": "Demo",
                "width": 3,
                "height": 3,
                "forklift_count": 1,
                "blocked_cells": [{"x": 1, "y": 1}],
                "zone_cells": [{"x": 2, "y": 2, "zone": "C"}],
            }
        )
        topology = build_topology(config)
        start = first_reachable_cell(config)
        self.assertIn(start, topology.adjacency_map)
        self.assertIn("C", topology.zone_to_cells)

    def test_task_builder_uses_first_reachable_cell(self):
        config = warehouse_config_from_dict(
            {
                "warehouse_name": "Demo",
                "width": 2,
                "height": 2,
                "forklift_count": 1,
                "blocked_cells": [{"x": 0, "y": 0}],
                "zone_cells": [{"x": 1, "y": 1, "zone": "A"}],
            }
        )
        task = make_simple_zone_task(config, ["A", "C"])
        self.assertEqual(task.start.x, 1)
        self.assertEqual(task.start.y, 0)
        self.assertEqual(task.target_zones, ("A", "C"))

    def test_load_layout_config_reads_json_file(self):
        payload = {
            "warehouse_name": "Saved Layout",
            "width": 5,
            "height": 5,
            "forklift_count": 3,
            "blocked_cells": [{"x": 2, "y": 2}],
            "zone_cells": [{"x": 4, "y": 4, "zone": "B"}],
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "layout.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            config = load_layout_config(path)
            self.assertEqual(config.warehouse_name, "Saved Layout")
            self.assertEqual(config.forklift_count, 3)


if __name__ == "__main__":
    unittest.main()
