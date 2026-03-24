from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd
import streamlit as st


@dataclass
class LayoutConfig:
    warehouse_name: str
    width: int
    height: int
    forklift_count: int
    blocked_cells: list[dict[str, int]]
    zone_cells: list[dict[str, int | str]]


OUTPUT_DIR = Path(__file__).resolve().parent / "output"
DEFAULT_CONFIG_PATH = OUTPUT_DIR / "warehouse_layout_config.json"
ZONE_OPTIONS = ["A", "B", "C", "D", "E", "F"]
CELL_OPTIONS = ["", "X", *ZONE_OPTIONS]
ZONE_LABELS = {
    "": "Reachable",
    "X": "Blocked",
    "A": "Zone A",
    "B": "Zone B",
    "C": "Zone C",
    "D": "Zone D",
    "E": "Zone E",
    "F": "Zone F",
}


def main() -> None:
    st.set_page_config(page_title="Warehouse Layout Configurator", layout="wide")
    _inject_styles()
    st.title("Warehouse Layout Configurator")
    st.caption("Set warehouse size, forklift count, blocked areas, and named zones using a cleaner grid editor.")

    _init_state()

    with st.sidebar:
        st.header("Warehouse Settings")
        warehouse_name = st.text_input("Warehouse name", value=st.session_state.warehouse_name)
        width = st.number_input("Grid width", min_value=4, max_value=40, value=st.session_state.width, step=1)
        height = st.number_input("Grid height", min_value=4, max_value=30, value=st.session_state.height, step=1)
        forklift_count = st.number_input("Number of forklifts", min_value=1, max_value=500, value=st.session_state.forklift_count, step=1)

        st.markdown("### Actions")
        apply_size = st.button("Apply grid size", use_container_width=True)
        clear_grid = st.button("Clear all cells", use_container_width=True)
        save_config = st.button("Save configuration", type="primary", use_container_width=True)

        st.markdown("### Cell legend")
        for key in CELL_OPTIONS:
            label = ZONE_LABELS[key]
            display = key or "·"
            st.markdown(f"- **{display}** = {label}")

    if apply_size:
        st.session_state.warehouse_name = warehouse_name
        st.session_state.width = int(width)
        st.session_state.height = int(height)
        st.session_state.forklift_count = int(forklift_count)
        _resize_grid(int(width), int(height))

    st.session_state.warehouse_name = warehouse_name
    st.session_state.forklift_count = int(forklift_count)

    if clear_grid:
        st.session_state.grid_df = _empty_grid_df(st.session_state.height, st.session_state.width)

    left, right = st.columns([2.2, 1])

    with left:
        st.subheader("Layout editor")
        st.write("Edit the grid directly: use `X` for blocked cells and `A-F` for named zones.")
        st.info("Tip: start with a smaller grid, lay out walls/blocked cells first, then assign zones.")

        edited_df = st.data_editor(
            st.session_state.grid_df,
            key="layout_editor",
            use_container_width=True,
            num_rows="fixed",
            hide_index=True,
            column_config={
                col: st.column_config.SelectboxColumn(
                    label=col,
                    options=CELL_OPTIONS,
                    required=False,
                    width="small",
                )
                for col in st.session_state.grid_df.columns
            },
        )
        st.session_state.grid_df = edited_df.fillna("")

    with right:
        st.subheader("Configuration summary")
        config = _build_config()
        blocked_count = len(config.blocked_cells)
        zoned_count = len(config.zone_cells)
        total_cells = config.width * config.height

        c1, c2 = st.columns(2)
        c1.metric("Blocked", blocked_count)
        c2.metric("Zoned", zoned_count)
        st.metric("Reachable", total_cells - blocked_count)
        st.metric("Forklifts", config.forklift_count)

        st.markdown("### Zone counts")
        zone_counts = _zone_counts()
        if zone_counts:
            for zone, count in zone_counts.items():
                st.markdown(f"- **Zone {zone}**: {count} cells")
        else:
            st.caption("No zones assigned yet.")

        with st.expander("Preview JSON", expanded=False):
            st.json(asdict(config))

        st.markdown("### Suggested usage")
        st.markdown("- `X` = walls, racks, pillars, safety zones")
        st.markdown("- `A-F` = operating/destination zones forklifts should be able to reach")

    if save_config:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        DEFAULT_CONFIG_PATH.write_text(json.dumps(asdict(config), indent=2), encoding="utf-8")
        st.success(f"Saved configuration to {DEFAULT_CONFIG_PATH}")


def _init_state() -> None:
    if "warehouse_name" not in st.session_state:
        st.session_state.warehouse_name = "Main Warehouse"
    if "width" not in st.session_state:
        st.session_state.width = 12
    if "height" not in st.session_state:
        st.session_state.height = 8
    if "forklift_count" not in st.session_state:
        st.session_state.forklift_count = 3
    if "grid_df" not in st.session_state:
        st.session_state.grid_df = _empty_grid_df(st.session_state.height, st.session_state.width)


def _empty_grid_df(height: int, width: int) -> pd.DataFrame:
    return pd.DataFrame([["" for _ in range(width)] for _ in range(height)], columns=[str(x) for x in range(width)])


def _resize_grid(width: int, height: int) -> None:
    old_df = st.session_state.grid_df.copy()
    new_df = _empty_grid_df(height, width)
    min_h = min(height, len(old_df.index))
    min_w = min(width, len(old_df.columns))
    for y in range(min_h):
        for x in range(min_w):
            new_df.iat[y, x] = old_df.iat[y, x]
    st.session_state.grid_df = new_df


def _build_config() -> LayoutConfig:
    blocked_cells: list[dict[str, int]] = []
    zone_cells: list[dict[str, int | str]] = []
    df = st.session_state.grid_df.fillna("")

    for y, row in df.iterrows():
        for x_str, value in row.items():
            x = int(x_str)
            value = str(value).strip().upper()
            if value == "X":
                blocked_cells.append({"x": x, "y": int(y)})
            elif value in ZONE_OPTIONS:
                zone_cells.append({"x": x, "y": int(y), "zone": value})

    return LayoutConfig(
        warehouse_name=st.session_state.warehouse_name,
        width=st.session_state.width,
        height=st.session_state.height,
        forklift_count=st.session_state.forklift_count,
        blocked_cells=blocked_cells,
        zone_cells=zone_cells,
    )


def _zone_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    for cell in _build_config().zone_cells:
        zone = str(cell["zone"])
        counts[zone] = counts.get(zone, 0) + 1
    return dict(sorted(counts.items()))


def _inject_styles() -> None:
    st.markdown(
        """
        <style>
        .stDataFrame, .stDataEditor {border-radius: 12px;}
        [data-testid="stMetric"] {
            background: #f8fafc;
            border: 1px solid #e5e7eb;
            padding: 10px;
            border-radius: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
