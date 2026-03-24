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

## Decisions
- Decision: Use ERPNext as the initial WMS for the project.
- Reason: Start with a single practical system of record now and expand later if needed.
- Alternatives considered: Odoo, OpenBoxes.
- Follow-up needed: define ERPNext-first MVP scope, data model, and simulator boundaries.

## Update Log

### 2026-03-24
- Created process documentation source file.
- Established workflow: maintain documentation here during work, then sync polished updates to Google Docs.
- Recorded ERPNext as the initial WMS choice for the warehouse project.
