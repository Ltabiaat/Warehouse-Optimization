# Process Documentation

This file is the workspace source of truth for process documentation before syncing polished updates to Google Docs.

## Purpose

Track:
- implementation progress
- function/component operations
- architecture and behavior explanations
- decisions and tradeoffs
- open issues and next steps

The goal is to make generated code easy to understand and maintain later.

## Sync Target

- Google Doc: https://docs.google.com/document/d/1fTt_3JAG4_u5jb5yyL3o2rqV4ggKh2Bv497zYz1Qw5A/edit?tab=t.0
- Sync mode: workspace-first, then polished Google Docs updates

## Documentation Rules

- Update this doc as work progresses, not only at the end.
- Prefer concise explanations of why something exists and how it behaves.
- For major changes, document both implementation details and operational impact.
- Keep code-adjacent docs readable by someone seeing the project fresh.

## Standard Sections

### 1. Current Status
- What is in progress
- What is complete
- What is blocked

### 2. Recent Changes
- Date:
- Change:
- Why:
- Impact:

### 3. Functions and Components
For each meaningful function/component/module, document:
- Name:
- Location:
- Responsibility:
- Inputs:
- Outputs:
- Side effects:
- Important edge cases:
- Notes for future changes:

### 4. Decisions
- Decision:
- Reason:
- Alternatives considered:
- Follow-up needed:

### 5. Operational Notes
- How the system behaves at runtime
- External dependencies
- Failure modes
- Monitoring/debugging notes

### 6. Known Issues
- Issue:
- Impact:
- Workaround:
- Planned fix:

### 7. Next Steps
- Immediate next tasks
- Nice-to-have follow-ups

## Current Status
- Project direction is being refined for a warehouse optimization system.
- Initial WMS choice: ERPNext.
- Broader platform additions may come later after the first implementation path is validated.
- A real warehouse movement export has now been translated into an MVP-friendly schema and build plan.

## Decisions
- Decision: Use ERPNext as the initial WMS for the project.
- Reason: Start with a single practical system of record now and expand later if needed.
- Alternatives considered: Odoo, OpenBoxes.
- Follow-up needed: define ERPNext-first MVP scope, data model, and simulator boundaries.
- Decision: Use the provided warehouse export as the first movement-event dataset for proof-of-concept testing.
- Reason: It is enough to test analytics, heuristics, and a lightweight simulation direction without waiting for perfect ERPNext integration.
- Alternatives considered: waiting for a more complete ERP/warehouse dataset first.
- Follow-up needed: build parser/cleaner, normalized fact table, and baseline KPI logic.

## Recent Changes
- Date: 2026-03-24
- Change: Created warehouse event data dictionary, MVP schema, ERPNext mapping notes, and an MVP build plan.
- Why: Needed a concrete way to test the idea using real warehouse columns rather than staying at the architecture-discussion level.
- Impact: The project now has a practical data model and a clear workaround strategy for missing ideal fields.
- Date: 2026-03-24
- Change: Scaffolded the first Python normalization package for the warehouse MVP, including schema mapping, row normalization, and unit tests.
- Why: Needed a concrete ingestion path from raw Japanese warehouse export rows to a normalized event model.
- Impact: The project now has an executable foundation for sample-file ingestion and downstream KPI work.

## Functions and Components
- Name: `warehouse_mvp.schema.SOURCE_TO_NORMALIZED`
- Location: `warehouse_mvp/src/warehouse_mvp/schema.py`
- Responsibility: Maps source Japanese warehouse export headers into normalized English field names.
- Inputs: raw column names from the source export.
- Outputs: normalized field names.
- Side effects: none.
- Important edge cases: unmapped columns currently pass through unchanged.
- Notes for future changes: extend carefully when real source variants appear.

- Name: `warehouse_mvp.normalizer.normalize_row`
- Location: `warehouse_mvp/src/warehouse_mvp/normalizer.py`
- Responsibility: Cleans a raw row, parses dates/times/quantities, derives event fields, and returns a normalized event record.
- Inputs: raw dictionary keyed by source column names.
- Outputs: normalized row with derived fields such as `event_ts`, `movement_qty`, `movement_direction`, and `event_id`.
- Side effects: none.
- Important edge cases: blank numeric fields default to zero; multiple date/time formats are supported; unsupported formats raise explicit errors.
- Notes for future changes: add batch normalization, structured validation errors, and CSV ingestion wrappers.

