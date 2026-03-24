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

## Operational Notes
- Current MVP framing is intentionally narrow: movement analytics, baseline heuristics, and lightweight simulation assumptions.
- Missing ideal fields such as full order context, warehouse graph geometry, and exact task durations are not blockers for proof-of-concept testing if handled with explicit approximations.

## Next Steps
- Build raw-to-normalized mapping logic for the warehouse export.
- Create a sample ingestion/cleaning pipeline.
- Define first KPI set and baseline prioritization heuristic.
- Sync a polished summary of this work into the Google Doc.

## Update Log

### 2026-03-24
- Created process documentation source file.
- Established workflow: maintain documentation here during work, then sync polished updates to Google Docs.
- Recorded ERPNext as the initial WMS choice for the warehouse project.
- Added a translated warehouse movement data dictionary and MVP event schema.
- Added ERPNext mapping notes and a workaround-oriented MVP build plan for incomplete source data.
