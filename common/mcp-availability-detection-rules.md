---
id: 'agents.common.mcp-availability-detection-rules'
title: 'MCP Availability Detection Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'mcp/capabilities'
    - 'frontend/verification'
parent:
    - '[[common/rendered-visual-verification-policy|Rendered Visual Verification Policy]]'
related:
    - '[[common/tool-capability-model|Tool Capability Model]]'
    - '[[common/smart-verification-budget|Smart Verification Budget]]'
    - '[[skills/mcp-toolchain-manager/SKILL|MCP Toolchain Manager]]'
depends_on: []
---

# MCP Availability Detection Rules

Purpose: prevent agents from wasting time or making false claims while detecting tool availability.

## Availability Sources

Detect tool availability from these sources, in order:

1. Current session tool registry when the client exposes one.
2. Validated local-only `project/mcp-profile.md` facts.
3. Client config files only when the user asked for onboarding, context refresh, or toolchain audit.
4. Targeted manual report from the user.

## Non-Proof Sources

These are not proof that an MCP server or browser capability is available:

- `package.json` dependency entries;
- lockfile entries;
- `node_modules` directories;
- local Playwright package installation;
- a running local app;
- an open network port;
- a config file that has not been validated in the current client session.

## Lightweight Boundary

For Fast Lookup, Micro UI Fix, and low-risk CSS-only changes:

- do not inspect MCP installation state;
- do not search for local browser automation packages;
- do not start a dev server merely to detect tools;
- do not read visual QA rules unless rendered visual evidence is actually in scope.

## Missing Capability Rule

When a required capability is missing:

1. Report the missing capability.
2. Report the blocked check.
3. Use the allowed fallback if it is honest.
4. Do not install or configure tools without explicit approval.

## Visual QA Rule

Use Browser or Playwright only when rendered visual evidence is required by the task. Tool availability does not make browser verification mandatory.
