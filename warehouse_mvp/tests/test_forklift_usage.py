import unittest

from warehouse_mvp.forklift_usage import enrich_trajectory_rows, summarize_forklift_usage


class TestForkliftUsage(unittest.TestCase):
    def test_enrich_trajectory_rows_derives_quality_and_distance(self):
        rows = [
            {
                "device_id": "gr-fl-v3-0033",
                "timestamp": "2024-09-09 09:05:58.310000",
                "x": "31.0",
                "y": "45.0",
                "z": "1.8",
                "std_x": "0.1",
                "std_y": "0.2",
            },
            {
                "device_id": "gr-fl-v3-0033",
                "timestamp": "2024-09-09 09:05:59.310000",
                "x": "34.0",
                "y": "49.0",
                "z": "1.8",
                "std_x": "0.1",
                "std_y": "0.2",
            },
        ]
        enriched = enrich_trajectory_rows(rows, uncertainty_threshold_m=2.5)
        self.assertTrue(enriched[0]["valid_position_flag"])
        self.assertEqual(round(enriched[1]["distance_increment_m"], 3), 5.0)

    def test_summarize_forklift_usage_combines_trajectory_and_state(self):
        trajectory_rows = enrich_trajectory_rows(
            [
                {
                    "device_id": "gr-fl-v3-0033",
                    "timestamp": "2024-09-09 09:05:58.310000",
                    "x": "31.0",
                    "y": "45.0",
                    "z": "1.8",
                    "std_x": "0.1",
                    "std_y": "0.2",
                },
                {
                    "device_id": "gr-fl-v3-0033",
                    "timestamp": "2024-09-09 09:05:59.310000",
                    "x": "34.0",
                    "y": "49.0",
                    "z": "1.8",
                    "std_x": "0.1",
                    "std_y": "0.2",
                },
            ]
        )
        state_rows = [
            {
                "device_id": "gr-fl-v3-0033",
                "timestamp": "2024-09-09 09:05:58.310000",
                "ready": "true",
                "load_beacon_minor_id": "1201",
                "driver_beacon_minor_id_1": "501",
            },
            {
                "device_id": "gr-fl-v3-0033",
                "timestamp": "2024-09-09 09:05:59.310000",
                "ready": "true",
                "load_beacon_minor_id": "",
                "driver_beacon_minor_id_1": "501",
            },
        ]
        summary = summarize_forklift_usage(trajectory_rows, state_rows)
        self.assertEqual(len(summary), 1)
        self.assertEqual(summary[0]["device_id"], "gr-fl-v3-0033")
        self.assertEqual(summary[0]["total_points"], 2)
        self.assertEqual(summary[0]["ready_points"], 2)
        self.assertEqual(summary[0]["load_detect_count"], 1)
        self.assertEqual(summary[0]["driver_detect_count"], 2)


if __name__ == "__main__":
    unittest.main()
