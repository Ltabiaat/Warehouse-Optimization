"""
Warehouse Layout Editor — visual editor for large-scale warehouse grids.

Run:  streamlit run warehouse_mvp/streamlit_app.py

Features:
  - Import / export layout JSON (including CAD-generated layouts)
  - Click-to-paint on the rendered grid image
  - Rectangle fill for bulk zone / wall placement
  - Custom zone names, undo stack, real-time statistics
  - Door cell type for CAD floorplan doors
  - Grid resize, flood fill, line draw, border walls
  - Navigate-to-region, adjustable zoom, coordinate readout
"""
from __future__ import annotations

import json
from collections import deque
from pathlib import Path
from typing import Any

import numpy as np
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

try:
    from streamlit_image_coordinates import streamlit_image_coordinates

    HAS_CLICK = True
except ImportError:
    HAS_CLICK = False

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
DEFAULT_LAYOUT = OUTPUT_DIR / "case_study_d_layout.json"
SAVE_PATH = OUTPUT_DIR / "warehouse_layout_config.json"

# ---------------------------------------------------------------------------
# Colours
# ---------------------------------------------------------------------------
_SPECIAL_COLORS: dict[str, tuple[int, int, int]] = {
    "":  (245, 245, 245),
    "X": (55,  55,  55),
    "S": (50,  200, 50),
    "I": (100, 180, 255),
    "O": (255, 100, 100),
    "D": (255, 215, 0),
}

_ZONE_PALETTE = [
    (173, 216, 230), (144, 238, 144), (255, 255, 153),
    (255, 178, 102), (204, 153, 255), (255, 153, 204),
    (102, 205, 170), (255, 218, 185), (176, 224, 230),
    (240, 230, 140), (221, 160, 221), (152, 251, 152),
]


def _zone_color(zone: str) -> tuple[int, int, int]:
    idx = sum(ord(c) for c in zone)
    return _ZONE_PALETTE[idx % len(_ZONE_PALETTE)]


def _cell_color(val: str) -> tuple[int, int, int]:
    if val in _SPECIAL_COLORS:
        return _SPECIAL_COLORS[val]
    return _zone_color(val)


# ---------------------------------------------------------------------------
# Grid <-> JSON
# ---------------------------------------------------------------------------

def _grid_from_json(data: dict[str, Any]) -> np.ndarray:
    w, h = int(data["width"]), int(data["height"])
    grid = np.full((h, w), "", dtype=object)
    for c in data.get("blocked_cells", []):
        grid[int(c["y"]), int(c["x"])] = "X"
    for c in data.get("zone_cells", []):
        grid[int(c["y"]), int(c["x"])] = str(c["zone"]).strip().upper()
    for c in data.get("start_cells", []):
        grid[int(c["y"]), int(c["x"])] = "S"
    for c in data.get("inbound_docks", []):
        grid[int(c["y"]), int(c["x"])] = "I"
    for c in data.get("outbound_docks", []):
        grid[int(c["y"]), int(c["x"])] = "O"
    for c in data.get("door_cells", []):
        grid[int(c["y"]), int(c["x"])] = "D"
    return grid


def _grid_to_json(grid: np.ndarray, name: str, forklift_count: int) -> dict[str, Any]:
    h, w = grid.shape
    blocked, zones, starts, inbound, outbound, doors = [], [], [], [], [], []
    for y in range(h):
        for x in range(w):
            v = grid[y, x]
            if v == "X":
                blocked.append({"x": x, "y": y})
            elif v == "S":
                starts.append({"x": x, "y": y})
            elif v == "I":
                inbound.append({"x": x, "y": y})
            elif v == "O":
                outbound.append({"x": x, "y": y})
            elif v == "D":
                doors.append({"x": x, "y": y})
            elif v:
                zones.append({"x": x, "y": y, "zone": v})
    return {
        "warehouse_name": name,
        "width": w,
        "height": h,
        "forklift_count": forklift_count,
        "blocked_cells": blocked,
        "zone_cells": zones,
        "start_cells": starts,
        "inbound_docks": inbound,
        "outbound_docks": outbound,
        "door_cells": doors,
    }


# ---------------------------------------------------------------------------
# Flood fill (BFS, capped at 10,000 cells)
# ---------------------------------------------------------------------------

