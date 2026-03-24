from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

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
ZONE_COLORS = {
    "A": "#dbeafe",
    "B": "#dcfce7",
    "C": "#fef3c7",
    "D": "#fee2e2",
    "E": "#ede9fe",
    "F": "#fce7f3",
}


def main() -> None:
    st.set_page_config(page_title="Warehouse Layout Configurator", layout="wide")
    st.title("Warehouse Layout Configurator")
    st.caption("Define warehouse size, forklift count, blocked areas, and named zones for layout/simulation work.")

    _init_state()

    with st.sidebar:
        st.header("Warehouse Settings")
        warehouse_name = st.text_input("Warehouse name", value=st.session_state.warehouse_name)
        width = st.number_input("Grid width", min_value=4, max_value=100, value=st.session_state.width, step=1)
        height = st.number_input("Grid height", min_value=4, max_value=100, value=st.session_state.height, step=1)
        forklift_count = st.number_input("Number of forklifts", min_value=1, max_value=500, value=st.session_state.forklift_count, step=1)

        st.header("Editing Mode")
        edit_mode = st.radio(
            "What do you want to place?",
            options=["Blocked cells", "Zones"],
            index=0 if st.session_state.edit_mode == "Blocked cells" else 1,
        )
        selected_zone = st.selectbox("Zone label", options=ZONE_OPTIONS, index=ZONE_OPTIONS.index(st.session_state.selected_zone))

        resize_clicked = st.button("Apply grid size")
        clear_blocked_clicked = st.button("Clear blocked cells")
        clear_zones_clicked = st.button("Clear zones")
        save_clicked = st.button("Save configuration")

    st.session_state.edit_mode = edit_mode
    st.session_state.selected_zone = selected_zone

    if resize_clicked:
        st.session_state.width = int(width)
        st.session_state.height = int(height)
        st.session_state.warehouse_name = warehouse_name
        st.session_state.forklift_count = int(forklift_count)
        _trim_grid_state()

    st.session_state.warehouse_name = warehouse_name
    st.session_state.forklift_count = int(forklift_count)

    if clear_blocked_clicked:
        st.session_state.blocked_cells = set()

    if clear_zones_clicked:
        st.session_state.zone_cells = {}

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Layout grid")
        st.write("Click cells to mark blocked areas or assign them to a named zone.")
        _render_grid()

    with col2:
        st.subheader("Current configuration")
        config = LayoutConfig(
            warehouse_name=st.session_state.warehouse_name,
            width=st.session_state.width,
            height=st.session_state.height,
            forklift_count=st.session_state.forklift_count,
            blocked_cells=_serialize_blocked_cells(),
            zone_cells=_serialize_zone_cells(),
        )
        st.json(asdict(config))
        st.metric("Blocked cells", len(st.session_state.blocked_cells))
        st.metric("Zoned cells", len(st.session_state.zone_cells))
        st.metric("Reachable cells", (st.session_state.width * st.session_state.height) - len(st.session_state.blocked_cells))

        st.markdown("### Zone legend")
        for zone in ZONE_OPTIONS:
            color = ZONE_COLORS[zone]
            st.markdown(
                f"<div style='padding:4px 8px; border-radius:6px; background:{color}; margin-bottom:4px;'>Zone {zone}</div>",
                unsafe_allow_html=True,
            )

        st.markdown("### Suggested use")
        st.markdown("- blocked cells = walls, racks, pillars, safety zones")
        st.markdown("- zones = areas forklifts may need to reach, such as A/B/C picking or storage zones")

    if save_clicked:
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
    if "blocked_cells" not in st.session_state:
        st.session_state.blocked_cells = set()
    if "zone_cells" not in st.session_state:
        st.session_state.zone_cells = {}
    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = "Blocked cells"
    if "selected_zone" not in st.session_state:
        st.session_state.selected_zone = "A"


def _render_grid() -> None:
    width = st.session_state.width
    height = st.session_state.height

    for y in range(height):
        cols = st.columns(width)
        for x, col in enumerate(cols):
            zone = st.session_state.zone_cells.get((x, y))
            blocked = (x, y) in st.session_state.blocked_cells
            label = "X" if blocked else zone or "·"
            bg = "#111827" if blocked else ZONE_COLORS.get(zone, "#f8fafc")
            fg = "white" if blocked else "#111827"
            button_key = f"cellbtn_{x}_{y}"
            col.markdown(
                f"<div style='text-align:center; font-size:12px; color:#6b7280;'>{x},{y}</div>",
                unsafe_allow_html=True,
            )
            if col.button(label, key=button_key, use_container_width=True):
                _toggle_cell(x, y)
            col.markdown(
                f"<div style='height:6px; background:{bg}; border-radius:4px; margin-top:-4px; margin-bottom:8px;'></div>",
                unsafe_allow_html=True,
            )


def _toggle_cell(x: int, y: int) -> None:
    cell = (x, y)
    if st.session_state.edit_mode == "Blocked cells":
        if cell in st.session_state.blocked_cells:
            st.session_state.blocked_cells.discard(cell)
        else:
            st.session_state.blocked_cells.add(cell)
            st.session_state.zone_cells.pop(cell, None)
    else:
        if cell in st.session_state.blocked_cells:
            return
        current = st.session_state.zone_cells.get(cell)
        if current == st.session_state.selected_zone:
            st.session_state.zone_cells.pop(cell, None)
        else:
            st.session_state.zone_cells[cell] = st.session_state.selected_zone


def _trim_grid_state() -> None:
    width = st.session_state.width
    height = st.session_state.height
    st.session_state.blocked_cells = {
        (x, y)
        for (x, y) in st.session_state.blocked_cells
        if x < width and y < height
    }
    st.session_state.zone_cells = {
        (x, y): zone
        for (x, y), zone in st.session_state.zone_cells.items()
        if x < width and y < height
    }


def _serialize_blocked_cells() -> list[dict[str, int]]:
    return [
        {"x": x, "y": y}
        for x, y in sorted(st.session_state.blocked_cells, key=lambda cell: (cell[1], cell[0]))
    ]


def _serialize_zone_cells() -> list[dict[str, int | str]]:
    return [
        {"x": x, "y": y, "zone": zone}
        for (x, y), zone in sorted(st.session_state.zone_cells.items(), key=lambda item: (item[0][1], item[0][0]))
    ]


if __name__ == "__main__":
    main()
