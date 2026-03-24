import json
import tempfile
import unittest
from pathlib import Path

from warehouse_mvp.rl_env_factory import build_route_env


class TestRlEnvFactory(unittest.TestCase):
    def test_build_route_env_from_layout_and_csv(self):
        layout = {
            "warehouse_name": "Demo",
            "width": 6,
            "height": 5,
            "forklift_count": 1,
            "blocked_cells": [],
            "zone_cells": [
                {"x": 1, "y": 1, "zone": "A"},
                {"x": 2, "y": 2, "zone": "QC"},
                {"x": 5, "y": 4, "zone": "OUT"},
            ],
            "start_cells": [{"x": 0, "y": 0}],
            "inbound_docks": [],
            "outbound_docks": [{"x": 5, "y": 4}],
        }
        csv_text = "商品コード,商品名１,伝票日付,入出庫伝票№,取引区分略称,ロット№,フロアコード,ロケーション№,単位名,入庫数量,出庫数量,ﾀｲﾑｽﾀﾝﾌﾟ（時間）,ﾀｲﾑｽﾀﾝﾌﾟ（日付）,担当者コード,クライアントＩＤ\nSKU-001,Item 1,2026/03/24,SLIP-1,出庫,LOT-1,A,LOC-A,EA,0,4,09:00,2026/03/24,OP1,C1\n"
        with tempfile.TemporaryDirectory() as tmpdir:
            layout_path = Path(tmpdir) / "layout.json"
            csv_path = Path(tmpdir) / "warehouse.csv"
            layout_path.write_text(json.dumps(layout), encoding="utf-8")
            csv_path.write_text(csv_text, encoding="utf-8")
            env = build_route_env(
                layout_path=str(layout_path),
                warehouse_csv_path=str(csv_path),
                location_to_zone={"LOC-A": "A"},
                processing_zone_by_item={"SKU-001": "QC"},
                default_dropoff_zone="OUT",
            )
            obs, info = env.reset()
            self.assertEqual(obs["forklift_position"], [0, 0])
            self.assertEqual(info["current_target_zone"], "A")


if __name__ == "__main__":
    unittest.main()
