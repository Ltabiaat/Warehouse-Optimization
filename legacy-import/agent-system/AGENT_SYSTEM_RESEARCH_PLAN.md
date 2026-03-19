# Agent System Research + Implementation Plan (v1)

Date: 2026-02-18 (UTC)
Owner: Squire

## Goal
Design a high-quality multi-agent system for your OpenClaw setup that is:
- reliable in daily use
- safe by default
- easy to maintain
- measurable (quality is tracked, not guessed)

This plan assumes:
- one shared Google identity/OAuth application across agents
- OpenClaw as the runtime/orchestrator
- Telegram already active, Google channel/services being added

---

## Executive Summary

Use a **hub-and-spoke architecture**:
- a **Coordinator agent** (main interface) handles routing, memory policy, and user-facing responses
- specialized worker agents handle bounded domains (ops, research, messaging, writing, etc.)
- workers run in tighter tool/sandbox constraints than coordinator

Key quality strategy:
1. Start with a simple architecture (avoid premature complexity)
2. Add explicit guardrails and tool allow/deny by agent
3. Add evals + runbooks before scaling number of agents
4. Ship in phases with measurable acceptance criteria

---

## Proposed Target Architecture

### A. Core agent roles (initial)
1. **Coordinator (main)**
2. **Research worker**
3. **Ops worker**
4. **Comms worker (optional phase 2)**

### B. Orchestration policy
- Default: coordinator calls workers as sub-tasks and verifies outputs.
- Require coordinator quality gate before final answers.

### C. Memory strategy
- Daily operational notes in `memory/YYYY-MM-DD.md`
- Durable preferences/decisions in `MEMORY.md`

---

## Risks & Mitigations
- too many agents too early -> add only with evidence/metrics
- over-permissioned tools -> least privilege
- OAuth sprawl -> one project/shared app + scope register
- hidden regressions -> regression evals

---

## Notes
Imported from legacy bot as design reference only. Not active config.
