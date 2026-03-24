from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OrderLineTask:
    task_id: str
    source_type: str
    order_ref: str
    item_code: str
    item_name: str
    quantity: float
    pickup_zone: str | None
    pickup_location: str | None
    processing_zone: str | None
    dropoff_type: str
    dropoff_zone: str | None
    priority: int
    client_id: str | None


@dataclass(frozen=True)
class TaskSequence:
    task_id: str
    steps: tuple[str, ...]
