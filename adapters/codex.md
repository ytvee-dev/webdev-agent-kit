---
id: 'agents.adapters.codex'
title: 'Codex Client Adapter'
doc_type: 'client-adapter'
layer: 'adapter'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/adapter'
    - 'client/codex'
parent:
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
related:
    - '[[templates/root-pointers/AGENTS.codex|Codex AGENTS Pointer Template]]'
depends_on:
    - '[[common/core/runtime-core-policy|Portable Runtime Core Policy]]'
---

# Codex Client Adapter

Purpose: map portable behavior to Codex instruction, skill, tool, and sandbox conventions without redefining workflow policy.

## Discovery

- Project policy entrypoint after extraction: `.agents/AGENTS.md` through the approved root `AGENTS.md` pointer.
- Project skill root: `.agents/skills`.
- Native skill UI metadata: `skills/*/agents/openai.yaml` when present in the Codex target.
- Capability declarations: `tool-capabilities-manifest.json`; `agents/openai.yaml` is not capability-availability evidence.

## Project Instructions

Root `AGENTS.md` stays a minimal pointer to `.agents/AGENTS.md`. Create or merge it only after explicit user approval; never replace existing project instructions during ordinary bundle work.

## Tool And Sandbox Boundary

Use the active Codex tool registry or validated project profile as capability evidence. A native Codex tool can satisfy a capability without a named MCP server. Treat sandbox restrictions and approval policy as separate controls. Ask before crossing approval boundaries, and report blocked checks after the bounded fallback defined by portable policy.

## Output Boundary

Use the portable core output contract. Mention Codex configuration, approvals, or sandbox details only when they affect the result or next decision.
