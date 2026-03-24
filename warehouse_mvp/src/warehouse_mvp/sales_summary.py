from __future__ import annotations

import csv
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
from typing import Any


def summarize_sales(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], dict[str, Any]] = {}

    for row in rows:
        item_code = row.get("item_code") or ""
        item_name = row.get("item_name") or ""
        key = (item_code, item_name)
        current = grouped.setdefault(
            key,
            {
                "item_code": item_code,
                "item_name": item_name,
                "total_qty_out": Decimal("0"),
                "outbound_event_count": 0,
                "clients_seen": set(),
                "locations_seen": set(),
            },
        )
        qty_out = _to_decimal(row.get("qty_out"))
        current["total_qty_out"] += qty_out
        if qty_out > 0:
            current["outbound_event_count"] += 1
        if row.get("client_id"):
            current["clients_seen"].add(row["client_id"])
        if row.get("location_no"):
            current["locations_seen"].add(row["location_no"])

    results = []
    for current in grouped.values():
        results.append(
            {
                "item_code": current["item_code"],
                "item_name": current["item_name"],
                "total_qty_out": str(current["total_qty_out"]),
                "outbound_event_count": current["outbound_event_count"],
                "distinct_clients": len(current["clients_seen"]),
                "distinct_locations": len(current["locations_seen"]),
            }
        )

    return sorted(results, key=lambda row: Decimal(row["total_qty_out"]), reverse=True)


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
            writer.writerow(row)


def _to_decimal(value: Any) -> Decimal:
    if value is None or value == "":
        return Decimal("0")
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))
