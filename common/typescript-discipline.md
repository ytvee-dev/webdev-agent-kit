---
id: 'agents.common.typescript-discipline'
title: 'TypeScript Discipline'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'frontend/typescript'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/frontend-bugfix-debugger/SKILL|Frontend Bugfix Debugger]]'
    - '[[skills/frontend-refactor-surgeon/SKILL|Frontend Refactor Surgeon]]'
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
depends_on: []
---

# TypeScript Discipline

Purpose: preserve type safety during frontend fixes, refactors, and reviews.

## Rules

- Preserve the project's TypeScript strictness.
- Prefer narrowing, discriminated unions, and explicit types over casts.
- Avoid `any` unless the project already uses it and no safer narrow type is
  available.
- Do not use forced casts to hide design errors.
- Type component props and public helpers explicitly when they cross file
  boundaries.
- Keep public types stable during refactors unless the behavior change is
  approved.
- Align with local `tsconfig` and nearby patterns before generic advice.
