from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class Product:
    product_id: str
    sku: str
    name: str
    item_group: Optional[str] = None
    stock_uom: Optional[str] = None


@dataclass(slots=True)
class WarehouseSite:
    warehouse_id: str
    name: str
    company: Optional[str] = None
    parent_warehouse_id: Optional[str] = None


@dataclass(slots=True)
class StorageLocation:
    location_id: str
    warehouse_id: str
    name: str
    location_type: Optional[str] = None


@dataclass(slots=True)
class SalesOrder:
    order_id: str
    customer_id: Optional[str]
    order_date: datetime
    status: Optional[str] = None
    company: Optional[str] = None
    warehouse_id: Optional[str] = None


@dataclass(slots=True)
class SalesOrderLine:
    line_id: str
    order_id: str
    product_id: str
    quantity: float
    warehouse_id: Optional[str] = None
    requested_delivery_date: Optional[datetime] = None


@dataclass(slots=True)
class InventoryBalance:
    product_id: str
    warehouse_id: str
    quantity_on_hand: float
    reserved_quantity: float = 0.0
    as_of: Optional[datetime] = None


@dataclass(slots=True)
class StockMovement:
    movement_id: str
    product_id: str
    warehouse_id: str
    quantity_delta: float
    movement_type: str
    occurred_at: datetime
    reference_id: Optional[str] = None


@dataclass(slots=True)
class DemandSnapshot:
    warehouse_id: str
    period_start: datetime
    period_end: datetime
    total_order_count: int
    total_units: float
    product_quantities: dict[str, float] = field(default_factory=dict)
