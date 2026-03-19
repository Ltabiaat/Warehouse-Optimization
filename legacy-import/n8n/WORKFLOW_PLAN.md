# n8n Migration Plan: Internship + Lead Pipelines (Low-Token Mode)

## Objective
Move recurring data workflows from LLM-driven turns to deterministic automations in n8n.
Use AI only for exception handling and final summaries.

## Workflow A — Internship Collector (Weekly)
Trigger: Every Monday 10:00 UTC

### Node flow
1. Schedule Trigger
2. Source list (Set node with approved sources)
3. Loop sources (Split In Batches)
4. HTTP Request (fetch listing pages / APIs)
5. HTML Extract / RSS / JSON parse
6. Code node: normalize rows
7. Code node: hard reject policy
   - reject paid placement programs
   - reject non-direct postings
   - reject closed/stale/unverified links
   - enforce Tokyo + English-friendly
8. Code node: dedupe by Apply Link + title/company hash
9. IF node: keep 3–10 best diversified rows
10. Google Sheets: read existing rows
11. Code node: remove violating prior rows + compute inserts
12. Google Sheets: append rows
13. Discord/Telegram summary message

## Workflow B — Compliant Lead Pipeline (Daily)
Trigger: Daily at chosen time

### Node flow
1. Schedule Trigger
2. Input source nodes (manual CSV/Sheet import, approved APIs, public pages)
3. Normalize lead objects
4. Compliance gate
   - no anti-bot bypass
   - no disallowed scraping
   - require source + legit basis
5. Scoring node (ICP fit + pain signal + role relevance)
6. Google Sheets upsert (lead tracker)
7. Optional CRM sync (only if compliance check passed)
8. Weekly KPI rollup node

## Hard Rules
- No anti-bot bypass/evasion logic.
- No paid placement internship sources.
- Maintain source URL + verification timestamp.
- Human approval required for outreach sends (optional gate).

## Token Efficiency Strategy
- n8n handles collection/filtering/dedupe/storage.
- LLM invoked only for:
  - ambiguous relevance cases
  - writing concise summaries
  - generating outreach drafts (optional)

## Next step to activate
1. Import the workflow JSON templates from `services/n8n/workflows/`.
2. Configure credentials:
   - Google Sheets OAuth
   - Discord (optional)
3. Fill allowed source lists.
4. Run test execution manually.
5. Enable schedules.
