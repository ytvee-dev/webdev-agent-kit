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
    - '[[common/target-stack-policy|Target Stack Policy]]'
    - '[[common/anti-patterns|Common Anti-Patterns]]'
    - '[[common/typescript-discipline|TypeScript Discipline]]'
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

## TypeScript Implementation Style

- Prefer arrow functions for new or changed functions unless local runtime semantics require otherwise.
- Add explicit return types to new or changed functions.
- Destructure named object fields when it improves clarity and does not hide nullability.

Example:

```ts
const selectNotificationTitle = (notification: Notification): string => {
  const { title } = notification.content;
  return title;
};
```

## Single Discriminant Status

Use one typed status field for one lifecycle or async state.

Prefer:

```ts
type AuthInitializationStatus = 'idle' | 'initializing' | 'initialized' | 'failed';

type AuthState = {
  initializationStatus: AuthInitializationStatus;
};
```

Use discriminated unions when each status carries different data.

```ts
type AuthInitializationState =
  | { status: 'idle' }
  | { status: 'initializing' }
  | { status: 'initialized'; userId: string }
  | { status: 'failed'; error: string };
```

## Component Decomposition

- Keep every changed component focused on one primary responsibility.
- Split screens into route or page shell, feature sections, small presentational components, list or item components, and named helpers when needed.
- Extract repeated markup into named components before final reporting.
- Extract non-trivial filtering, sorting, grouping, mapping, and formatting into named helpers, selectors, adapters, or approved hooks.
- Keep JSX readable without inline business logic.
- Do not use `renderXxx`, `xxxRender`, nested array pipelines, component-body JSX preparation, or `useCallback` to hide poor component shape.
- Apply this rule regardless of the framework, router, state library, data library, or styling system.

## Verification

- Use browser-rendered evidence for visual work when rendered visual QA is in scope.
- Compare implementation screenshots against the spec and visual references.
- Report material visual deviations instead of hiding them.
