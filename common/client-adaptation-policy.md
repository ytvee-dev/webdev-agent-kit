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
    - '[[adapters/claude-code|Claude Code Client Adapter]]'
    - '[[adapters/codex|Codex Client Adapter]]'
    - '[[adapters/cursor|Cursor Client Adapter]]'
    - '[[templates/root-pointers/AGENTS.codex|Codex AGENTS Pointer Template]]'
    - '[[templates/root-pointers/AGENTS.vs-code-codex|VS Code Codex AGENTS Pointer Template]]'
    - '[[templates/root-pointers/AGENTS.cursor|Cursor AGENTS Pointer Template]]'
    - '[[templates/root-pointers/CLAUDE.claude-code|Claude Code Pointer Template]]'
depends_on: []
---

# Client Adaptation Policy

Purpose: select the matching thin client adapter while preserving one portable core and one evidence-gated project profile.

## Native Entrypoint Rule

During source-bundle onboarding, detect the installed canonical target or compatibility alias and resolve it through `bundle-manifest.json`. A generated target does not include that internal manifest; read the sole adapter shipped under `adapters/` instead.

The adapter owns native discovery, pointer syntax, tool-registry interpretation, sandbox details, and configuration paths. It must not redefine portable workflow, safety, verification, project-profile, or output policy.

Create only the smallest native pointer allowed by the matching adapter. Do not mirror the full bundled policy into client-native files.

## Pointer Templates

Use only the pointer template linked by the matching adapter. Compatibility aliases reuse the canonical adapter and template behavior.

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
- The selected adapter must match the canonical target after alias resolution.
- Generated targets must not ship adapters for other clients.
- Client installation must not silently create or replace project instructions.
- MCP setup remains approval-gated and capability-first.