def _flood_fill(grid: np.ndarray, sx: int, sy: int, fill_val: str) -> int:
    """Fill connected cells of the same type starting at (sx, sy). Returns count filled."""
    h, w = grid.shape
    target = grid[sy, sx]
    if target == fill_val:
        return 0
    visited = set()
    queue = deque([(sx, sy)])
    visited.add((sx, sy))
    count = 0
    cap = 10_000
    while queue and count < cap:
        cx, cy = queue.popleft()
        grid[cy, cx] = fill_val
        count += 1
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited and grid[ny, nx] == target:
                visited.add((nx, ny))
                queue.append((nx, ny))
    return count


# ---------------------------------------------------------------------------
# Bresenham line drawing
# ---------------------------------------------------------------------------

def _bresenham(x0: int, y0: int, x1: int, y1: int) -> list[tuple[int, int]]:
    """Return list of (x, y) cells on the line from (x0,y0) to (x1,y1)."""
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    return points


# ---------------------------------------------------------------------------
# Image rendering
# ---------------------------------------------------------------------------

RULER_PX = 24  # ruler margin in pixels


def _render_grid(grid: np.ndarray, cell_px: int) -> Image.Image:
    h, w = grid.shape
    img_w = w * cell_px + RULER_PX
    img_h = h * cell_px + RULER_PX
    img = Image.new("RGB", (img_w, img_h), (30, 30, 30))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 9)
    except Exception:
        font = ImageFont.load_default()

    # Cells
    for y in range(h):
        for x in range(w):
            color = _cell_color(grid[y, x])
            x0 = RULER_PX + x * cell_px
            y0 = RULER_PX + y * cell_px
            draw.rectangle([x0, y0, x0 + cell_px - 1, y0 + cell_px - 1], fill=color)

    # Rulers every 10 cells
    if cell_px >= 4:
        for x in range(0, w, 10):
            px = RULER_PX + x * cell_px + cell_px // 2
            draw.text((px, 2), str(x), fill=(200, 200, 200), font=font, anchor="mt")
        for y in range(0, h, 10):
            py = RULER_PX + y * cell_px + cell_px // 2
            draw.text((RULER_PX - 3, py), str(y), fill=(200, 200, 200), font=font, anchor="rm")

    return img


