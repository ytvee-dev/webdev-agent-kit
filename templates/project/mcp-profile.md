---
id: 'agents.templates.project.mcp-profile'
title: 'MCP Profile Template'
doc_type: 'template'
layer: 'template'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/template'
    - 'mcp/capabilities'
parent:
    - '[[skills/mcp-toolchain-manager/SKILL|MCP Toolchain Manager]]'
related:
    - '[[common/tool-capability-model|Tool Capability Model]]'
    - '[[common/mcp-installation-policy|MCP Installation Policy]]'
depends_on: []
---

# MCP Profile

Purpose: record local-only MCP and tool capability facts for this project.

> Copy this template to `project/mcp-profile.md` during onboarding or toolchain refresh. The copied file must use `publishable: false` and `local_only: true`.

## Client

- client:
- config scope:
- config file:
- last checked:

## Capability State

| Capability | Status | Provider | Required By | Fallback | Confidence Impact |
| --- | --- | --- | --- | --- | --- |

## Configured MCP Servers

| Server | Client Name | Transport | Source | Trusted | Validation |
| --- | --- | --- | --- | --- | --- |

## Missing Capabilities

## Optional Capabilities

## Blocked Capabilities

## Official Sources Verified

## Approval State

## Validation Results

## Allowed Fallbacks

## Notes
