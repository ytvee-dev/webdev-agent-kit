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
    - '[[common/skill-applicability-policy|Skill Applicability Policy]]'
    - '[[common/framework-source-map|Framework Source Map]]'
    - '[[common/target-stack-policy|Target Stack Policy]]'
    - '[[skills/frontend-architecture-planner/SKILL|Frontend Architecture Planner]]'
depends_on: []
---

# Framework Adaptation Policy

Purpose: adapt frontend work to React, Next.js, CSS Modules, Redux, TanStack, and Axios without turning the bundle into a generic framework pack, while still allowing framework-agnostic skills to run in non-target frontend projects.

## Rules

- Detect whether the project is within the target stack before applying stack-specific guidance.
- Read `common/skill-applicability-policy.md` when the detected framework is outside the target stack or when the task may be solved by a framework-agnostic design, QA, review, lint, planning, MCP, onboarding, context, or skill-authoring workflow.
- Prefer local project conventions and overlays before generic documentation.
- Use official docs or configured docs MCP when current target-stack behavior affects correctness.
- Load only the reference needed for the detected target-stack area.
- Report unsupported scope for React/Next/CSS Modules/Redux/TanStack/Axios implementation, architecture, or greenfield guidance instead of adapting those rules to unrelated frameworks.
- Do not report the entire bundle as unusable when a framework-agnostic skill matches the task.
- Do not introduce a framework migration, package install, UI library, styling system, or test workflow by default.
