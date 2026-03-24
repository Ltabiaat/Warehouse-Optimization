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


OUTPUT_DIR = Path(__file__).resolve().parent / "output"
DEFAULT_CONFIG_PATH = OUTPUT_DIR / "warehouse_layout_config.json"


def main() -> None:
    st.set_page_config(page_title="Warehouse Layout Configurator", layout="wide")
    st.title("Warehouse Layout Configurator")
    st.caption("Define warehouse size, forklift count, and blocked areas for simulation/configuration work.")

    _init_state()

    with st.sidebar:
        st.header("Warehouse Settings")
        warehouse_name = st.text_input("Warehouse name", value=st.session_state.warehouse_name)
        width = st.number_input("Grid width", min_value=4, max_value=100, value=st.session_state.width, step=1)
        height = st.number_input("Grid height", min_value=4, max_value=100, value=st.session_state.height, step=1)
        forklift_count = st.number_input("Number of forklifts", min_value=1, max_value=500, value=st.session_state.forklift_count, step=1)

        resize_clicked = st.button("Apply grid size")
        clear_clicked = st.button("Clear blocked cells")
        save_clicked = st.button("Save configuration")

    if resize_clicked:
        st.session_state.width = int(width)
        st.session_state.height = int(height)
        st.session_state.warehouse_name = warehouse_name
        st.session_state.forklift_count = int(forklift_count)
        _trim_blocked_cells()

    st.session_state.warehouse_name = warehouse_name
    st.session_state.forklift_count = int(forklift_count)

    if clear_clicked:
        st.session_state.blocked_cells = set()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Layout grid")
        st.write("Click checkboxes to mark blocked cells (walls, racks, restricted zones, or unreachable areas).")
        _render_grid()

    with col2:
        st.subheader("Current configuration")
        config = LayoutConfig(
            warehouse_name=st.session_state.warehouse_name,
            width=st.session_state.width,
            height=st.session_state.height,
            forklift_count=st.session_state.forklift_count,
            blocked_cells=_serialize_blocked_cells(),
        )
        st.json(asdict(config))
        st.metric("Blocked cells", len(st.session_state.blocked_cells))
        st.metric("Reachable cells", (st.session_state.width * st.session_state.height) - len(st.session_state.blocked_cells))

        st.markdown("### Cell legend")
        st.markdown("- unchecked = reachable")
        st.markdown("- checked = blocked")

        st.markdown("### Suggested use")
        st.markdown("- walls")
        st.markdown("- pillars")
        st.markdown("- shelves/racking")
        st.markdown("- loading zones forklifts should not drive through")
        st.markdown("- safety-restricted areas")

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


def _render_grid() -> None:
    width = st.session_state.width
    height = st.session_state.height

    for y in range(height):
        cols = st.columns(width)
        for x, col in enumerate(cols):
            key = f"cell_{x}_{y}"
            checked = (x, y) in st.session_state.blocked_cells
            value = col.checkbox(f"{x},{y}", value=checked, key=key, label_visibility="collapsed")
            if value:
                st.session_state.blocked_cells.add((x, y))
            else:
                st.session_state.blocked_cells.discard((x, y))


def _trim_blocked_cells() -> None:
    width = st.session_state.width
    height = st.session_state.height
    st.session_state.blocked_cells = {
        (x, y)
        for (x, y) in st.session_state.blocked_cells
        if x < width and y < height
    }


def _serialize_blocked_cells() -> list[dict[str, int]]:
    return [
        {"x": x, "y": y}
        for x, y in sorted(st.session_state.blocked_cells, key=lambda cell: (cell[1], cell[0]))
    ]


if __name__ == "__main__":
    main()
