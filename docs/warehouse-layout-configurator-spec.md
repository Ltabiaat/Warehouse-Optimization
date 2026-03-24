# Warehouse Layout Configurator Spec

Purpose: define the first Streamlit app for warehouse setup input.

## Goal

Provide a simple user-facing app where a user can:
- specify warehouse layout size
- specify number of forklifts
- mark walls or blocked/unreachable areas

This app is intended to become the first warehouse-configuration input surface before simulation or Gymnasium work.

## MVP features

### 1. Warehouse metadata
- warehouse name
- grid width
- grid height
- forklift count

### 2. Layout grid editor
- render a 2D grid
- allow users to mark cells as blocked
- blocked cells represent walls, shelving, pillars, restricted zones, or otherwise unreachable areas

### 3. Exportable configuration
- save the current configuration to JSON
- JSON should include warehouse dimensions, forklift count, and blocked cell coordinates

## Representation model

### Grid-based representation
For MVP, model the warehouse as a simple 2D grid.

Pros:
- easy to understand
- easy to edit in Streamlit
- easy to convert into graph nodes later
- enough for first-pass route/path simulation work

### Blocked cells
Blocked cells should represent any area forklifts must not traverse, including:
- walls
- racks/shelves
- safety zones
- structural obstacles
- unreachable/loading-only areas

## Output format

Suggested JSON structure:

```json
{
  "warehouse_name": "Main Warehouse",
  "width": 12,
  "height": 8,
  "forklift_count": 3,
  "blocked_cells": [
    {"x": 2, "y": 1},
    {"x": 2, "y": 2}
  ]
}
```

## Future enhancements
- draggable drawing tools instead of checkboxes
- named zones
- inbound/outbound dock positions
- pick zones
- storage rack templates
- one-way aisles
- forklift start positions
- loading and staging areas
- export directly into simulation environment config
