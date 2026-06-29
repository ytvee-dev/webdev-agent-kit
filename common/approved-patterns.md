---
id: 'agents.common.approved-patterns'
title: 'Approved Patterns'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'docs/policy'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[SUMMARY|Agent Documentation Summary]]'
    - '[[common/target-stack-policy|Target Stack Policy]]'
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
depends_on: []
---

# Approved Patterns

Purpose: define reusable patterns for React, Next.js, CSS Modules, Redux, TanStack, and Axios frontend implementation.

## Source-First Design Intake

- Treat user-supplied screenshots, copied inspect panels, exported assets, and written notes as the design source.
- Convert visual input into a `Design Implementation Spec` before editing code.
- Keep unknown states, breakpoints, assets, and token values explicit.

## Project-Native Implementation

- Confirm the target area is React, Next.js, CSS Modules, Redux, TanStack, or Axios before applying stack guidance.
- Reuse existing React components, Next.js routes, CSS Modules, Redux slices, TanStack conventions, Axios clients, tokens, breakpoints, and verification commands.
- Keep styles local to the edited surface by default through CSS Modules.
- Touch global CSS only when the existing project has a specific global owner and the task requires it.

## Verification

- Use browser-rendered evidence for visual work.
- Compare implementation screenshots against the spec and visual references.
- Report material visual deviations instead of hiding them.
