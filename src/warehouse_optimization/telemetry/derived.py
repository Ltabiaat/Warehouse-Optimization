from __future__ import annotations

from dataclasses import dataclass
from math import hypot

from warehouse_optimization.telemetry.models import TelemetryPoint


@dataclass(slots=True)
class MotionSummary:
    total_points: int
    usable_points: int
    moving_segments: int
    stopped_segments: int
    total_distance_m: float


def compute_step_distance(a: TelemetryPoint, b: TelemetryPoint) -> float:
    return hypot(b.x - a.x, b.y - a.y)


def classify_motion(
    a: TelemetryPoint,
    b: TelemetryPoint,
    stop_distance_threshold_m: float = 0.5,
) -> str:
    distance = compute_step_distance(a, b)
    if distance <= stop_distance_threshold_m:
        return "stopped"
    return "moving"


def summarize_motion(points: list[TelemetryPoint]) -> MotionSummary:
    total_points = len(points)
    usable = [point for point in points if point.usable_for_route_analysis]

    moving_segments = 0
    stopped_segments = 0
    total_distance_m = 0.0

    for current, nxt in zip(usable, usable[1:]):
        distance = compute_step_distance(current, nxt)
        total_distance_m += distance
        motion = classify_motion(current, nxt)
        if motion == "moving":
            moving_segments += 1
        else:
            stopped_segments += 1

    return MotionSummary(
        total_points=total_points,
        usable_points=len(usable),
        moving_segments=moving_segments,
        stopped_segments=stopped_segments,
        total_distance_m=total_distance_m,
    )