## Operational Notes
- Current MVP framing is intentionally narrow: movement analytics, baseline heuristics, and lightweight simulation assumptions.
- Missing ideal fields such as full order context, warehouse graph geometry, and exact task durations are not blockers for proof-of-concept testing if handled with explicit approximations.
- The initial code scaffold is dependency-light on purpose so it can run in the current environment without extra package installation.

## Recent Changes
- Date: 2026-03-24
- Change: Added sample CSV ingestion, normalized CSV output generation, and first KPI summary generation.
- Why: Needed an end-to-end proof that the MVP pipeline can turn raw warehouse export rows into analysis-ready outputs.
- Impact: We now have executable sample outputs and a first signal check for dataset usefulness.

## Operational Notes
- Sample pipeline outputs currently live under `warehouse_mvp/output/`.
- Current sample KPI signal is promising enough for MVP continuation: the pipeline can identify top items, top locations, operator event counts, movement direction mix, and expiry-related candidates.
- This is still a proof-of-concept signal, not yet a production warehouse truth model.
- The Google Drive project folder has been mirrored locally into `docs/google-knowledge-base/` so prior Google Docs can be used as repo-accessible project knowledge.

## Recent Changes
- Date: 2026-03-24
- Change: Documented forklift tracker data inputs and scaffolded a forklift usage ingestion/summarization path.
- Why: Dashboard scope was narrowed to top-selling items and most-used forklifts, which requires tracker trajectory/state files in addition to the warehouse movement export.
- Impact: The project now has a clear split between sales reporting inputs and forklift usage reporting inputs.

## Operational Notes
- Sales reporting should continue to use the warehouse movement export.
- Forklift usage reporting should use the tracker master file plus `<device_id>.csv` and `<device_id>_STATE.csv` files.
- The tracker pipeline derives quality-aware distance and simple usage metrics that are suitable for a first Power BI dashboard.

## Recent Changes
- Date: 2026-03-24
- Change: Added Power BI-ready sales summary generation and a dashboard specification for the narrowed MVP.
- Why: The immediate goal is now a practical dashboard for top-selling items and most-used forklifts, not broader optimization logic.
- Impact: The project now has concrete reporting outputs and a dashboard build spec.

## Operational Notes
- `sales_summary.csv` is the current Power BI-ready sales source.
- `forklift_usage_summary.csv` is the current Power BI-ready forklift usage source.
- Current dashboard semantics are intentionally careful: outbound quantity is not revenue, and tracker activity is a usage proxy rather than exact utilization truth.

## Recent Changes
- Date: 2026-03-24
- Change: Added a Streamlit-based warehouse layout configurator scaffold with grid size, forklift count, and blocked-cell editing.
- Why: The project needs a user-facing way to specify warehouse layout and movement constraints before simulation work.
- Impact: There is now an MVP input surface for warehouse dimensions, forklift count, and unreachable areas.

## Functions and Components
- Name: `streamlit_app.py`
- Location: `warehouse_mvp/streamlit_app.py`
- Responsibility: Provides a simple UI for editing warehouse size, forklift count, and blocked cells, then exporting the configuration as JSON.
- Inputs: warehouse name, width, height, forklift count, blocked cell selections.
- Outputs: `output/warehouse_layout_config.json`.
- Side effects: writes layout configuration JSON when saved.
- Important edge cases: very large grids will become cumbersome in checkbox form; resizing trims blocked cells outside the new bounds.
- Notes for future changes: replace checkbox grid with a more ergonomic drawing interaction if the app grows.

## Recent Changes
- Date: 2026-03-24
- Change: Extended the Streamlit layout configurator to support named zones on the grid.
- Why: Users need to mark reachable operational areas such as zone A and zone C, not only blocked cells.
- Impact: The layout config can now represent both movement constraints and destination/operating zones.

## Operational Notes
- The Streamlit app currently uses a simple grid-based model, which is enough for first-pass graph/simulation work.
- Blocked cells represent walls, racks, structural obstacles, and any area forklifts should not traverse.
- Zone cells represent named target/operating areas that forklifts may need to reach.

