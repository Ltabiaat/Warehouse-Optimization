from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time
from decimal import Decimal, InvalidOperation
import hashlib
from typing import Any

from .schema import SOURCE_TO_NORMALIZED


@dataclass(frozen=True)
class NormalizedRow:
    data: dict[str, Any]


def rename_source_fields(row: dict[str, Any]) -> dict[str, Any]:
    renamed: dict[str, Any] = {}
    for key, value in row.items():
        renamed[SOURCE_TO_NORMALIZED.get(key, key)] = value
    return renamed


def _clean(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return value


def _parse_decimal(value: Any) -> Decimal:
    value = _clean(value)
    if value is None:
        return Decimal("0")
    if isinstance(value, Decimal):
        return value
    text = str(value).replace(",", "")
    try:
        return Decimal(text)
    except InvalidOperation as exc:
        raise ValueError(f"Invalid decimal value: {value!r}") from exc


def _parse_date(value: Any) -> date | None:
    value = _clean(value)
    if value is None:
        return None
    text = str(value)
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Unsupported date format: {value!r}")


def _parse_time(value: Any) -> time | None:
    value = _clean(value)
    if value is None:
        return None
    text = str(value)
    for fmt in ("%H:%M:%S", "%H:%M", "%H%M%S", "%H%M"):
        try:
            return datetime.strptime(text, fmt).time()
        except ValueError:
            continue
    raise ValueError(f"Unsupported time format: {value!r}")


def _combine_timestamp(d: date | None, t: time | None) -> datetime | None:
    if d is None:
        return None
    if t is None:
        t = time(0, 0, 0)
    return datetime.combine(d, t)


def build_event_id(normalized: dict[str, Any]) -> str:
    raw = "|".join(
        str(normalized.get(part) or "")
        for part in (
            "inventory_slip_no",
            "item_code",
            "location_no",
            "event_date",
            "event_time",
            "operator_code",
        )
    )
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def normalize_row(row: dict[str, Any]) -> NormalizedRow:
    renamed = rename_source_fields(row)
    cleaned = {key: _clean(value) for key, value in renamed.items()}

    cleaned["qty_in"] = _parse_decimal(cleaned.get("qty_in"))
    cleaned["qty_out"] = _parse_decimal(cleaned.get("qty_out"))

    if "qty_in_each" in cleaned:
        cleaned["qty_in_each"] = _parse_decimal(cleaned.get("qty_in_each"))
    if "qty_out_each" in cleaned:
        cleaned["qty_out_each"] = _parse_decimal(cleaned.get("qty_out_each"))

    cleaned["transaction_date"] = _parse_date(cleaned.get("transaction_date"))
    cleaned["event_date"] = _parse_date(cleaned.get("event_date"))
    cleaned["event_time"] = _parse_time(cleaned.get("event_time"))
    cleaned["receipt_date"] = _parse_date(cleaned.get("receipt_date"))
    cleaned["expiration_date"] = _parse_date(cleaned.get("expiration_date"))

    data_date = _parse_date(cleaned.get("data_timestamp_date"))
    data_time = _parse_time(cleaned.get("data_timestamp_time"))

    cleaned["event_ts"] = _combine_timestamp(cleaned.get("event_date"), cleaned.get("event_time"))
    cleaned["data_ts"] = _combine_timestamp(data_date, data_time)
    cleaned["movement_qty"] = cleaned["qty_in"] - cleaned["qty_out"]
    cleaned["movement_direction"] = (
        "IN" if cleaned["movement_qty"] > 0 else "OUT" if cleaned["movement_qty"] < 0 else "ZERO"
    )
    cleaned["is_perishable"] = cleaned.get("expiration_date") is not None
    cleaned["location_group"] = cleaned.get("floor_code") or _derive_location_group(cleaned.get("location_no"))
    cleaned["event_id"] = build_event_id(cleaned)

    return NormalizedRow(cleaned)


def _derive_location_group(location_no: Any) -> str | None:
    location_no = _clean(location_no)
    if location_no is None:
        return None
    if "-" in location_no:
        return location_no.split("-", 1)[0]
    return str(location_no)[:3] if len(str(location_no)) >= 3 else str(location_no)
