from __future__ import annotations

from pathlib import Path

from warehouse_mvp.forklift_usage import (
    enrich_trajectory_rows,
    read_csv_rows,
    summarize_forklift_usage,
    write_csv,
)

BASE = Path(__file__).resolve().parents[1]
TRAJECTORY = BASE / "data" / "gr-fl-v3-0033.csv"
STATE = BASE / "data" / "gr-fl-v3-0033_STATE.csv"
OUTPUT_ENRICHED = BASE / "output" / "gr-fl-v3-0033_enriched.csv"
OUTPUT_SUMMARY = BASE / "output" / "forklift_usage_summary.csv"


def main() -> None:
    trajectory_rows = read_csv_rows(TRAJECTORY)
    state_rows = read_csv_rows(STATE)
    enriched = enrich_trajectory_rows(trajectory_rows)
    summary = summarize_forklift_usage(enriched, state_rows)
    write_csv(OUTPUT_ENRICHED, enriched)
    write_csv(OUTPUT_SUMMARY, summary)
    print(f"Enriched trajectory written to: {OUTPUT_ENRICHED}")
    print(f"Forklift usage summary written to: {OUTPUT_SUMMARY}")


if __name__ == "__main__":
    main()