## Recent Changes
- Date: 2026-03-24
- Change: Reworked the Streamlit layout UI into a cleaner table-style grid editor.
- Why: The earlier button-per-cell interaction was too clumsy and visually noisy.
- Impact: Users can now edit blocked cells and zones more directly in a spreadsheet-like layout.

## Operational Notes
- The current Streamlit layout editor now uses direct cell editing with allowed values: blank, `X`, and `A-F`.
- This is still an MVP, but it should be materially easier to use than the previous button grid.

## Recent Changes
- Date: 2026-03-24
- Change: Defined and scaffolded the conversion path from Streamlit layout JSON into canonical warehouse config, topology, and task objects for future Gymnasium use.
- Why: The layout app is intended to become the front-end input layer for custom environment generation.
- Impact: The project now has a concrete internal pipeline from user-entered warehouse layout data toward environment construction.

## Functions and Components
- Name: `layout_loader.warehouse_config_from_dict`
- Location: `warehouse_mvp/src/warehouse_mvp/layout_loader.py`
- Responsibility: Validates and converts saved Streamlit JSON into a canonical `WarehouseConfig` model.
- Inputs: parsed layout JSON data.
- Outputs: typed warehouse configuration object.
- Side effects: none.
- Important edge cases: rejects out-of-bounds cells and overlapping blocked/zone cells.
- Notes for future changes: extend with forklift start positions, docks, and equipment metadata.

- Name: `topology.build_topology`
- Location: `warehouse_mvp/src/warehouse_mvp/topology.py`
- Responsibility: Converts a warehouse configuration into reachable cells, zone lookup, and adjacency graph.
- Inputs: `WarehouseConfig`.
- Outputs: `WarehouseTopology`.
- Side effects: none.
- Important edge cases: all-blocked layouts will fail later when no reachable start exists.
- Notes for future changes: extend beyond 4-neighbor movement and add traversal costs.

## Operational Notes
- The current Streamlit config is now formally treated as a configuration layer, not as the Gymnasium environment itself.
- The intended path is: Streamlit JSON -> canonical config -> topology -> tasks -> Gymnasium environment.
- MVP environment scope should start with single-forklift, grid-based navigation to named zones.

## Recent Changes
- Date: 2026-03-24
- Change: Added the first custom Gymnasium environment (`WarehouseNavigationEnv`) built on top of the Streamlit layout conversion pipeline.
- Why: Needed a concrete runnable environment that turns saved warehouse layout input into navigation tasks for RL/simulation work.
- Impact: The project now has a working first environment for single-forklift navigation to named zones.

## Functions and Components
- Name: `gym_env.WarehouseNavigationEnv`
- Location: `warehouse_mvp/src/warehouse_mvp/gym_env.py`
- Responsibility: Provides a grid-based Gymnasium environment with blocked-cell handling, zone targets, reward logic, and episode termination.
- Inputs: `WarehouseConfig`, `NavigationTask`, and `max_steps`.
- Outputs: Gymnasium reset/step observations, rewards, done flags, and info.
- Side effects: none.
- Important edge cases: invalid moves stay in place and incur penalties; all target zones reached terminates the episode.
- Notes for future changes: extend to multiple forklifts, richer tasks, and better movement cost modeling.

## Operational Notes
- The first environment is intentionally narrow: single forklift, grid navigation, blocked cells, and named zones.
- This is enough to prove the Streamlit-to-environment path before adding ERPNext demand coupling or multi-agent complexity.
- Gymnasium is now an explicit project dependency inside the local warehouse MVP environment.

## Recent Changes
- Date: 2026-03-24
- Change: Extended the layout schema and Streamlit app to support forklift start positions plus inbound and outbound dock markers.
- Why: Environment generation should be able to use explicit starts and dock semantics instead of relying only on generic reachable cells.
- Impact: The configuration layer now captures more realistic routing anchors for future tasks and scenarios.

## Operational Notes
- The layout grid now supports `S` for start cells, `I` for inbound docks, and `O` for outbound docks.
- Task generation currently prefers the first configured start cell when available.
- Dock markers are stored and validated now, even if the first Gymnasium environment does not yet use them deeply.

