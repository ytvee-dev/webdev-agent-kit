---
id: 'agents.common.anti-patterns.no-use-callback-by-default'
title: 'No UseCallback By Default'
doc_type: 'anti-pattern-template'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'anti-patterns/react'
parent:
    - '[[common/anti-patterns/README|Anti-Pattern Templates]]'
related:
    - '[[common/typescript-discipline|TypeScript Discipline]]'
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
    - '[[skills/frontend-refactor-surgeon/SKILL|Frontend Refactor Surgeon]]'
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
depends_on: []
---

# No UseCallback By Default

## Rule

Do not introduce `useCallback` in new or changed code by default.

A normal typed arrow function is the default.

## Bad

```tsx
const handleSelectTag = useCallback(
    (tagId: TagId): void => {
        onChange([...selectedTagIds, tagId]);
    },
    [onChange, selectedTagIds],
);
```

This is bad when no measured identity-sensitive consumer exists.

## Good

```tsx
const handleSelectTag = (tagId: TagId): void => {
    onChange([...selectedTagIds, tagId]);
};
```

## Allowed Only When Proven

`useCallback` is allowed only when all of these are true:

1. There is a measured or directly observable re-render, subscription, event bridge, or performance problem.
2. Stable callback identity is actually consumed by a memoized child, dependency-sensitive hook, subscription, event bridge, or third-party API.
3. A normal typed arrow function would cause a concrete issue.
4. The final report explains why the callback identity must be stable.

## Required Evidence

If `useCallback` is introduced, the final report must state:

- why a normal arrow function was insufficient;
- what consumes the stable function identity;
- what evidence proves the need;
- why the dependency array is safe.

## Forbidden Reasons

Do not use `useCallback` because:

- it looks optimized;
- it is described as a generic best practice;
- it might prevent re-renders without proof;
- a lint suggestion was handled by stabilizing identity before understanding the root cause;
- memoization is used to hide poor component shape.

## Review Rule

Flag newly introduced `useCallback` as a required fix unless the diff proves an identity-sensitive consumer or measured performance reason.

## Apply When

Use this during React implementation, bugfix, refactor, and review work whenever a callback is introduced or changed.
