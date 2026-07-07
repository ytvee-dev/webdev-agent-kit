---
id: 'agents.common.client-adaptation-policy'
title: 'Client Adaptation Policy'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'client/adaptation'
parent:
    - '[[skills/project-onboarding-adapter/SKILL|Project Onboarding Adapter]]'
related:
    - '[[common/tool-capability-model|Tool Capability Model]]'
    - '[[common/mcp-installation-policy|MCP Installation Policy]]'
    - '[[templates/root-pointers/AGENTS.codex|Codex AGENTS Pointer Template]]'
    - '[[templates/root-pointers/AGENTS.vs-code-codex|VS Code Codex AGENTS Pointer Template]]'
    - '[[templates/root-pointers/AGENTS.cursor|Cursor AGENTS Pointer Template]]'
    - '[[templates/root-pointers/CLAUDE.claude-code|Claude Code Pointer Template]]'
depends_on: []
---

# Client Adaptation Policy

Purpose: keep project adaptation native to the installed agent client while preserving one canonical bundle policy.

## Native Entrypoint Rule

During onboarding, detect the installed package target or current host client and create the smallest native pointer that the client reads by default.

Use these defaults:

- Codex and VS Code Codex: root `AGENTS.md` points to `.agents/AGENTS.md`.
- Cursor: root `AGENTS.md` points to `.agents/AGENTS.md`; Cursor rules may also point to the same policy when the Cursor target is installed.
- Claude Code and VS Code Claude: root `CLAUDE.md` points to or imports `.agents/AGENTS.md`; create root `AGENTS.md` only when the user approves cross-agent compatibility.
- Generic clients: create only the pointer explicitly requested by the user or documented by the installed target.

The root pointer must stay small. Do not mirror the full bundled policy into client-native files.

## Pointer Templates

Use the matching template when creating a new native pointer:

- `templates/root-pointers/AGENTS.codex.md`.
- `templates/root-pointers/AGENTS.vs-code-codex.md`.
- `templates/root-pointers/AGENTS.cursor.md`.
- `templates/root-pointers/CLAUDE.claude-code.md`.

For VS Code Claude, use the Claude Code pointer shape until a stricter editor-specific template is added.

## Existing Entrypoint Rule

If a host project already has `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/**`, or client config files:

1. Inspect only the minimal pointer section needed for adaptation.
2. Do not overwrite existing instructions.
3. Propose a merge when existing instructions are non-empty or ambiguous.
4. Require user approval before editing existing host instructions.

## Client Profile

Record detected client facts in local-only `project/client-profile.md`:

- installed package target;
- detected client and surface;
- confidence and evidence;
- native entrypoint;
- pointer files created, updated, preserved, or blocked;
- MCP config locations;
- available and missing tool capabilities;
- fallback rules.

## Runtime Boundary

Client adaptation is local host-project state. Keep detected client facts in `project/**`. Do not copy host-project or client-specific facts into reusable `common/**` or `skills/**` files.

## Validation Gates

- Native pointers must be minimal.
- Existing host instructions must not be overwritten without approval.
- Claude targets must not depend on Codex-only `agents/openai.yaml` files for capability discovery.
- Cursor and VS Code setup must be documented as client setup, not mandatory runtime policy.
- MCP setup remains approval-gated and capability-first.
