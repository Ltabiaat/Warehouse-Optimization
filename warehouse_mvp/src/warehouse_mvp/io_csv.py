from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from .normalizer import normalize_row


def read_raw_rows(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def normalize_rows(rows: Iterable[dict[str, str]]) -> list[dict[str, object]]:
    return [normalize_row(row).data for row in rows]


def write_normalized_rows(path: str | Path, rows: list[dict[str, object]]) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        output_path.write_text("", encoding="utf-8")
        return

    fieldnames = sorted({key for row in rows for key in row.keys()})
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: _stringify(v) for k, v in row.items()})


def _stringify(value: object) -> str:
    if value is None:
        return ""
    return str(value)
