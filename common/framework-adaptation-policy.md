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
    - '[[common/target-stack-policy|Target Stack Policy]]'
    - '[[skills/frontend-architecture-planner/SKILL|Frontend Architecture Planner]]'
depends_on: []
---

# Framework Adaptation Policy

Purpose: adapt frontend work to React, Next.js, CSS Modules, Redux, TanStack, and Axios without turning the bundle into a generic framework pack.

## Rules

- Detect whether the project is within the target stack before applying guidance.
- Prefer local project conventions and overlays before generic documentation.
- Use official docs or configured docs MCP when current target-stack behavior affects correctness.
- Load only the reference needed for the detected target-stack area.
- Report unsupported scope instead of adapting to unrelated frameworks.
- Do not introduce a framework migration, package install, UI library, styling system, or test workflow by default.
