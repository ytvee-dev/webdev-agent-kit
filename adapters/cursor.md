---
id: 'agents.adapters.cursor'
title: 'Cursor Client Adapter'
doc_type: 'client-adapter'
layer: 'adapter'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/adapter'
    - 'client/cursor'
parent:
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
related:
    - '[[templates/root-pointers/AGENTS.cursor|Cursor AGENTS Pointer Template]]'
depends_on:
    - '[[common/core/runtime-core-policy|Portable Runtime Core Policy]]'
---

# Cursor Client Adapter

Purpose: map portable behavior to Cursor rules and shared project skills without redefining workflow policy.

## Discovery

- Native rule entrypoint: `.cursor/rules/webdev-agent-kit.mdc` at the host project root.
- Shared project skill root: `.agents/skills`.
- Shared policy: `.agents/AGENTS.md` through the approved root pointer and Cursor rule.

## Project Instructions

Keep the Cursor rule and root pointer minimal. Create or merge them only after explicit user approval, preserve existing rules, and do not duplicate the full portable policy into `.cursor/rules`.

## Tool Boundary

Detect tools from the active Cursor registry and verified project capability facts. A native Cursor tool can satisfy a capability without a named MCP server. Do not infer availability from packages, config, provider names, or another client's metadata. Use portable fallbacks and report unavailable verification honestly.

## Output Boundary

Use the portable core output contract. Mention Cursor setup only when it changed, failed, or blocks the requested work.
