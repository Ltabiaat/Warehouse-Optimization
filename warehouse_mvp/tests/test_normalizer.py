import unittest
from decimal import Decimal

from warehouse_mvp.normalizer import normalize_row, rename_source_fields


class TestNormalizer(unittest.TestCase):
    def test_rename_source_fields_maps_japanese_headers(self):
        row = {"商品コード": "ABC123", "ロケーション№": "A-01-01"}
        renamed = rename_source_fields(row)
        self.assertEqual(renamed["item_code"], "ABC123")
        self.assertEqual(renamed["location_no"], "A-01-01")

    def test_normalize_row_derives_core_fields(self):
        row = {
            "商品コード": "ABC123",
            "商品名１": "Test Item",
            "伝票日付": "2026/03/24",
            "入出庫伝票№": "SLIP-001",
            "取引区分略称": "出庫",
            "ロット№": "LOT-77",
            "入荷日": "2026/03/20",
            "消費期限": "2026/04/30",
            "フロアコード": "F1",
            "ロケーション№": "A-01-01",
            "単位名": "CS",
            "入庫数量": "0",
            "出庫数量": "12",
            "入庫数（バラ）": "0",
            "出庫数（バラ）": "24",
            "ﾀｲﾑｽﾀﾝﾌﾟ（時間）": "13:45:00",
            "ﾀｲﾑｽﾀﾝﾌﾟ（日付）": "2026/03/24",
            "担当者コード": "OP001",
            "担当者名": "Tanaka",
            "クライアントＩＤ": "CLIENT-9",
        }

        normalized = normalize_row(row).data

        self.assertEqual(normalized["item_code"], "ABC123")
        self.assertEqual(normalized["movement_qty"], Decimal("-12"))
        self.assertEqual(normalized["movement_direction"], "OUT")
        self.assertTrue(normalized["is_perishable"])
        self.assertEqual(normalized["location_group"], "F1")
        self.assertEqual(normalized["event_ts"].isoformat(), "2026-03-24T13:45:00")
        self.assertEqual(len(normalized["event_id"]), 16)

    def test_normalize_row_uses_location_prefix_when_floor_missing(self):
        row = {
            "商品コード": "ABC123",
            "伝票日付": "20260324",
            "入出庫伝票№": "SLIP-002",
            "取引区分略称": "入庫",
            "ロット№": "LOT-88",
            "ロケーション№": "Z-99-02",
            "単位名": "EA",
            "入庫数量": "5",
            "出庫数量": "0",
            "ﾀｲﾑｽﾀﾝﾌﾟ（時間）": "1345",
            "ﾀｲﾑｽﾀﾝﾌﾟ（日付）": "20260324",
            "担当者コード": "OP002",
            "クライアントＩＤ": "CLIENT-1",
        }

        normalized = normalize_row(row).data

        self.assertEqual(normalized["movement_qty"], Decimal("5"))
        self.assertEqual(normalized["movement_direction"], "IN")
        self.assertEqual(normalized["location_group"], "Z")

    def test_normalize_row_defaults_blank_quantities_to_zero(self):
        row = {
            "商品コード": "ABC123",
            "伝票日付": "2026-03-24",
            "入出庫伝票№": "SLIP-003",
            "取引区分略称": "棚卸",
            "ロット№": "LOT-99",
            "ロケーション№": "B-01-01",
            "単位名": "EA",
            "入庫数量": "",
            "出庫数量": "",
            "ﾀｲﾑｽﾀﾝﾌﾟ（時間）": "09:00",
            "ﾀｲﾑｽﾀﾝﾌﾟ（日付）": "2026-03-24",
            "担当者コード": "OP003",
            "クライアントＩＤ": "CLIENT-1",
        }

        normalized = normalize_row(row).data

        self.assertEqual(normalized["qty_in"], Decimal("0"))
        self.assertEqual(normalized["qty_out"], Decimal("0"))
        self.assertEqual(normalized["movement_direction"], "ZERO")


if __name__ == "__main__":
    unittest.main()
