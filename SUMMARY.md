---
id: 'agents.summary'
title: 'Agent Documentation Summary'
doc_type: 'summary'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/summary'
    - 'docs/navigation'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[README|WebDev Assistant README]]'
depends_on: []
---

# Agent Documentation Summary

Purpose: provide a manual catalog of the focused WebDev Assistant `.agents` bundle for humans.

This file is not part of normal agent runtime. Agents must not use this file for prompt routing or required context unless the user explicitly asks to edit, audit, or summarize `SUMMARY.md`.

## Target Stack

WebDev Assistant targets only React, Next.js, CSS Modules, Redux, TanStack, and Axios.

## Common Docs

- `common/target-stack-policy.md` - supported stack policy.
- `common/approved-patterns.md` - project-native implementation patterns.
- `common/anti-patterns.md` - prohibited workflow directions and anti-pattern template index.
- `common/anti-patterns/README.md` - small loadable anti-pattern templates with code examples.
- `common/anti-patterns/no-as-const-variables.md` - no variables created with `as const` casts.
- `common/anti-patterns/no-anonymous-functions.md` - no anonymous components, handlers, or behavior helpers.
- `common/anti-patterns/no-use-callback-by-default.md` - no `useCallback` when a normal function works.
- `common/anti-patterns/no-render-functions.md` - no `renderXxx`, `xxxRender`, or similar JSX helpers.
- `common/anti-patterns/no-nested-array-pipelines.md` - no unreadable nested maps, filters, reduces, or inline transformations.
- `common/anti-patterns/no-component-loops.md` - no imperative render preparation inside component bodies.
- `common/anti-patterns/no-tests-for-components-or-functions.md` - no tests for components or functions.
- `common/lint-verification-rules.md` - lint verification rules.
- `common/framework-source-map.md` - official source order for target-stack guidance.
- `common/framework-adaptation-policy.md` - target-stack adaptation policy.
- `common/state-ownership-rules.md` - React, Redux, and TanStack state rules.
- `common/data-fetching-boundary-rules.md` - TanStack and Axios data rules.
- `common/frontend-integration-boundaries.md` - frontend integration limits.

## Skills

- `skills/goal-planner`
- `skills/execution-plan-manager`
- `skills/mcp-toolchain-manager`
- `skills/frontend-design-director`
- `skills/frontend-architecture-planner`
- `skills/greenfield-project-builder`
- `skills/frontend-linter-manager`
- `skills/frontend-bugfix-debugger`
- `skills/frontend-refactor-surgeon`
- `skills/frontend-quality-reviewer`
- `skills/design-screenshot-spec`
- `skills/frontend-layout-implementer`
- `skills/frontend-visual-qa`
- `skills/project-onboarding-adapter`
- `skills/project-context-adapter`
- `skills/agent-rules-skill-author`

## Main Pipeline

```text
design-screenshot-spec
-> frontend-design-director
-> frontend-architecture-planner
-> frontend-layout-implementer
-> frontend-linter-manager
-> frontend-visual-qa
-> frontend-quality-reviewer
```
