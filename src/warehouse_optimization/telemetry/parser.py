from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Optional

from warehouse_optimization.telemetry.models import (
    BeaconObservation,
    DeviceStateEvent,
    TelemetryPoint,
)
from warehouse_optimization.telemetry.quality import (
    classify_uncertainty,
    compute_uncertainty_2d,
    usable_for_route_analysis,
)


def _parse_datetime(value: str) -> Optional[datetime]:
    value = value.strip()
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")


def _parse_float(value: str) -> Optional[float]:
    value = value.strip()
    if not value:
        return None
    return float(value)


def _parse_int(value: str) -> Optional[int]:
    value = value.strip()
    if not value:
        return None
    return int(value)


def _parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise ValueError(f"Unsupported boolean value: {value}")


def parse_trajectory_csv(path: str | Path) -> list[TelemetryPoint]:
    path = Path(path)
    rows: list[TelemetryPoint] = []
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        for index, row in enumerate(reader, start=2):
            std_x = float(row["std_x"])
            std_y = float(row["std_y"])
            uncertainty_2d = compute_uncertainty_2d(std_x, std_y)
            quality_status = classify_uncertainty(uncertainty_2d)
            rows.append(
                TelemetryPoint(
                    device_id=row["device_id"],
                    timestamp=_parse_datetime(row["timestamp"]),
                    x=float(row["x"]),
                    y=float(row["y"]),
                    z=float(row["z"]),
                    q_x=float(row["q_x"]),
                    q_y=float(row["q_y"]),
                    q_z=float(row["q_z"]),
                    q_w=float(row["q_w"]),
                    std_x=std_x,
                    std_y=std_y,
                    std_z=float(row["std_z"]),
                    std_R=float(row["std_R"]),
                    std_P=float(row["std_P"]),
                    std_Y=float(row["std_Y"]),
                    uncertainty_2d=uncertainty_2d,
                    quality_status=quality_status,
                    usable_for_route_analysis=usable_for_route_analysis(quality_status),
                    source_file=path.name,
                    source_row=index,
                )
            )
    return rows


def parse_state_csv(path: str | Path) -> list[DeviceStateEvent]:
    path = Path(path)
    rows: list[DeviceStateEvent] = []
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        for index, row in enumerate(reader, start=2):
            driver_beacons: list[BeaconObservation] = []
            for beacon_index in range(1, 6):
                minor_id = _parse_int(row[f"driver_beacon_minor_id_{beacon_index}"])
                rssi = _parse_int(row[f"driver_beacon_rssi_{beacon_index}"])
                timestamp = _parse_datetime(row[f"driver_beacon_timestamp_{beacon_index}"])
                if minor_id is not None and rssi is not None:
                    driver_beacons.append(
                        BeaconObservation(
                            timestamp=timestamp,
                            minor_id=minor_id,
                            rssi=rssi,
                        )
                    )

            rows.append(
                DeviceStateEvent(
                    device_id=row["device_id"],
                    timestamp=_parse_datetime(row["timestamp"]),
                    ready=_parse_bool(row["ready"]),
                    load_beacon_timestamp=_parse_datetime(row["load_beacon_timestamp"]),
                    load_beacon_minor_id=_parse_int(row["load_beacon_minor_id"]),
                    load_beacon_tx_power=_parse_int(row["load_beacon_tx_power"]),
                    driver_beacons=driver_beacons,
                    source_file=path.name,
                    source_row=index,
                )
            )
    return rows
