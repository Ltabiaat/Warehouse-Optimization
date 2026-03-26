from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(slots=True)
class WarehouseDimensions:
    width_m: float
    length_m: float
    height_m: Optional[float] = None


@dataclass(slots=True)
class Zone:
    zone_id: str
    name: str
    zone_type: str
    capacity_units: Optional[int] = None


@dataclass(slots=True)
class Equipment:
    equipment_id: str
    name: str
    equipment_type: str
    count: int = 1


@dataclass(slots=True)
class WMSConnection:
    provider: str
    connection_type: str
    endpoint: Optional[str] = None


@dataclass(slots=True)
class WarehouseConfiguration:
    warehouse_id: str
    name: str
    dimensions: WarehouseDimensions
    zones: List[Zone] = field(default_factory=list)
    equipment: List[Equipment] = field(default_factory=list)
    wms_connection: Optional[WMSConnection] = None
