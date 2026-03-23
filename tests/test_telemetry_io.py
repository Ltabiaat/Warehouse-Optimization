import unittest
from pathlib import Path

from warehouse_optimization.telemetry.io import ingest_device_batch


class TelemetryIOTests(unittest.TestCase):
    def test_ingest_device_batch_returns_parsed_data_and_summary(self) -> None:
        base = Path("examples/sample_data")
        batch = ingest_device_batch(
            trajectory_path=base / "gr-fl-v3-0033.csv",
            state_path=base / "gr-fl-v3-0033_STATE.csv",
        )

        self.assertEqual(batch.device_id, "gr-fl-v3-0033")
        self.assertEqual(len(batch.trajectory_points), 15)
        self.assertEqual(len(batch.state_events), 15)
        self.assertEqual(batch.motion_summary.total_points, 15)
        self.assertEqual(batch.quality_counts["good"], 13)
        self.assertEqual(batch.quality_counts["poor"], 2)

    def test_ingest_device_batch_uses_only_trajectory_points_for_quality_counts(self) -> None:
        base = Path("examples/sample_data")
        batch = ingest_device_batch(
            trajectory_path=base / "gr-fl-v3-0033.csv",
            state_path=base / "gr-fl-v3-0033_STATE.csv",
        )

        total_classified = sum(batch.quality_counts.values())
        self.assertEqual(total_classified, len(batch.trajectory_points))


if __name__ == "__main__":
    unittest.main()
