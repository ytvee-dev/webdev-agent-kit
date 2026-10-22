---
id: 'agents.docs.index'
title: 'WebDev Agent Kit Documentation'
doc_type: 'user-guide-index'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags:
    - 'docs/entrypoint'
parent:
    - '[[CHANGELOG|WebDev Agent Kit Changelog]]'
related:
    - '[[docs/architecture/design-system-pilot]]'
    - '[[docs/architecture/react-performance-audit]]'
    - '[[docs/release/1.3.0-plan]]'
    - '[[docs/architecture/superpowers-adoption]]'
    - '[[docs/release/1.1.0-checklist]]'
    - '[[docs/install/README|Installation Guides]]'
    - '[[docs/mcp/README|MCP for WebDev Agent Kit]]'
    - '[[docs/architecture/runtime-target-contracts|Runtime Target Contracts]]'
    - '[[docs/release/0.3.0-checklist|0.3.0 Release Checklist]]'
    - '[[docs/release/0.4.0-checklist|0.4.0 Release Checklist]]'
depends_on: []
---

# WebDev Agent Kit Documentation

[← Project home](../README.md)

## Set up and use the Kit

- [Install for your client](install/README.md)
- [Check your first installation](install/first-run.md)
- [Choose models and tools](install/model-capability-guide.md)
- [Connect and check MCP servers](mcp/README.md)
- [Select a frontend or designer role](install/roles.md)
- [Configure Codex subagents](install/gpt-model-routing.md)
- [Use Claude project context and subagents](install/claude-agents.md)
- [Update or roll back without losing local work](install/upgrade.md)
- [Ask for help or report a bug](../SUPPORT.md)

## Understand and maintain the Kit

- [Package layouts and client aliases](architecture/runtime-target-contracts.md)
- [Run and assess agent evaluations](architecture/behavior-evaluation.md)
- [Reproduce bugfix, screenshot and review cases](architecture/reproducible-workflows.md)
- [Report results from real projects](architecture/field-evidence.md)
- [React performance rule audit](architecture/react-performance-audit.md)
- [Design-system pilot — experimental](architecture/design-system-pilot.md)
- [Design choices informed by Superpowers](architecture/superpowers-adoption.md)
- [Maintainer workflow](../MAINTENANCE.md)

## Release history

Start with the [changelog](../CHANGELOG.md) for changes by version. The documents
below record plans and checks for those versions; they are not current setup guides.

- [0.3.0 checklist](release/0.3.0-checklist.md)
- [0.4.0 checklist](release/0.4.0-checklist.md)
- [0.5.0 checklist](release/0.5.0-checklist.md)
- [1.0.0 routing checks](release/1.0.0-checklist.md)
- [1.1.0 acceptance checks](release/1.1.0-checklist.md)
- [1.2.0 Claude checks](release/1.2.0-checklist.md)
- [1.3.0 implementation plan](release/1.3.0-plan.md)
- [1.4.0 learning preview plan](release/1.4.0-plan.md)

These pages are for users and maintainers. Agent instructions live in
`AGENTS.md`, `common/`, `profiles/`, `adapters/`, `skills/` and `templates/`.
