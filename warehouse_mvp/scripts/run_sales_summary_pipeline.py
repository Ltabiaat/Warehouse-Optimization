from __future__ import annotations

from pathlib import Path

from warehouse_mvp.io_csv import normalize_rows, read_raw_rows
from warehouse_mvp.sales_summary import summarize_sales, write_csv

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "sample_warehouse_export.csv"
OUTPUT = BASE / "output" / "sales_summary.csv"


def main() -> None:
    raw_rows = read_raw_rows(RAW)
    normalized = normalize_rows(raw_rows)
    sales_summary = summarize_sales(normalized)
    write_csv(OUTPUT, sales_summary)
    print(f"Sales summary written to: {OUTPUT}")


if __name__ == "__main__":
    main()