## Decisions
- Decision: Use the Streamlit app as the warehouse/world configuration layer, not as the task-definition layer.
- Reason: Warehouse structure and operational work generation are separate concerns and should stay cleanly separated.
- Alternatives considered: encoding tasks directly in layout input.
- Follow-up needed: implement order/inventory-driven task generation.
- Decision: Generate forklift tasks from operational sales/order/inventory context and execute them inside the Gymnasium environment built from the layout config.
- Reason: This reflects real warehouse work more accurately than manually scripted zone sequences.
- Alternatives considered: hand-authored scenario sequences only.
- Follow-up needed: build task dataclasses and an order-to-task generator.

## Operational Notes
- The current intended architecture is now: Streamlit layout -> canonical warehouse config/topology -> order/inventory-driven task generation -> Gymnasium environment execution -> analytics/Power BI reporting.
- Task generation should eventually use what was ordered, where it is located, and how it must be processed.
- The current manual zone-sequence task support remains useful as a simple baseline and testing mechanism.

## Recent Changes
- Date: 2026-03-24
- Change: Added the first order-driven task generation layer for outbound workflows.
- Why: The architecture requires operational demand data to generate forklift work rather than relying only on hand-authored zone sequences.
- Impact: The project now has a concrete bridge from normalized operational rows to forklift task sequences.

## Functions and Components
- Name: `order_task_generator.generate_outbound_tasks`
- Location: `warehouse_mvp/src/warehouse_mvp/order_task_generator.py`
- Responsibility: Converts normalized outbound rows into outbound forklift tasks with pickup, optional processing, and dropoff context.
- Inputs: normalized rows, location-to-zone mapping, processing rules, default dropoff zone.
- Outputs: sorted `OrderLineTask` objects.
- Side effects: none.
- Important edge cases: skips non-outbound rows; falls back to location or floor context when detailed zoning is incomplete.
- Notes for future changes: extend to inbound, transfers, and richer priority logic.

## Operational Notes
- The first task-generation layer is intentionally simple and outbound-focused.
- Current generated sequences are suitable for turning order/work demand into environment-ready route objectives.
- Manual zone-sequence tasks still remain useful for smoke tests and baseline debugging.

## Recent Changes
- Date: 2026-03-24
- Change: Wired generated outbound task sequences into a demo environment runner via a task-sequence adapter.
- Why: Needed to prove the architecture path from operational data to environment execution instead of stopping at task generation.
- Impact: The project now demonstrates operational rows -> generated task -> task sequence -> navigation task -> Gymnasium environment.

## Functions and Components
- Name: `task_sequence_adapter.sequence_to_navigation_task`
- Location: `warehouse_mvp/src/warehouse_mvp/task_sequence_adapter.py`
- Responsibility: Converts generated task sequences into zone-addressable navigation tasks for the current environment.
- Inputs: `WarehouseConfig`, `TaskSequence`.
- Outputs: `NavigationTask`.
- Side effects: none.
- Important edge cases: currently only zone-addressable steps are usable by the environment adapter.
- Notes for future changes: replace this adapter once the environment consumes richer task semantics directly.

## Operational Notes
- The generated-task demo now proves the intended architecture path end to end.
- The current demo uses a generated outbound task and a hard-coded action sequence; because the route is topology-constrained, invalid moves correctly hit blocked areas and incur penalties.
- A path planner or heuristic policy runner would make the generated-task demo complete routes more reliably than a fixed action script.

## Next Steps
- Add a simple planner/heuristic runner so generated tasks can complete automatically in the demo.
- Add inbound putaway and internal transfer task generators.
- Verify the revised Streamlit UX with real usage.
- Sync polished updates back into the Google Doc when useful.

## Update Log

### 2026-03-24
- Created process documentation source file.
- Established workflow: maintain documentation here during work, then sync polished updates to Google Docs.
- Recorded ERPNext as the initial WMS choice for the warehouse project.
- Added a translated warehouse movement data dictionary and MVP event schema.
- Added ERPNext mapping notes and a workaround-oriented MVP build plan for incomplete source data.
