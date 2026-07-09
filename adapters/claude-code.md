---
id: 'agents.adapters.claude-code'
title: 'Claude Code Client Adapter'
doc_type: 'client-adapter'
layer: 'adapter'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/adapter'
    - 'client/claude-code'
parent:
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
related:
    - '[[templates/root-pointers/CLAUDE.claude-code|Claude Code Pointer Template]]'
depends_on:
    - '[[common/core/runtime-core-policy|Portable Runtime Core Policy]]'
---

# Claude Code Client Adapter

Purpose: map portable behavior to Claude Code discovery and project instructions without redefining workflow policy.

## Discovery

- Native package root: `.claude-plugin/plugin.json`.
- Native skill root: `skills/` inside the installed plugin.
- Do not depend on `.agents/skills`, `.codex-plugin`, or `agents/openai.yaml` for skill discovery.

## Project Instructions

Plugin installation does not authorize project-file edits. If the project separately uses `.agents/AGENTS.md`, propose the exact root `CLAUDE.md` import `@.agents/AGENTS.md`. Create or merge it only after explicit user approval; never overwrite existing instructions.

## Tool Boundary

Detect tools from the current Claude Code registry and verified project capability facts. Do not infer tool availability from package dependencies or another client's metadata. Use the portable fallback when a capability is absent and report the resulting verification limit.

## Output Boundary

Use the portable core output contract. Do not add client setup narration unless setup changed, failed, or requires a user decision.
