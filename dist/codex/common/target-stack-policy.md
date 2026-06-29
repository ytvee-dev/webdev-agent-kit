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
    - '[[common/framework-adaptation-policy|Framework Adaptation Policy]]'
    - '[[common/framework-source-map|Framework Source Map]]'
depends_on: []
---

# Target Stack Policy

WebDev Assistant targets React, Next.js, CSS Modules, Redux, TanStack, and Axios.

Use local project conventions first. Use official documentation for the detected target-stack library when current behavior matters.

## Allowed Targets

- React components and hooks.
- Next.js routing and server/client boundaries.
- CSS Modules as the default styling target.
- Redux state boundaries when the project already uses Redux.
- TanStack Query, Router, or related TanStack frontend libraries when already present or explicitly approved.
- Axios API adapter work when the project already uses Axios.
- MDN for browser platform behavior.
- TypeScript documentation for typing behavior.

## Unsupported Targets By Default

Do not present other frontend frameworks, UI libraries, styling systems, or app generators as supported defaults.

Vite may be mentioned only as an already-detected build tool inside a supported React project. Do not scaffold or migrate to Vite unless the user explicitly changes the project scope.

## Approval Rule

Do not add packages, libraries, generators, global styling systems, or framework migrations without explicit user approval.
