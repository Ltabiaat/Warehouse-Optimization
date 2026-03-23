from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from warehouse_optimization.telemetry.derived import MotionSummary, summarize_motion
from warehouse_optimization.telemetry.models import DeviceStateEvent, TelemetryPoint
from warehouse_optimization.telemetry.parser import parse_state_csv, parse_trajectory_csv


@dataclass(slots=True)
class TelemetryBatch:
    device_id: str
    trajectory_points: list[TelemetryPoint] = field(default_factory=list)
    state_events: list[DeviceStateEvent] = field(default_factory=list)
    quality_counts: dict[str, int] = field(default_factory=dict)
    motion_summary: MotionSummary | None = None


def ingest_device_batch(
    trajectory_path: str | Path,
    state_path: str | Path,
) -> TelemetryBatch:
    trajectory_points = parse_trajectory_csv(trajectory_path)
    state_events = parse_state_csv(state_path)

    if not trajectory_points:
        raise ValueError("No trajectory points were parsed")

    device_id = trajectory_points[0].device_id
    quality_counts = dict(Counter(point.quality_status for point in trajectory_points))
    motion_summary = summarize_motion(trajectory_points)

    return TelemetryBatch(
        device_id=device_id,
        trajectory_points=trajectory_points,
        state_events=state_events,
        quality_counts=quality_counts,
        motion_summary=motion_summary,
    )
