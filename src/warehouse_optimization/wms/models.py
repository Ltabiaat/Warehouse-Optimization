from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class OrderSummary:
    order_id: str
    created_at: datetime
    sku: str
    quantity: int
    source_zone_id: str
    destination_zone_id: str
