---
id: 'agents.common.anti-patterns.no-parallel-status-booleans'
title: 'No Parallel Status Booleans'
doc_type: 'anti-pattern-template'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'anti-patterns/state'
parent:
    - '[[common/anti-patterns/README|Anti-Pattern Templates]]'
related:
    - '[[common/approved-patterns|Approved Patterns]]'
    - '[[common/typescript-discipline|TypeScript Discipline]]'
depends_on: []
---

# No Parallel Status Booleans

## Rule

Do not model a single lifecycle, initialization flow, loading process, request state, auth state, or wizard state as multiple boolean flags.

Use one typed discriminant status field instead.

## Avoid

```ts
type AuthState = {
  isInitialized: boolean;
  isInitializing: boolean;
  hasInitializationFailed: boolean;
};
```

This permits impossible or ambiguous states.

```ts
const isInitialized = useAppSelector((state) => state.auth.isInitialized);
const isInitializing = useAppSelector((state) => state.auth.isInitializing);
```

## Prefer

```ts
type AuthInitializationStatus = 'idle' | 'initializing' | 'initialized' | 'failed';

type AuthState = {
  initializationStatus: AuthInitializationStatus;
};
```

Use derived booleans at the edge when needed.

```ts
const initializationStatus = useAppSelector(
  (state): AuthInitializationStatus => state.auth.initializationStatus,
);

const isInitializing = initializationStatus === 'initializing';
const isInitialized = initializationStatus === 'initialized';
```

## Stronger Pattern

Use a discriminated union when each status carries different data.

```ts
type AuthInitializationState =
  | { status: 'idle' }
  | { status: 'initializing' }
  | { status: 'initialized'; userId: string }
  | { status: 'failed'; error: string };
```

## Allowed Exception

Independent facts may remain booleans when they are genuinely independent.

```ts
type FormState = {
  isDirty: boolean;
  isValid: boolean;
};
```

## Apply When

Use this whenever state fields represent one mutually exclusive lifecycle or async status.
