"""
DXF -> Warehouse Layout JSON
Case Study D

Parses wall and door layers from a DXF file, rasterises them onto a 1m/cell
grid, clears door openings, then writes a layout JSON.
"""

import json
import math
import sys
from pathlib import Path

import ezdxf

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DXF_PATH = "/Users/lancelot/Desktop/CAD Floorplan Case Study D.dxf"

OUTPUT_PATH = (
    "/Users/lancelot/Desktop/Dev/Guide Robotics/Warehouse-Optimization"
    "/warehouse_mvp/output/case_study_d_layout.json"
)

WALL_LAYERS = {
    r"1_02_\U+305d\U+306e\U+4ed6\U+82af",   # 1_02_その他芯
    r"1_02_\U+9593\U+4ed5\U+5207\U+82af",   # 1_02_間仕切芯
    "2_03_ALC",
    r"2_03-2-\U+ff32\U+ff23\U+ff11",        # 2_03-2-ＲＣ１
}

DOOR_LAYERS = {
    r"2_10-1_\U+5efa\U+5177",               # 2_10-1_建具
    r"2_10_1_\U+5efa\U+51771",              # 2_10_1_建具1
    r"2_10_3_\U+5efa\U+51773",              # 2_10_3_建具3
    r"2_11_\U+5efa\U+5177\U+8a18\U+53f7_SD",  # 2_11_建具記号_SD
}

WALL_HALF_WIDTH = 0.3   # metres either side of wall centre line
DOOR_CLEAR_RADIUS = 2.0  # metres radius around door midpoint to clear


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def segments_from_entity(entity):
    """Return a list of (x0,y0,x1,y1) float tuples for a LINE or LWPOLYLINE."""
    segs = []
    dxftype = entity.dxftype()
    if dxftype == "LINE":
        s = entity.dxf.start
        e = entity.dxf.end
        segs.append((s.x, s.y, e.x, e.y))
    elif dxftype == "LWPOLYLINE":
        pts = list(entity.get_points())   # (x, y, start_width, end_width, bulge)
        coords = [(p[0], p[1]) for p in pts]
        closed = entity.is_closed
        n = len(coords)
        for i in range(n - 1):
            x0, y0 = coords[i]
            x1, y1 = coords[i + 1]
            segs.append((x0, y0, x1, y1))
        if closed and n > 1:
            x0, y0 = coords[-1]
            x1, y1 = coords[0]
            segs.append((x0, y0, x1, y1))
    return segs


def midpoint_of_entity(entity):
    """Return (mx, my) midpoint for a LINE or the centroid of a LWPOLYLINE."""
    dxftype = entity.dxftype()
    if dxftype == "LINE":
        s = entity.dxf.start
        e = entity.dxf.end
        return ((s.x + e.x) / 2.0, (s.y + e.y) / 2.0)
    elif dxftype == "LWPOLYLINE":
        pts = list(entity.get_points())
        if not pts:
            return None
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        return (sum(xs) / len(xs), sum(ys) / len(ys))
    return None


def rasterise_thick_segment(grid, W, H, x0, y0, x1, y1, half_w, origin_x, origin_y):
    """
    Mark all cells within half_w metres of the segment (x0,y0)-(x1,y1) as True.
    Uses a pixel-walking approach: iterate over the bounding box of the
    thickened segment and test distance-to-segment for each candidate cell.
    """
    # Transform to grid coordinates (cell centres at integer+0.5)
    def to_grid(wx, wy):
        return (wx - origin_x, wy - origin_y)

    gx0, gy0 = to_grid(x0, y0)
    gx1, gy1 = to_grid(x1, y1)

    margin = half_w + 0.5   # extra half-cell so thick walls fill properly

    col_min = max(0, int(math.floor(min(gx0, gx1) - margin)))
    col_max = min(W - 1, int(math.ceil(max(gx0, gx1) + margin)))
    row_min = max(0, int(math.floor(min(gy0, gy1) - margin)))
    row_max = min(H - 1, int(math.ceil(max(gy0, gy1) + margin)))

    # Direction vector
    dx = gx1 - gx0
    dy = gy1 - gy0
    seg_len_sq = dx * dx + dy * dy

    for col in range(col_min, col_max + 1):
        cx = col + 0.5   # cell centre in grid coords
        for row in range(row_min, row_max + 1):
            cy = row + 0.5
            # Distance from cell centre to segment
            if seg_len_sq == 0:
                dist = math.sqrt((cx - gx0) ** 2 + (cy - gy0) ** 2)
            else:
                t = ((cx - gx0) * dx + (cy - gy0) * dy) / seg_len_sq
                t = max(0.0, min(1.0, t))
                px = gx0 + t * dx
                py = gy0 + t * dy
                dist = math.sqrt((cx - px) ** 2 + (cy - py) ** 2)
            if dist <= half_w:
                grid[row][col] = True


