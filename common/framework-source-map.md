---
id: 'agents.common.framework-source-map'
title: 'Framework Source Map'
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
    - '[[common/framework-adaptation-policy|Framework Adaptation Policy]]'
    - '[[common/target-stack-policy|Target Stack Policy]]'
depends_on: []
---

# Framework Source Map

Purpose: choose authoritative documentation sources for the supported frontend stack.

## Preferred Source Order

1. Current project overlays and configs.
2. Existing source patterns in nearby files.
3. Official documentation for the detected target-stack library.
4. MDN for browser platform behavior.

## Supported Target Sources

- React official docs.
- Next.js official docs.
- CSS Modules documentation and Next.js CSS Modules docs when the project is Next.js.
- Redux official docs.
- TanStack Query or Router official docs.
- Axios official docs.
- TypeScript official docs.
- MDN for browser platform behavior.

## Unsupported Stack Rule

Do not load framework guidance for unrelated frontend stacks. If the detected project is outside React, Next.js, CSS Modules, Redux, TanStack, or Axios scope, report the unsupported scope instead of adapting this bundle to it.
