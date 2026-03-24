from __future__ import annotations

from collections import Counter, defaultdict
from decimal import Decimal
from typing import Any


def summarize_kpis(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total_rows = len(rows)
    unique_items = len({row.get("item_code") for row in rows if row.get("item_code")})
    unique_locations = len({row.get("location_no") for row in rows if row.get("location_no")})
    unique_operators = len({row.get("operator_code") for row in rows if row.get("operator_code")})
    unique_clients = len({row.get("client_id") for row in rows if row.get("client_id")})

    total_qty_in = sum(_to_decimal(row.get("qty_in")) for row in rows)
    total_qty_out = sum(_to_decimal(row.get("qty_out")) for row in rows)
    net_movement = sum(_to_decimal(row.get("movement_qty")) for row in rows)
    perishable_rows = sum(1 for row in rows if row.get("is_perishable"))

    movement_direction_counts = Counter(row.get("movement_direction") for row in rows)
    transaction_type_counts = Counter(row.get("transaction_type") for row in rows if row.get("transaction_type"))

    by_item = defaultdict(Decimal)
    by_location = defaultdict(Decimal)
    by_operator = defaultdict(int)
    expiry_pressure = []

    for row in rows:
        item_code = row.get("item_code")
        location_no = row.get("location_no")
        operator_code = row.get("operator_code")
        movement_qty = abs(_to_decimal(row.get("movement_qty")))

        if item_code:
            by_item[item_code] += movement_qty
        if location_no:
            by_location[location_no] += movement_qty
        if operator_code:
            by_operator[operator_code] += 1

        if row.get("expiration_date"):
            expiry_pressure.append(
                {
                    "item_code": item_code,
                    "expiration_date": str(row.get("expiration_date")),
                    "movement_direction": row.get("movement_direction"),
                    "location_no": location_no,
                }
            )

    return {
        "total_rows": total_rows,
        "unique_items": unique_items,
        "unique_locations": unique_locations,
        "unique_operators": unique_operators,
        "unique_clients": unique_clients,
        "total_qty_in": str(total_qty_in),
        "total_qty_out": str(total_qty_out),
        "net_movement": str(net_movement),
        "perishable_rows": perishable_rows,
        "movement_direction_counts": dict(movement_direction_counts),
        "transaction_type_counts": dict(transaction_type_counts),
        "top_items_by_movement": _top_n(by_item, 5),
        "top_locations_by_movement": _top_n(by_location, 5),
        "operator_event_counts": _top_n_int(by_operator, 10),
        "expiry_candidates": expiry_pressure[:10],
    }


def _to_decimal(value: Any) -> Decimal:
    if value is None or value == "":
        return Decimal("0")
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def _top_n(counter_like: dict[str, Decimal], n: int) -> list[dict[str, str]]:
    pairs = sorted(counter_like.items(), key=lambda kv: kv[1], reverse=True)[:n]
    return [{"key": key, "value": str(value)} for key, value in pairs]


def _top_n_int(counter_like: dict[str, int], n: int) -> list[dict[str, int]]:
    pairs = sorted(counter_like.items(), key=lambda kv: kv[1], reverse=True)[:n]
    return [{"key": key, "value": value} for key, value in pairs]