def _render_zoomed(
    grid: np.ndarray, cell_px: int, cx: int, cy: int, radius: int
) -> Image.Image:
    """Render a zoomed-in view around (cx, cy) with labels on each cell."""
    h, w = grid.shape
    x1 = max(0, cx - radius)
    y1 = max(0, cy - radius)
    x2 = min(w - 1, cx + radius)
    y2 = min(h - 1, cy + radius)
    rw = x2 - x1 + 1
    rh = y2 - y1 + 1

    margin = 28
    img = Image.new("RGB", (rw * cell_px + margin, rh * cell_px + margin), (30, 30, 30))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", max(8, cell_px // 3))
    except Exception:
        font = ImageFont.load_default()

    for gy in range(y1, y2 + 1):
        for gx in range(x1, x2 + 1):
            color = _cell_color(grid[gy, gx])
            lx = margin + (gx - x1) * cell_px
            ly = margin + (gy - y1) * cell_px
            draw.rectangle([lx, ly, lx + cell_px - 1, ly + cell_px - 1], fill=color)
            draw.rectangle([lx, ly, lx + cell_px - 1, ly + cell_px - 1], outline=(100, 100, 100))

            val = grid[gy, gx]
            if val:
                tc = (255, 255, 255) if val == "X" else (40, 40, 40)
                draw.text(
                    (lx + cell_px // 2, ly + cell_px // 2),
                    val[:3], fill=tc, font=font, anchor="mm",
                )

    # Axis labels
    for gx in range(x1, x2 + 1):
        lx = margin + (gx - x1) * cell_px + cell_px // 2
        draw.text((lx, 4), str(gx), fill=(180, 180, 180), font=font, anchor="mt")
    for gy in range(y1, y2 + 1):
        ly = margin + (gy - y1) * cell_px + cell_px // 2
        draw.text((margin - 4, ly), str(gy), fill=(180, 180, 180), font=font, anchor="rm")

    return img


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------

def _compute_stats(grid: np.ndarray) -> dict[str, Any]:
    flat = grid.flatten()
    total = len(flat)
    walls = int(np.sum(flat == "X"))
    open_floor = int(np.sum(flat == ""))
    starts = int(np.sum(flat == "S"))
    inbound = int(np.sum(flat == "I"))
    outbound = int(np.sum(flat == "O"))
    doors = int(np.sum(flat == "D"))
    zones_dict = dict(sorted(
        {v: int(np.sum(flat == v)) for v in set(flat) if v and v not in ("X", "S", "I", "O", "D")}.items()
    ))
    zone_total = sum(zones_dict.values())
    return {
        "total": total,
        "walls": walls,
        "open_floor": open_floor,
        "starts": starts,
        "inbound_docks": inbound,
        "outbound_docks": outbound,
        "doors": doors,
        "zones": zones_dict,
        "zone_total": zone_total,
    }


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

def _init_state() -> None:
    if "grid" not in st.session_state:
        if DEFAULT_LAYOUT.exists():
            data = json.loads(DEFAULT_LAYOUT.read_text(encoding="utf-8"))
            st.session_state.grid = _grid_from_json(data)
            st.session_state.warehouse_name = data.get("warehouse_name", "Case Study D")
            st.session_state.forklift_count = data.get("forklift_count", 4)
        else:
            st.session_state.grid = np.full((140, 140), "", dtype=object)
            st.session_state.warehouse_name = "Main Warehouse"
            st.session_state.forklift_count = 4
    if "undo_stack" not in st.session_state:
        st.session_state.undo_stack = []
    if "last_click" not in st.session_state:
        st.session_state.last_click = None
    if "zoom_center" not in st.session_state:
        st.session_state.zoom_center = None
    if "line_start" not in st.session_state:
        st.session_state.line_start = None
    if "last_click_info" not in st.session_state:
        st.session_state.last_click_info = None


def _push_undo() -> None:
    st.session_state.undo_stack.append(st.session_state.grid.copy())
    if len(st.session_state.undo_stack) > 30:
        st.session_state.undo_stack.pop(0)


def _pop_undo() -> bool:
    if st.session_state.undo_stack:
        st.session_state.grid = st.session_state.undo_stack.pop()
        return True
    return False


# ---------------------------------------------------------------------------
# Tool value helper
# ---------------------------------------------------------------------------

def _get_tool_value(tool: str, custom_zone: str) -> str:
    m = {
        "Wall (X)": "X", "Eraser (floor)": "", "Start (S)": "S",
        "Inbound dock (I)": "I", "Outbound dock (O)": "O",
        "Door (D)": "D",
        "--- Zone ---": (custom_zone or "A").strip().upper(),
    }
    return m.get(tool, "")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    st.set_page_config(page_title="Warehouse Layout Editor", layout="wide")
    st.markdown(
        """<style>
        [data-testid="stMetric"] {
            background: #f8fafc; border: 1px solid #e5e7eb;
            padding: 8px; border-radius: 10px;
        }
        </style>""",
        unsafe_allow_html=True,
    )
    _init_state()
    grid = st.session_state.grid
    h, w = grid.shape

    # ================================================================
    # Sidebar
    # ================================================================
    with st.sidebar:
        st.header("Warehouse Settings")
        st.session_state.warehouse_name = st.text_input(
            "Warehouse name", value=st.session_state.warehouse_name,
        )
        st.session_state.forklift_count = st.number_input(
            "Forklifts", 1, 500, st.session_state.forklift_count,
        )

        # -- Grid Resize --
        st.divider()
        st.subheader("Grid Resize")
        rc1, rc2 = st.columns(2)
        new_w = rc1.number_input("Width", 10, 500, w, key="resize_w")
        new_h = rc2.number_input("Height", 10, 500, h, key="resize_h")
        st.caption(f"Area: {int(new_w)} x {int(new_h)} = **{int(new_w) * int(new_h):,} m**² (target ~13,000 m²)")
        if st.button("Resize grid", use_container_width=True):
            nw, nh = int(new_w), int(new_h)
            if nw != w or nh != h:
                _push_undo()
                new_grid = np.full((nh, nw), "", dtype=object)
                copy_h = min(h, nh)
                copy_w = min(w, nw)
                new_grid[:copy_h, :copy_w] = grid[:copy_h, :copy_w]
                st.session_state.grid = new_grid
                st.success(f"Resized to {nw} x {nh}")
                st.rerun()

        # -- Import / Export --
        st.divider()
        st.subheader("Import / Export")
        uploaded = st.file_uploader("Import layout JSON", type=["json"])
        if uploaded:
            data = json.loads(uploaded.read())
            _push_undo()
            st.session_state.grid = _grid_from_json(data)
            st.session_state.warehouse_name = data.get("warehouse_name", st.session_state.warehouse_name)
            st.session_state.forklift_count = data.get("forklift_count", st.session_state.forklift_count)
            st.success(f"Imported {data['width']}x{data['height']} layout")
            st.rerun()

        json_files = sorted(OUTPUT_DIR.glob("*.json")) if OUTPUT_DIR.exists() else []
        if json_files:
            sel = st.selectbox("Load from output/", ["(none)"] + [f.name for f in json_files])
            if sel != "(none)" and st.button("Load", use_container_width=True):
                data = json.loads((OUTPUT_DIR / sel).read_text(encoding="utf-8"))
                _push_undo()
                st.session_state.grid = _grid_from_json(data)
                st.session_state.warehouse_name = data.get("warehouse_name", st.session_state.warehouse_name)
                st.session_state.forklift_count = data.get("forklift_count", st.session_state.forklift_count)
                st.rerun()

        if st.button("Save configuration", type="primary", use_container_width=True):
            config = _grid_to_json(grid, st.session_state.warehouse_name, st.session_state.forklift_count)
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            SAVE_PATH.write_text(json.dumps(config, indent=2), encoding="utf-8")
            st.success(f"Saved -> {SAVE_PATH.name}")

        if st.button("Export & Preview in Gym", use_container_width=True):
            config = _grid_to_json(grid, st.session_state.warehouse_name, st.session_state.forklift_count)
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            SAVE_PATH.write_text(json.dumps(config, indent=2), encoding="utf-8")
            st.success(f"Saved -> {SAVE_PATH.name}")
            st.info("The Gymnasium WarehouseNavigationEnv automatically loads configs from this path.")

        # -- Drawing tool --
        st.divider()
        st.subheader("Drawing tool")
        tool = st.selectbox("Active tool", [
            "Wall (X)", "Eraser (floor)", "Start (S)",
            "Inbound dock (I)", "Outbound dock (O)", "Door (D)",
            "--- Zone ---",
        ])
        custom_zone = ""
        if tool == "--- Zone ---":
            custom_zone = st.text_input("Zone name", "A", max_chars=12,
                                        help="Any name: A, QC, STORAGE, RECEIVING...")
        tool_value = _get_tool_value(tool, custom_zone)

        brush_mode = st.radio(
            "Brush mode", ["Radius brush", "Flood fill", "Line draw"],
            horizontal=True, key="brush_mode",
        )
        brush = 0
        if brush_mode == "Radius brush":
            brush = st.slider("Brush radius", 0, 15, 1,
                              help="0 = single cell, 5 = 11x11 area per click")
        elif brush_mode == "Flood fill":
            st.caption("Click a cell to fill all connected cells of the same type.")
        elif brush_mode == "Line draw":
            if st.session_state.line_start is not None:
                lx, ly = st.session_state.line_start
                st.caption(f"Line start set at ({lx}, {ly}). Click to draw line endpoint.")
                if st.button("Cancel line", use_container_width=True):
                    st.session_state.line_start = None
                    st.rerun()
            else:
                st.caption("Click to set line start point.")

        # -- Navigate-to-Region --
        st.divider()
        st.subheader("Navigate to region")
        nc1, nc2 = st.columns(2)
        nav_x = nc1.number_input("Go to X", 0, max(0, w - 1), min(w // 2, w - 1), key="nav_x")
        nav_y = nc2.number_input("Go to Y", 0, max(0, h - 1), min(h // 2, h - 1), key="nav_y")
        if st.button("Jump to position", use_container_width=True):
            st.session_state.zoom_center = (int(nav_x), int(nav_y))
            st.rerun()

        # -- Zoom Controls --
        st.divider()
        st.subheader("Zoom controls")
        zoom_radius = st.slider("Zoom radius", 5, 30, 12, key="zoom_radius")
        zoom_cell_size = st.slider("Zoom cell size (px)", 16, 40, 28, key="zoom_cell_size")

        if st.session_state.zoom_center:
            zx, zy = st.session_state.zoom_center
            step = max(1, zoom_radius)
            zc1, zc2, zc3, zc4 = st.columns(4)
            if zc1.button("< Left", use_container_width=True):
                st.session_state.zoom_center = (max(0, zx - step), zy)
                st.rerun()
            if zc2.button("Right >", use_container_width=True):
                st.session_state.zoom_center = (min(w - 1, zx + step), zy)
                st.rerun()
            if zc3.button("^ Up", use_container_width=True):
                st.session_state.zoom_center = (zx, max(0, zy - step))
                st.rerun()
            if zc4.button("v Down", use_container_width=True):
                st.session_state.zoom_center = (zx, min(h - 1, zy + step))
                st.rerun()

        # -- Undo / Clear --
        st.divider()
        c1, c2 = st.columns(2)
        if c1.button("Undo", use_container_width=True):
            if _pop_undo():
                st.rerun()
            else:
                st.warning("Nothing to undo")
        if c2.button("Clear all", use_container_width=True):
            _push_undo()
            st.session_state.grid[:] = ""
            st.rerun()

        # -- Stats --
        st.divider()
        st.subheader("Statistics")
        stats = _compute_stats(grid)
        st.caption(f"Grid: **{w}** x **{h}** ({stats['total']:,} m²)")
        c1, c2 = st.columns(2)
        c1.metric("Walls", f"{stats['walls']:,}")
        c2.metric("Open floor", f"{stats['open_floor']:,} m²")
        c1, c2 = st.columns(2)
        c1.metric("Starts", stats["starts"])
        c2.metric("Forklifts", st.session_state.forklift_count)
        c1, c2 = st.columns(2)
        c1.metric("Inbound", stats["inbound_docks"])
        c2.metric("Outbound", stats["outbound_docks"])
        c1, c2 = st.columns(2)
        c1.metric("Doors", stats["doors"])

        if stats["zones"]:
            st.markdown("**Zones:**")
            for z, cnt in stats["zones"].items():
                col = _zone_color(z)
                hx = "#{:02x}{:02x}{:02x}".format(*col)
                pct = cnt / stats["total"] * 100 if stats["total"] else 0
                st.markdown(
                    f'<span style="background:{hx};padding:2px 8px;border-radius:4px">'
                    f'{z}</span> **{cnt:,}** m² ({pct:.1f}%)',
                    unsafe_allow_html=True,
                )

        # -- Legend --
        st.divider()
        st.subheader("Legend")
        for label, col in [
            ("Floor", _SPECIAL_COLORS[""]),
            ("Wall", _SPECIAL_COLORS["X"]),
            ("Start", _SPECIAL_COLORS["S"]),
            ("Inbound", _SPECIAL_COLORS["I"]),
            ("Outbound", _SPECIAL_COLORS["O"]),
            ("Door", _SPECIAL_COLORS["D"]),
        ]:
            hx = "#{:02x}{:02x}{:02x}".format(*col)
            st.markdown(
                f'<span style="display:inline-block;width:14px;height:14px;'
                f'background:{hx};border:1px solid #888;border-radius:3px;'
                f'vertical-align:middle;margin-right:6px"></span> {label}',
                unsafe_allow_html=True,
            )

    # ================================================================
    # Main area
    # ================================================================

    # -- Summary bar --
    stats = _compute_stats(grid)
    total = stats["total"]

    def _pct(n: int) -> str:
        return f"{n / total * 100:.1f}%" if total else "0%"

    st.markdown(
        f"**{total:,} m² warehouse** -- "
        f"{_pct(stats['open_floor'])} open floor, "
        f"{_pct(stats['zone_total'])} zones, "
        f"{_pct(stats['walls'])} walls, "
        f"{_pct(stats['doors'])} doors, "
        f"{_pct(stats['starts'] + stats['inbound_docks'] + stats['outbound_docks'])} docks/starts"
    )

    st.title("Warehouse Layout Editor")

    # -- Quick tool select (radio buttons at top) --
    quick_tools = ["Wall (X)", "Eraser (floor)", "Start (S)",
                   "Inbound dock (I)", "Outbound dock (O)", "Door (D)"]
    # Show existing zone names as quick options
    existing_zones_list = sorted(set(
        v for v in grid.flatten() if v and v not in ("X", "S", "I", "O", "D")
    ))
    for z in existing_zones_list[:6]:
        quick_tools.append(f"Zone {z}")

    quick_sel = st.radio("Quick tool select", quick_tools, horizontal=True, key="quick_tool")
    # Apply quick tool selection
    if quick_sel and quick_sel.startswith("Zone "):
        quick_value = quick_sel.replace("Zone ", "")
    else:
        quick_value = {
            "Wall (X)": "X", "Eraser (floor)": "", "Start (S)": "S",
            "Inbound dock (I)": "I", "Outbound dock (O)": "O", "Door (D)": "D",
        }.get(quick_sel, tool_value)
    # The sidebar tool takes precedence unless quick tool was changed
    active_value = quick_value if quick_sel else tool_value

    st.caption(
        f"**{st.session_state.warehouse_name}** | {w}x{h} | 1 cell = 1 m² | "
        f"Tool: **{active_value or 'Floor'}** | Brush: **{brush_mode}**"
        + (f" (r={brush})" if brush_mode == "Radius brush" else "")
    )

    # -- Coordinate readout --
    if st.session_state.last_click_info:
        lci = st.session_state.last_click_info
        st.caption(f"Last click: ({lci['x']}, {lci['y']}) -- Cell type: **{lci['type'] or 'Floor'}**")

    tab_visual, tab_rect, tab_json = st.tabs(["Visual Editor", "Rectangle Tools", "JSON"])

    cell_px = max(4, min(10, min(1200 // w, 800 // h)))

    # -- Tab 1: Visual click-to-paint editor --
    with tab_visual:
        if not HAS_CLICK:
            st.warning(
                "Install `streamlit-image-coordinates` for click-to-paint:\n\n"
                "`pip install streamlit-image-coordinates`"
            )
            st.image(_render_grid(grid, cell_px), caption="Current layout (read-only)")
        else:
            st.markdown(
                "**Click on the grid** to paint with the active tool. "
                "Adjust brush radius in the sidebar for larger strokes."
            )
            img = _render_grid(grid, cell_px)
            coords = streamlit_image_coordinates(img, key="grid_click")

            if coords and coords.get("x") is not None and coords.get("y") is not None:
                px_x = int(coords["x"]) - RULER_PX
                px_y = int(coords["y"]) - RULER_PX
                gx = px_x // cell_px
                gy = px_y // cell_px

                if 0 <= gx < w and 0 <= gy < h:
                    click_key = (gx, gy, active_value, brush, brush_mode)
                    if click_key != st.session_state.last_click:
                        st.session_state.last_click = click_key
                        st.session_state.last_click_info = {
                            "x": gx, "y": gy,
                            "type": grid[gy, gx],
                        }

                        if brush_mode == "Flood fill":
                            _push_undo()
                            filled = _flood_fill(st.session_state.grid, gx, gy, active_value)
                            st.session_state.zoom_center = (gx, gy)
                            st.rerun()

                        elif brush_mode == "Line draw":
                            if st.session_state.line_start is None:
                                st.session_state.line_start = (gx, gy)
                                st.session_state.zoom_center = (gx, gy)
                                st.rerun()
                            else:
                                lx0, ly0 = st.session_state.line_start
                                points = _bresenham(lx0, ly0, gx, gy)
                                _push_undo()
                                for px, py in points:
                                    if 0 <= px < w and 0 <= py < h:
                                        st.session_state.grid[py, px] = active_value
                                st.session_state.line_start = None
                                st.session_state.zoom_center = (gx, gy)
                                st.rerun()

                        else:
                            # Radius brush (default)
                            _push_undo()
                            for dy in range(-brush, brush + 1):
                                for dx in range(-brush, brush + 1):
                                    nx, ny = gx + dx, gy + dy
                                    if 0 <= nx < w and 0 <= ny < h:
                                        st.session_state.grid[ny, nx] = active_value
                            st.session_state.zoom_center = (gx, gy)
                            st.rerun()

            # Zoom inset
            if st.session_state.zoom_center:
                zx, zy = st.session_state.zoom_center
                st.divider()
                st.markdown(f"**Zoom** -- centred on ({zx}, {zy})")
                zoom_cell = st.session_state.get("zoom_cell_size", 28)
                zr = st.session_state.get("zoom_radius", 12)
                zoom_img = _render_zoomed(grid, zoom_cell, zx, zy, zr)
                st.image(zoom_img, use_container_width=False)

    # -- Tab 2: Rectangle fill --
    with tab_rect:
        st.subheader("Rectangle fill")
        st.caption("Fill a rectangular region. Coordinates in meters (cell units).")

        rc1, rc2, rc3, rc4 = st.columns(4)
        rx1 = rc1.number_input("x1", 0, w - 1, 0, key="rx1")
        ry1 = rc2.number_input("y1", 0, h - 1, 0, key="ry1")
        rx2 = rc3.number_input("x2", 0, w - 1, min(20, w - 1), key="rx2")
        ry2 = rc4.number_input("y2", 0, h - 1, min(20, h - 1), key="ry2")

        rect_tools = [
            "Wall (X)", "Eraser (floor)", "Start (S)",
            "Inbound dock (I)", "Outbound dock (O)", "Door (D)",
        ]
        existing_zones = sorted(set(
            v for v in grid.flatten() if v and v not in ("X", "S", "I", "O", "D")
        ))
        rect_tools += [f"Zone: {z}" for z in existing_zones]
        rect_tools.append("Custom zone...")

        rect_tool = st.selectbox("Fill with", rect_tools, key="rect_tool")
        rect_custom = ""
        if rect_tool == "Custom zone...":
            rect_custom = st.text_input("Zone name", "A", key="rz").strip().upper()

        if rect_tool.startswith("Zone: "):
            rect_val = rect_tool.split(": ", 1)[1]
        elif rect_tool == "Custom zone...":
            rect_val = rect_custom or "A"
        else:
            rect_val = {"Wall (X)": "X", "Eraser (floor)": "", "Start (S)": "S",
                        "Inbound dock (I)": "I", "Outbound dock (O)": "O",
                        "Door (D)": "D"}.get(rect_tool, "")

        x1s, x2s = sorted([int(rx1), int(rx2)])
        y1s, y2s = sorted([int(ry1), int(ry2)])
        area = (x2s - x1s + 1) * (y2s - y1s + 1)
        st.caption(f"Area: **{area:,}** cells -> **{rect_val or 'Floor'}**")

        # Preview the region
        preview_img = _render_zoomed(grid, 20, (x1s + x2s) // 2, (y1s + y2s) // 2,
                                     max(x2s - x1s, y2s - y1s) // 2 + 5)
        st.image(preview_img, caption="Region preview", use_container_width=False)

        if st.button("Apply rectangle fill", type="primary", use_container_width=True):
            _push_undo()
            st.session_state.grid[y1s:y2s + 1, x1s:x2s + 1] = rect_val
            st.success(f"Filled ({x1s},{y1s})->({x2s},{y2s}) with {rect_val or 'Floor'}")
            st.rerun()

        # -- Border Walls Quick Action --
        st.divider()
        st.subheader("Quick actions")
        if st.button("Add border walls", use_container_width=True,
                     help="Fill the outermost row/column with walls (X)"):
            _push_undo()
            g = st.session_state.grid
            gh, gw = g.shape
            g[0, :] = "X"
            g[gh - 1, :] = "X"
            g[:, 0] = "X"
            g[:, gw - 1] = "X"
            st.success("Added border walls around the perimeter")
            st.rerun()

        st.divider()
        st.subheader("Cell inspector")
        sc1, sc2 = st.columns(2)
        sx = sc1.number_input("x", 0, w - 1, 0, key="sx")
        sy = sc2.number_input("y", 0, h - 1, 0, key="sy")
        cur = grid[int(sy), int(sx)]
        st.caption(f"Cell ({int(sx)}, {int(sy)}): **{cur or 'Floor'}**")

    # -- Tab 3: JSON --
    with tab_json:
        config = _grid_to_json(grid, st.session_state.warehouse_name, st.session_state.forklift_count)
        st.json(config)
        st.download_button(
            "Download JSON",
            json.dumps(config, indent=2),
            "warehouse_layout_config.json",
            "application/json",
        )


if __name__ == "__main__":
    main()
