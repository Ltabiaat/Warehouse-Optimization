import unittest

from warehouse_mvp.normalizer import normalize_row
from warehouse_mvp.order_task_generator import generate_outbound_tasks, task_to_sequence


class TestOrderTaskGenerator(unittest.TestCase):
    def test_generate_outbound_tasks_filters_to_qty_out_rows(self):
        rows = [
            normalize_row(
                {
                    "商品コード": "SKU-001",
                    "商品名１": "Item 1",
                    "伝票日付": "2026/03/24",
                    "入出庫伝票№": "SLIP-1",
                    "取引区分略称": "出庫",
                    "ロット№": "LOT-1",
                    "ロケーション№": "LOC-A",
                    "フロアコード": "A",
                    "単位名": "EA",
                    "入庫数量": "0",
                    "出庫数量": "4",
                    "ﾀｲﾑｽﾀﾝﾌﾟ（時間）": "09:00",
                    "ﾀｲﾑｽﾀﾝﾌﾟ（日付）": "2026/03/24",
                    "担当者コード": "OP1",
                    "クライアントＩＤ": "C1",
                    "消費期限": "2026/04/01",
                }
            ).data,
            normalize_row(
                {
                    "商品コード": "SKU-002",
                    "商品名１": "Item 2",
                    "伝票日付": "2026/03/24",
                    "入出庫伝票№": "SLIP-2",
                    "取引区分略称": "入庫",
                    "ロット№": "LOT-2",
                    "ロケーション№": "LOC-B",
                    "フロアコード": "B",
                    "単位名": "EA",
                    "入庫数量": "10",
                    "出庫数量": "0",
                    "ﾀｲﾑｽﾀﾝﾌﾟ（時間）": "09:10",
                    "ﾀｲﾑｽﾀﾝﾌﾟ（日付）": "2026/03/24",
                    "担当者コード": "OP2",
                    "クライアントＩＤ": "C1",
                }
            ).data,
        ]

        tasks = generate_outbound_tasks(rows, default_dropoff_zone="OUT")

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].item_code, "SKU-001")
        self.assertEqual(tasks[0].pickup_zone, "A")
        self.assertEqual(tasks[0].dropoff_zone, "OUT")
        self.assertEqual(tasks[0].source_type, "outbound")

    def test_task_to_sequence_builds_pick_process_dropoff_flow(self):
        row = normalize_row(
            {
                "商品コード": "SKU-001",
                "商品名１": "Item 1",
                "伝票日付": "2026/03/24",
                "入出庫伝票№": "SLIP-1",
                "取引区分略称": "出庫",
                "ロット№": "LOT-1",
                "ロケーション№": "LOC-A",
                "単位名": "EA",
                "入庫数量": "0",
                "出庫数量": "4",
                "ﾀｲﾑｽﾀﾝﾌﾟ（時間）": "09:00",
                "ﾀｲﾑｽﾀﾝﾌﾟ（日付）": "2026/03/24",
                "担当者コード": "OP1",
                "クライアントＩＤ": "C1",
            }
        ).data

        task = generate_outbound_tasks(
            [row],
            location_to_zone={"LOC-A": "A"},
            processing_zone_by_item={"SKU-001": "QC"},
            default_dropoff_zone="OUT",
        )[0]
        sequence = task_to_sequence(task)

        self.assertEqual(sequence.steps, ("pickup:A", "process:QC", "dropoff:OUT"))


if __name__ == "__main__":
    unittest.main()