def clear_door_radius(grid, W, H, mx, my, radius, origin_x, origin_y):
    """Clear (set to False) all cells within radius of door midpoint (mx, my)."""
    gmx = mx - origin_x
    gmy = my - origin_y

    r_ceil = int(math.ceil(radius)) + 1
    col_min = max(0, int(math.floor(gmx - radius)))
    col_max = min(W - 1, int(math.ceil(gmx + radius)))
    row_min = max(0, int(math.floor(gmy - radius)))
    row_max = min(H - 1, int(math.ceil(gmy + radius)))

    for col in range(col_min, col_max + 1):
        cx = col + 0.5
        for row in range(row_min, row_max + 1):
            cy = row + 0.5
            dist = math.sqrt((cx - gmx) ** 2 + (cy - gmy) ** 2)
            if dist <= radius:
                grid[row][col] = False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"Loading DXF: {DXF_PATH}")
    doc = ezdxf.readfile(DXF_PATH)
    msp = doc.modelspace()

    # --- Pass 1: collect wall segments and find bounding box ---------------
    wall_segments = []
    all_xs = []
    all_ys = []

    for entity in msp:
        layer = entity.dxf.layer
        if layer not in WALL_LAYERS:
            continue
        segs = segments_from_entity(entity)
        for seg in segs:
            x0, y0, x1, y1 = seg
            all_xs.extend([x0, x1])
            all_ys.extend([y0, y1])
            wall_segments.append(seg)

    if not wall_segments:
        print("ERROR: No wall entities found — check layer names.")
        sys.exit(1)

    min_x = min(all_xs)
    max_x = max(all_xs)
    min_y = min(all_ys)
    max_y = max(all_ys)

    W = int(math.ceil(max_x - min_x))
    H = int(math.ceil(max_y - min_y))

    print(f"Wall bounding box: X [{min_x:.2f}, {max_x:.2f}]  Y [{min_y:.2f}, {max_y:.2f}]")
    print(f"Grid dimensions:   {W} x {H} cells (1 cell = 1 m²)")
    print(f"Wall segments:     {len(wall_segments)}")

    # --- Build grid (rows = Y, cols = X) ------------------------------------
    # grid[row][col] == True  =>  blocked
    grid = [[False] * W for _ in range(H)]

    for seg in wall_segments:
        x0, y0, x1, y1 = seg
        rasterise_thick_segment(grid, W, H, x0, y0, x1, y1,
                                 WALL_HALF_WIDTH, min_x, min_y)

    blocked_before_doors = sum(grid[r][c] for r in range(H) for c in range(W))
    print(f"Blocked cells (before door clearing): {blocked_before_doors}")

    # --- Pass 2: door entities → clear openings ----------------------------
    door_midpoints = []

    for entity in msp:
        layer = entity.dxf.layer
        if layer not in DOOR_LAYERS:
            continue
        mp = midpoint_of_entity(entity)
        if mp is not None:
            door_midpoints.append(mp)

    print(f"Door entities found: {len(door_midpoints)}")

    for mx, my in door_midpoints:
        clear_door_radius(grid, W, H, mx, my, DOOR_CLEAR_RADIUS, min_x, min_y)

    blocked_after_doors = sum(grid[r][c] for r in range(H) for c in range(W))
    doors_cleared = blocked_before_doors - blocked_after_doors
    open_floor = W * H - blocked_after_doors

    print(f"Blocked cells (after door clearing):  {blocked_after_doors}")
    print(f"Cells cleared by door openings:       {doors_cleared}")
    print(f"Approximate open floor area:          {open_floor} m²")

    # --- Build blocked_cells list ------------------------------------------
    blocked_cells = []
    for row in range(H):
        for col in range(W):
            if grid[row][col]:
                blocked_cells.append({"x": col, "y": row})

    # --- Assemble JSON payload ---------------------------------------------
    layout = {
        "warehouse_name": "Case Study D",
        "width": W,
        "height": H,
        "forklift_count": 4,
        "blocked_cells": blocked_cells,
        "zone_cells": [],
        "start_cells": [{"x": 2, "y": 2}],
        "inbound_docks": [],
        "outbound_docks": [],
    }

    out_path = Path(OUTPUT_PATH)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(layout, f, ensure_ascii=False, indent=2)

    print(f"\nJSON written to: {out_path}")
    print("Done.")


if __name__ == "__main__":
    main()
