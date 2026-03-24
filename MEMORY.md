# MEMORY.md

## Identity
- Assistant name: Squire
- Nature: AI assistant
- Vibe: practical, warm, focused on helping Lancelot get work done
- Signature emoji: ⚔️

## User
- Preference: for actual product builds, document the process as work progresses so future iterations are easier to understand and improve
- Preference: maintain engineering documentation in workspace files first, then sync polished updates into Google Docs as work progresses
- Preference: Google Docs progress documentation should track implementation progress and function/component operations so generated code is easy to understand later
- Default process documentation sync target: https://docs.google.com/document/d/1fTt_3JAG4_u5jb5yyL3o2rqV4ggKh2Bv497zYz1Qw5A/edit?tab=t.0
- Warehouse project decision: use ERPNext as the initial WMS for this project; broader system additions can come later
- Warehouse architecture direction: treat Streamlit layout input as the warehouse/world definition, operational sales/order/inventory data as task-generation input, and Gymnasium as the execution/simulation layer that runs those generated forklift tasks inside the configured warehouse topology
- Warehouse optimization direction: RL should not only learn routing within a fixed layout; it should also be able to propose layout changes such as moving zones when changing sales patterns justify the operational disruption and expected efficiency gains
- Preference: focus on test-driven development when building products
- Name: Lancelot
- Preferred form of address: Lancelot
- Preference: prioritize the best solution within reasonable constraints, not the first solution that appears
- Preference: when troubleshooting important technical issues, do deeper research before applying fixes

## Legacy OpenClaw import from Linux bot
Imported on 2026-03-19 from `~/Desktop/openclawoldbot` on this Mac, which contained the prior Linux bot state.

Portable facts imported:
- The old bot used Telegram and Discord channels.
- Telegram DMs were configured with pairing.
- There were recurring automation jobs for:
  - weekly security / skill / update healthcheck
  - weekly Tokyo professional events post to Discord
  - weekly Tokyo English-friendly internships sheet update
  - weekly Tokyo student discussion prompt to Discord
  - weekly Tokyo social events post to Discord
- n8n was running in Docker on the old Linux machine and was part of the automation stack.
- The old internship workflow depended on Google Sheets access via `gog`/Google auth.
- A recurring old failure mode was Discord announce delivery failing when channel targets were ambiguous by name rather than stable IDs.
- Another recurring old failure mode was browser-control timeouts affecting the internship sheet update flow.
- Over time, the old environment gained many additional custom skills/CLIs; the more durable ones were Google tooling (`gog`), GitHub CLI guidance, Oracle second-model review, and media/document helper tools.

Do not blindly reuse Linux machine paths, tokens, or host-specific config from that backup on this Mac. Recreate only portable intent and documentation.
