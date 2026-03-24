# Warehouse Layout Configurator Spec

Purpose: define the first Streamlit app for warehouse setup input.

## Goal

Provide a simple user-facing app where a user can:
- specify warehouse layout size
- specify number of forklifts
- mark walls or blocked/unreachable areas
- define named zones such as A, B, C that forklifts may need to reach
- mark forklift start positions
- mark inbound and outbound dock cells

This app is intended to become the first warehouse-configuration input surface before simulation or Gymnasium work.

## MVP features

### 1. Warehouse metadata
- warehouse name
- grid width
- grid height
- forklift count

### 2. Layout grid editor
- render a 2D grid as a cleaner table-style editor
- allow users to set cells directly as blank, blocked (`X`), named zones (`A-F`), forklift starts (`S`), inbound docks (`I`), or outbound docks (`O`)
- blocked cells represent walls, shelving, pillars, restricted zones, or otherwise unreachable areas
- zones represent reachable operating areas forklifts may need to visit

### 3. Exportable configuration
- save the current configuration to JSON
- JSON should include warehouse dimensions, forklift count, blocked cell coordinates, zone cell assignments, start cells, inbound docks, and outbound docks

## Representation model

### Grid-based representation
For MVP, model the warehouse as a simple 2D grid.

### Blocked cells
Blocked cells should represent any area forklifts must not traverse.

### Zones
Zones should represent meaningful destinations or operating areas.

### Start positions
Start positions represent where forklifts may begin an episode or route.

### Dock markers
- inbound docks represent receiving entry/staging points
- outbound docks represent shipping/staging points

## Output format

Suggested JSON structure:

```json
{
  "warehouse_name": "Main Warehouse",
  "width": 12,
  "height": 8,
  "forklift_count": 3,
  "blocked_cells": [{"x": 2, "y": 1}],
  "zone_cells": [{"x": 5, "y": 1, "zone": "A"}],
  "start_cells": [{"x": 0, "y": 0}],
  "inbound_docks": [{"x": 0, "y": 7}],
  "outbound_docks": [{"x": 11, "y": 7}]
}
```

## Future enhancements
- draggable drawing tools instead of single-cell clicks
- named zone editing beyond A-F
- one-way aisles
- equipment-specific start positions
- export directly into simulation environment config
