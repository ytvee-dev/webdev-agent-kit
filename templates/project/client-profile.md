---
id: 'agents.templates.project.client-profile'
title: 'Client Profile Template'
doc_type: 'template'
layer: 'template'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/template'
    - 'client/adaptation'
parent:
    - '[[skills/project-onboarding-adapter/SKILL|Project Onboarding Adapter]]'
related:
    - '[[templates/project/model-routing-profile]]'
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
depends_on: []
---

# Client Profile

Purpose: record local-only host-client facts for this project.

> Copy this template to `project/client-profile.md` during onboarding. The copied file must use `publishable: false` and `local_only: true`.

## Detected Client

- client:
- surface:
- installed package target:
- canonical target and selected alias:
- kit version and archive/checksum or commit:
- client version, OS, and shell:
- confidence:
- evidence:
- last checked:
- checked source revision:
- refresh when:

## Native Entrypoint

- expected pointer:
- existing pointer:
- created:
- updated:
- preserved:
- blocked:
- approval required:

## Instruction Files

- root `AGENTS.md`:
- root `CLAUDE.md`:
- `.cursor/rules/**`:
- `.codex/config.toml`:
- `.vscode/mcp.json`:
- `.cursor/mcp.json`:
- `.mcp.json`:

## Skill Support

Record package installation, actual client discovery, and observed invocation
separately. Use `not-run` for a skill that has not been exercised.

- native skill support:
- packaged target:
- activation method:
- Codex metadata available:
- Claude-compatible skill layout available:
- Cursor rules available:

## MCP Configuration

- config location:
- config scope:
- configured servers:
- available capabilities:
- missing capabilities:
- blocked capabilities:
- availability evidence:
- last validated:

## Fallbacks

- project files:
- official documentation:
- rendered visual evidence:
- repository metadata:

## Unknowns

## Notes

## Optional GPT Model Routing

- Approved setup scope, or not requested:
- Native delegation and format evidence:
- Local `project/model-routing-profile.md`, when created:
- Configuration fingerprint and per-role runtime activation status:
- Client/auth/config drift requiring revalidation:

An absent or unverified model profile preserves normal single-agent behavior.
