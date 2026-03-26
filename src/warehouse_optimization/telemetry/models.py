from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class BeaconObservation:
    timestamp: Optional[datetime]
    minor_id: int
    rssi: int


@dataclass(slots=True)
class TelemetryPoint:
    device_id: str
    timestamp: datetime
    x: float
    y: float
    z: float
    q_x: float
    q_y: float
    q_z: float
    q_w: float
    std_x: float
    std_y: float
    std_z: float
    std_R: float
    std_P: float
    std_Y: float
    uncertainty_2d: float
    quality_status: str
    usable_for_route_analysis: bool
    source_file: str
    source_row: int


@dataclass(slots=True)
class DeviceStateEvent:
    device_id: str
    timestamp: datetime
    ready: bool
    load_beacon_timestamp: Optional[datetime] = None
    load_beacon_minor_id: Optional[int] = None
    load_beacon_tx_power: Optional[int] = None
    driver_beacons: list[BeaconObservation] = field(default_factory=list)
    source_file: str = ""
    source_row: int = 0
