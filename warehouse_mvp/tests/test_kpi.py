import unittest

from warehouse_mvp.kpi import summarize_kpis
from warehouse_mvp.normalizer import normalize_row


class TestKpi(unittest.TestCase):
    def test_summarize_kpis_counts_basic_metrics(self):
        rows = [
            normalize_row(
                {
                    "商品コード": "SKU-001",
                    "伝票日付": "2026/03/24",
                    "入出庫伝票№": "SLIP-1",
                    "取引区分略称": "入庫",
                    "ロット№": "LOT-1",
                    "ロケーション№": "A-01",
                    "単位名": "EA",
                    "入庫数量": "10",
                    "出庫数量": "0",
                    "ﾀｲﾑｽﾀﾝﾌﾟ（時間）": "09:00",
                    "ﾀｲﾑｽﾀﾝﾌﾟ（日付）": "2026/03/24",
                    "担当者コード": "OP1",
                    "クライアントＩＤ": "C1",
                    "消費期限": "2026/04/01",
                }
            ).data,
            normalize_row(
                {
                    "商品コード": "SKU-001",
                    "伝票日付": "2026/03/24",
                    "入出庫伝票№": "SLIP-2",
                    "取引区分略称": "出庫",
                    "ロット№": "LOT-1",
                    "ロケーション№": "A-01",
                    "単位名": "EA",
                    "入庫数量": "0",
                    "出庫数量": "4",
                    "ﾀｲﾑｽﾀﾝﾌﾟ（時間）": "10:00",
                    "ﾀｲﾑｽﾀﾝﾌﾟ（日付）": "2026/03/24",
                    "担当者コード": "OP2",
                    "クライアントＩＤ": "C1",
                }
            ).data,
        ]

        summary = summarize_kpis(rows)

        self.assertEqual(summary["total_rows"], 2)
        self.assertEqual(summary["unique_items"], 1)
        self.assertEqual(summary["unique_locations"], 1)
        self.assertEqual(summary["unique_operators"], 2)
        self.assertEqual(summary["total_qty_in"], "10")
        self.assertEqual(summary["total_qty_out"], "4")
        self.assertEqual(summary["net_movement"], "6")
        self.assertEqual(summary["movement_direction_counts"]["IN"], 1)
        self.assertEqual(summary["movement_direction_counts"]["OUT"], 1)


if __name__ == "__main__":
    unittest.main()
