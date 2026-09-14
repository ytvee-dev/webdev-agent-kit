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

Purpose: map portable policy to Claude Code discovery and project instructions.

## Discovery

- Native package root: `.claude-plugin/plugin.json`.
- Native skill root: `skills/` inside the installed plugin.
- Do not depend on `.agents/skills`, `.codex-plugin`, or `agents/openai.yaml` for skill discovery.

## Project Instructions

Plugin installation does not authorize project-file edits. If the project separately uses `.agents/AGENTS.md`, propose the exact root `CLAUDE.md` import `@.agents/AGENTS.md`. Create or merge it only after explicit user approval; never overwrite existing instructions.

Resolve reusable paths under the plugin root and `project/**` under host
`.agents/project/`. Never write host facts into the shared plugin.

## Tool Boundary

Detect tools from the current registry and verified project facts. Native tools
can satisfy capabilities. Packages, config, provider names, and another client's
metadata do not prove availability. Use declared fallbacks and report limits.

## Output Boundary

Use the portable core output contract. Do not add client setup narration unless setup changed, failed, or requires a user decision.
