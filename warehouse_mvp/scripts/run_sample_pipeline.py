from __future__ import annotations

import json
from pathlib import Path

from warehouse_mvp.io_csv import normalize_rows, read_raw_rows, write_normalized_rows
from warehouse_mvp.kpi import summarize_kpis

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "sample_warehouse_export.csv"
NORMALIZED = BASE / "output" / "sample_warehouse_normalized.csv"
KPI_JSON = BASE / "output" / "sample_kpi_summary.json"


def main() -> None:
    raw_rows = read_raw_rows(RAW)
    normalized_rows = normalize_rows(raw_rows)
    write_normalized_rows(NORMALIZED, normalized_rows)

    summary = summarize_kpis(normalized_rows)
    KPI_JSON.parent.mkdir(parents=True, exist_ok=True)
    KPI_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Raw rows: {len(raw_rows)}")
    print(f"Normalized rows written to: {NORMALIZED}")
    print(f"KPI summary written to: {KPI_JSON}")


if __name__ == "__main__":
    main()
