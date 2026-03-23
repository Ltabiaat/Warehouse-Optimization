import unittest
from datetime import datetime, timedelta

from warehouse_optimization.telemetry.derived import (
    classify_motion,
    compute_step_distance,
    summarize_motion,
)
from warehouse_optimization.telemetry.models import TelemetryPoint


def point(
    *,
    timestamp: datetime,
    x: float,
    y: float,
    quality_status: str = "good",
    usable_for_route_analysis: bool = True,
) -> TelemetryPoint:
    return TelemetryPoint(
        device_id="gr-fl-v3-0033",
        timestamp=timestamp,
        x=x,
        y=y,
        z=0.0,
        q_x=0.0,
        q_y=0.0,
        q_z=0.0,
        q_w=1.0,
        std_x=0.1,
        std_y=0.1,
        std_z=0.1,
        std_R=0.0,
        std_P=0.0,
        std_Y=0.0,
        uncertainty_2d=0.14,
        quality_status=quality_status,
        usable_for_route_analysis=usable_for_route_analysis,
        source_file="fixture.csv",
        source_row=1,
    )


class TelemetryDerivedTests(unittest.TestCase):
    def test_compute_step_distance(self) -> None:
        a = point(timestamp=datetime(2024, 9, 9, 9, 0, 0), x=0.0, y=0.0)
        b = point(timestamp=datetime(2024, 9, 9, 9, 0, 1), x=3.0, y=4.0)
        self.assertEqual(compute_step_distance(a, b), 5.0)

    def test_classify_motion_detects_stop(self) -> None:
        a = point(timestamp=datetime(2024, 9, 9, 9, 0, 0), x=10.0, y=10.0)
        b = point(timestamp=datetime(2024, 9, 9, 9, 0, 1), x=10.1, y=10.1)
        self.assertEqual(classify_motion(a, b), "stopped")

    def test_classify_motion_detects_moving(self) -> None:
        a = point(timestamp=datetime(2024, 9, 9, 9, 0, 0), x=10.0, y=10.0)
        b = point(timestamp=datetime(2024, 9, 9, 9, 0, 1), x=11.0, y=10.0)
        self.assertEqual(classify_motion(a, b), "moving")

    def test_summarize_motion_counts_moving_and_stopped_segments(self) -> None:
        t0 = datetime(2024, 9, 9, 9, 0, 0)
        rows = [
            point(timestamp=t0, x=0.0, y=0.0),
            point(timestamp=t0 + timedelta(seconds=1), x=0.1, y=0.1),
            point(timestamp=t0 + timedelta(seconds=2), x=1.3, y=0.1),
            point(timestamp=t0 + timedelta(seconds=3), x=2.6, y=0.1),
        ]
        summary = summarize_motion(rows)
        self.assertEqual(summary.total_points, 4)
        self.assertEqual(summary.moving_segments, 2)
        self.assertEqual(summary.stopped_segments, 1)
        self.assertGreater(summary.total_distance_m, 2.0)

    def test_summarize_motion_skips_unusable_points(self) -> None:
        t0 = datetime(2024, 9, 9, 9, 0, 0)
        rows = [
            point(timestamp=t0, x=0.0, y=0.0),
            point(
                timestamp=t0 + timedelta(seconds=1),
                x=5.0,
                y=5.0,
                quality_status="poor",
                usable_for_route_analysis=False,
            ),
            point(timestamp=t0 + timedelta(seconds=2), x=0.2, y=0.1),
        ]
        summary = summarize_motion(rows)
        self.assertEqual(summary.total_points, 3)
        self.assertEqual(summary.usable_points, 2)
        self.assertEqual(summary.moving_segments, 0)
        self.assertEqual(summary.stopped_segments, 1)


if __name__ == "__main__":
    unittest.main()
