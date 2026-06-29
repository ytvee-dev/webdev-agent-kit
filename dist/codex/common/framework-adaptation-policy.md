---
id: 'agents.common.framework-adaptation-policy'
title: 'Framework Adaptation Policy'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'frontend/frameworks'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/framework-source-map|Framework Source Map]]'
    - '[[skills/frontend-architecture-planner/SKILL|Frontend Architecture Planner]]'
depends_on: []
---

# Framework Adaptation Policy

Purpose: adapt frontend work to the detected framework without turning the
bundle into stack-specific dependency automation.

## Rules

- Detect the actual framework, router, package manager, build tool, and styling
  system before applying framework guidance.
- Prefer local project conventions and overlays before generic framework docs.
- Use official docs or configured docs MCP when current framework behavior
  affects correctness.
- Load only the reference needed for the detected stack.
- Do not introduce a framework migration, package install, UI library, or
  testing workflow by default.

