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

Purpose: map shared policy, skills and roles to Claude Code.

## Discovery

Native root: `.claude-plugin/plugin.json`; skills: `skills/`; agents: `agents/`.
Read the plugin's `AGENTS.md` through the invoked skill's `${CLAUDE_SKILL_DIR}`.
Do not require `.agents/skills`, `.codex-plugin` or `agents/openai.yaml`.
For delegation, use `common/claude-agent-routing-policy.md` and the onboarding
`references/claude-agent-bootstrap.md`. Verify actual registry names and tools.

## Project Instructions

Resolve reusable paths under the installed plugin root and `project/**` under
host `.agents/project/`. Preserve host `CLAUDE.md` and imported rules. Never write
host facts into the shared plugin. If separately installed shared project policy
is approved, use `@.agents/AGENTS.md`; never create a dangling import.
Plugin installation does not authorize host instruction replacement.

## Tool Boundary

Use current callable tools or verified local capability evidence. Configured
MCP, installed roles and model names do not prove availability or execution.
Preserve existing agents, models, permissions and global settings. Plan Mode
remains read-only; Codex role configuration does not apply.

## Output Boundary

Separate installed, discovered and exercised capabilities. Report missing evidence
and retain normal single-agent work when native delegation is unavailable.
