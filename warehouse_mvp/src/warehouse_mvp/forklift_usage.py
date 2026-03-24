from __future__ import annotations

import csv
import math
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


def read_csv_rows(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.strptime(value.strip(), "%Y-%m-%d %H:%M:%S.%f")


def parse_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def parse_bool(value: str | None) -> bool:
    return str(value).strip().lower() == "true"


def enrich_trajectory_rows(rows: list[dict[str, str]], uncertainty_threshold_m: float = 2.5) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []
    prev_by_device: dict[str, dict[str, Any]] = {}

    for row in rows:
        device_id = row.get("device_id", "")
        ts = parse_timestamp(row.get("timestamp"))
        x = parse_float(row.get("x"))
        y = parse_float(row.get("y"))
        z = parse_float(row.get("z"))
        std_x = parse_float(row.get("std_x")) or 0.0
        std_y = parse_float(row.get("std_y")) or 0.0

        uncertainty_2d = math.sqrt(std_x**2 + std_y**2)
        valid_position_flag = uncertainty_2d <= uncertainty_threshold_m
        distance_increment_m = 0.0

        prev = prev_by_device.get(device_id)
        if (
            prev
            and valid_position_flag
            and prev.get("valid_position_flag")
            and x is not None
            and y is not None
            and prev.get("x") is not None
            and prev.get("y") is not None
        ):
            distance_increment_m = math.sqrt((x - prev["x"]) ** 2 + (y - prev["y"]) ** 2)

        enriched_row = {
            **row,
            "timestamp_parsed": ts,
            "x": x,
            "y": y,
            "z": z,
            "std_x": std_x,
            "std_y": std_y,
            "position_uncertainty_2d": uncertainty_2d,
            "valid_position_flag": valid_position_flag,
            "distance_increment_m": distance_increment_m,
        }
        enriched.append(enriched_row)
        prev_by_device[device_id] = enriched_row

    return enriched


def summarize_forklift_usage(
    trajectory_rows: list[dict[str, Any]],
    state_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    state_by_device: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in state_rows:
        state_by_device[row.get("device_id", "")].append(row)

    agg: dict[str, dict[str, Any]] = {}

    for row in trajectory_rows:
        device_id = row.get("device_id", "")
        current = agg.setdefault(
            device_id,
            {
                "device_id": device_id,
                "total_points": 0,
                "valid_points": 0,
                "total_distance_m": 0.0,
                "first_seen_ts": None,
                "last_seen_ts": None,
            },
        )
        current["total_points"] += 1
        if row.get("valid_position_flag"):
            current["valid_points"] += 1
        current["total_distance_m"] += float(row.get("distance_increment_m") or 0.0)

        ts = row.get("timestamp_parsed")
        if ts is not None:
            if current["first_seen_ts"] is None or ts < current["first_seen_ts"]:
                current["first_seen_ts"] = ts
            if current["last_seen_ts"] is None or ts > current["last_seen_ts"]:
                current["last_seen_ts"] = ts

    for device_id, current in agg.items():
        states = state_by_device.get(device_id, [])
        ready_points = 0
        load_detect_count = 0
        driver_detect_count = 0

        for row in states:
            if parse_bool(row.get("ready")):
                ready_points += 1
            if row.get("load_beacon_minor_id"):
                load_detect_count += 1
            if any(row.get(f"driver_beacon_minor_id_{i}") for i in range(1, 6)):
                driver_detect_count += 1

        total_points = current["total_points"] or 1
        current["valid_point_ratio"] = current["valid_points"] / total_points
        current["ready_points"] = ready_points
        current["load_detect_count"] = load_detect_count
        current["driver_detect_count"] = driver_detect_count
        current["first_seen_ts"] = _fmt_ts(current["first_seen_ts"])
        current["last_seen_ts"] = _fmt_ts(current["last_seen_ts"])
        current["total_distance_m"] = round(current["total_distance_m"], 3)

    return sorted(agg.values(), key=lambda row: row["total_distance_m"], reverse=True)


def write_csv(path: str | Path, rows: list[dict[str, Any]]) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        output_path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: "" if v is None else v for k, v in row.items()})


def _fmt_ts(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat(sep=" ")
