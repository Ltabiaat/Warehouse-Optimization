import unittest

from warehouse_mvp.normalizer import normalize_row
from warehouse_mvp.sales_summary import summarize_sales


class TestSalesSummary(unittest.TestCase):
    def test_summarize_sales_groups_by_item(self):
        rows = [
            normalize_row(
                {
                    "商品コード": "SKU-001",
                    "商品名１": "Item 1",
                    "伝票日付": "2026/03/24",
                    "入出庫伝票№": "SLIP-1",
                    "取引区分略称": "出庫",
                    "ロット№": "LOT-1",
                    "ロケーション№": "A-01",
                    "単位名": "EA",
                    "入庫数量": "0",
                    "出庫数量": "4",
                    "ﾀｲﾑｽﾀﾝﾌﾟ（時間）": "09:00",
                    "ﾀｲﾑｽﾀﾝﾌﾟ（日付）": "2026/03/24",
                    "担当者コード": "OP1",
                    "クライアントＩＤ": "C1",
                }
            ).data,
            normalize_row(
                {
                    "商品コード": "SKU-001",
                    "商品名１": "Item 1",
                    "伝票日付": "2026/03/24",
                    "入出庫伝票№": "SLIP-2",
                    "取引区分略称": "出庫",
                    "ロット№": "LOT-1",
                    "ロケーション№": "A-02",
                    "単位名": "EA",
                    "入庫数量": "0",
                    "出庫数量": "3",
                    "ﾀｲﾑｽﾀﾝﾌﾟ（時間）": "10:00",
                    "ﾀｲﾑｽﾀﾝﾌﾟ（日付）": "2026/03/24",
                    "担当者コード": "OP2",
                    "クライアントＩＤ": "C2",
                }
            ).data,
        ]

        summary = summarize_sales(rows)
        self.assertEqual(len(summary), 1)
        self.assertEqual(summary[0]["item_code"], "SKU-001")
        self.assertEqual(summary[0]["total_qty_out"], "7")
        self.assertEqual(summary[0]["outbound_event_count"], 2)
        self.assertEqual(summary[0]["distinct_clients"], 2)
        self.assertEqual(summary[0]["distinct_locations"], 2)


if __name__ == "__main__":
    unittest.main()
