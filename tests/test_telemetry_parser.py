import unittest
from datetime import datetime
from pathlib import Path

from warehouse_optimization.telemetry.parser import parse_state_csv, parse_trajectory_csv


class TelemetryParserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base = Path("examples/sample_data")

    def test_parse_trajectory_csv_parses_typed_rows(self) -> None:
        rows = parse_trajectory_csv(self.base / "gr-fl-v3-0033.csv")

        self.assertEqual(len(rows), 15)
        first = rows[0]
        self.assertEqual(first.device_id, "gr-fl-v3-0033")
        self.assertEqual(first.timestamp, datetime(2024, 9, 9, 9, 5, 58, 310000))
        self.assertAlmostEqual(first.x, 31.978)
        self.assertAlmostEqual(first.uncertainty_2d, (0.014**2 + 0.019**2) ** 0.5)
        self.assertEqual(first.quality_status, "good")

    def test_parse_trajectory_csv_flags_high_uncertainty_rows(self) -> None:
        rows = parse_trajectory_csv(self.base / "gr-fl-v3-0033.csv")

        self.assertEqual(rows[-1].quality_status, "poor")
        self.assertGreater(rows[-1].uncertainty_2d, 2.5)
        self.assertFalse(rows[-1].usable_for_route_analysis)

    def test_parse_state_csv_handles_missing_optional_beacon_fields(self) -> None:
        rows = parse_state_csv(self.base / "gr-fl-v3-0033_STATE.csv")

        self.assertEqual(len(rows), 15)
        first = rows[0]
        self.assertFalse(first.ready)
        self.assertIsNone(first.load_beacon_minor_id)
        self.assertEqual(first.driver_beacons, [])

    def test_parse_state_csv_collects_driver_beacons(self) -> None:
        rows = parse_state_csv(self.base / "gr-fl-v3-0033_STATE.csv")

        row = rows[8]
        self.assertTrue(row.ready)
        self.assertEqual(row.load_beacon_minor_id, 1203)
        self.assertEqual(len(row.driver_beacons), 5)
        self.assertEqual(row.driver_beacons[0].minor_id, 301)
        self.assertEqual(row.driver_beacons[0].rssi, -63)


if __name__ == "__main__":
    unittest.main()
