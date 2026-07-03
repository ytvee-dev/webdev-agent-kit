---
id: 'agents.common.target-stack-policy'
title: 'Target Stack Policy'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'frontend/stack'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/skill-applicability-policy|Skill Applicability Policy]]'
    - '[[common/framework-adaptation-policy|Framework Adaptation Policy]]'
    - '[[common/framework-source-map|Framework Source Map]]'
depends_on: []
---

# Target Stack Policy

WebDev Agent Kit targets React, Next.js, CSS Modules, Redux, TanStack, and Axios for stack-specific implementation, architecture, greenfield, state, data, and styling guidance.

Use local project conventions first. Use official documentation for the detected target-stack library when current behavior matters.

Read `common/skill-applicability-policy.md` before deciding that no bundle skill applies to a non-target frontend project. Outside-stack projects are unsupported for stack-specific implementation guidance, but they can still use framework-agnostic design intake, visual direction, rendered visual QA, frontend quality review, existing lint verification, planning, MCP, onboarding, context, and skill-authoring workflows.

## Allowed Targets

- React components and hooks.
- Next.js routing and server/client boundaries.
- CSS Modules as the default styling target.
- Redux state boundaries when the project already uses Redux.
- TanStack Query, Router, or related TanStack frontend libraries when already present or explicitly approved.
- Axios API adapter work when the project already uses Axios.
- MDN for browser platform behavior.
- TypeScript documentation for typing behavior.

## Framework-Agnostic Allowed Use

For frontend projects outside the target stack, the bundle may still use skills that operate on screenshots, copied inspect values, exported assets, written design notes, browser-rendered evidence, viewport screenshots, console output, overflow, focus, responsive behavior, HTML, CSS, accessibility, Web APIs, browser behavior, TypeScript, existing project scripts, and `.agents` documentation.

Do not use this allowance to apply React, Next.js, CSS Modules, Redux, TanStack, or Axios implementation rules to an unrelated stack.

## Unsupported Targets By Default

Do not present other frontend frameworks, UI libraries, styling systems, or app generators as supported stack-specific defaults.

Vite may be mentioned only as an already-detected build tool inside a supported React project. Do not scaffold or migrate to Vite unless the user explicitly changes the project scope.

Non-target frontend stacks may be recorded as host-project facts for limited framework-agnostic workflows, but they are not supported targets for stack-specific implementation, architecture, or greenfield guidance by default.

## Approval Rule

Do not add packages, libraries, generators, global styling systems, or framework migrations without explicit user approval.
