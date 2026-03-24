from __future__ import annotations

import hashlib
from typing import Any

from .order_task_models import OrderLineTask, TaskSequence


def generate_outbound_tasks(
    rows: list[dict[str, Any]],
    location_to_zone: dict[str, str] | None = None,
    processing_zone_by_item: dict[str, str] | None = None,
    default_dropoff_zone: str | None = None,
) -> list[OrderLineTask]:
    location_to_zone = location_to_zone or {}
    processing_zone_by_item = processing_zone_by_item or {}

    tasks: list[OrderLineTask] = []
    for row in rows:
        qty_out = _to_float(row.get("qty_out"))
        if qty_out <= 0:
            continue

        item_code = str(row.get("item_code") or "")
        item_name = str(row.get("item_name") or "")
        order_ref = str(row.get("inventory_slip_no") or "")
        location_no = str(row.get("location_no") or "") or None
        pickup_zone = location_to_zone.get(location_no or "") or row.get("floor_code") or None
        processing_zone = processing_zone_by_item.get(item_code)
        dropoff_zone = default_dropoff_zone
        priority = _priority_score(row)

        tasks.append(
            OrderLineTask(
                task_id=_task_id(order_ref, item_code, location_no or ""),
                source_type="outbound",
                order_ref=order_ref,
                item_code=item_code,
                item_name=item_name,
                quantity=qty_out,
                pickup_zone=str(pickup_zone) if pickup_zone is not None else None,
                pickup_location=location_no,
                processing_zone=processing_zone,
                dropoff_type="outbound_dock",
                dropoff_zone=dropoff_zone,
                priority=priority,
                client_id=str(row.get("client_id")) if row.get("client_id") else None,
            )
        )

    return sorted(tasks, key=lambda t: (-t.priority, t.order_ref, t.item_code))


def task_to_sequence(task: OrderLineTask) -> TaskSequence:
    steps: list[str] = []
    if task.pickup_zone:
        steps.append(f"pickup:{task.pickup_zone}")
    elif task.pickup_location:
        steps.append(f"pickup_location:{task.pickup_location}")

    if task.processing_zone:
        steps.append(f"process:{task.processing_zone}")

    if task.dropoff_zone:
        steps.append(f"dropoff:{task.dropoff_zone}")
    else:
        steps.append(f"dropoff_type:{task.dropoff_type}")

    return TaskSequence(task_id=task.task_id, steps=tuple(steps))


def _priority_score(row: dict[str, Any]) -> int:
    qty_out = int(_to_float(row.get("qty_out")))
    expiry_bonus = 50 if row.get("expiration_date") else 0
    return qty_out + expiry_bonus


def _to_float(value: Any) -> float:
    if value is None or value == "":
        return 0.0
    return float(value)


def _task_id(order_ref: str, item_code: str, pickup_location: str) -> str:
    raw = f"{order_ref}|{item_code}|{pickup_location}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]
