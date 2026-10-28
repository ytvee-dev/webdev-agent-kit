---
id: 'agents.adapters.kimi'
title: 'Kimi Code Adapter'
doc_type: 'adapter'
layer: 'adapter'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/adapter'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related: []
depends_on:
    - '[[common/core/runtime-core-policy|Portable Runtime Core]]'
---

# Kimi Code Adapter

Use the portable runtime core and host instructions. This adapter targets Kimi
Code CLI with project `.agents/skills` discovery, including K3 when available
in the user's account. Preserve selected models, permissions and authentication.

Extract the Kimi project archive into the project root, preserving existing
`.agents/project` and `.agents/learning` state. Start a fresh session and invoke
`/skill:project-context-adapter` to verify skill discovery, references and tools.
Each generated skill loads the policy through `${KIMI_SKILL_DIR}`. Do not replace
an existing host AGENTS.md to activate this package.

Use actually available filesystem, shell, browser and MCP capabilities. Subagents require verified availability and scoped handoffs. Do not reuse
Codex/Claude configurations or install dependencies implicitly.

Learning remains opt-in. Use portable Python memory commands and explicit canonical JSONL imports. This
release does not install a Kimi capture hook or parse undocumented transcripts.
Codex/OpenCode proposal runners are not evidence of a Kimi model evaluation;
report an unavailable evaluator rather than claiming a live Kimi pass.

## Official References

- [Skills and project discovery](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html)
- [Agents and tool boundaries](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/agents.html)

Inspected 2026-10-28. Packaging checks do not prove live client behavior.
