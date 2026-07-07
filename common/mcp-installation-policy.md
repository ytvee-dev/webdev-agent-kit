---
id: 'agents.common.mcp-installation-policy'
title: 'MCP Installation Policy'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'agents/tooling'
    - 'mcp/security'
parent:
    - '[[skills/mcp-toolchain-manager/SKILL|MCP Toolchain Manager]]'
related:
    - '[[common/tool-capability-model|Tool Capability Model]]'
    - '[[common/codex-official-docs-policy|Codex Official Docs Policy]]'
depends_on: []
---

# MCP Installation Policy

Purpose: keep MCP setup deliberate, source-backed, client-specific, and safe.

## Installation Boundary

The bundle may detect required capabilities and propose MCP server candidates, but it must not install, enable, authenticate, or configure an MCP server without explicit user approval in the current task.

Approval must name:

- capability being satisfied;
- server or provider name;
- official source checked;
- target client and config scope;
- exact install or config action;
- validation command or session check;
- security, credential, network, and persistence risks.

## Official Source Rule

Accepted sources:

- official project documentation;
- official vendor documentation;
- official package repository owned by the maintainer;
- trusted repository owned by the server maintainer.

Rejected sources:

- random blog snippets;
- search result summaries;
- unverified package names;
- unofficial forks;
- generated guesses.

## Client-Specific Setup

MCP configuration is host-client setup, not reusable runtime policy text. Keep reusable rules capability-based. Keep actual installed server facts in local-only `project/mcp-profile.md`.

When setup depends on client behavior, check official documentation for the detected client before proposing commands or file locations.

## Secrets And Credentials

Do not hardcode API keys, tokens, cookies, or credentials in reusable docs, committed config snippets, or project overlays.

Use environment-variable placeholders or the host client's supported secret mechanism. If a server requires authentication, report the required secret shape and ask the user to configure it outside the reusable bundle.

## Fallback Rule

When an MCP server is missing:

1. Report the missing capability.
2. Report what cannot be verified or automated.
3. Use the allowed fallback when it is honest and task-appropriate.
4. Report lower confidence or blocked checks.
5. Do not turn a small code task into a tool-install task unless the user asked for tool setup or the missing capability blocks required verification.

## Validation Gates

Before finishing MCP setup work, verify:

- no server was installed without explicit approval;
- no client config was changed without explicit approval;
- official sources were recorded;
- missing capability impact was reported;
- fallbacks were honest;
- no production systems, secrets, or user accounts were accessed;
- no Figma or live design-tool workflow was introduced as a fallback for this bundle.
