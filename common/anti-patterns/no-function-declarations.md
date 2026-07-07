---
id: 'agents.common.anti-patterns.no-function-declarations'
title: 'No Function Declarations By Default'
doc_type: 'anti-pattern-template'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'anti-patterns/typescript'
parent:
    - '[[common/anti-patterns/README|Anti-Pattern Templates]]'
related:
    - '[[common/typescript-discipline|TypeScript Discipline]]'
depends_on: []
---

# No Function Declarations By Default

## Rule

Use arrow functions for new or changed functions unless framework/runtime semantics or nearby project convention require a function declaration.

## Avoid

```ts
function selectTitle(notification: Notification): string {
  return notification.content.title;
}
```

## Prefer

```ts
const selectTitle = (notification: Notification): string => {
  return notification.content.title;
};
```

## Allowed Exception

Use a function declaration only when it is required by the local file pattern, overload style, hoisting requirement, framework contract, or runtime API.

## Apply When

Use this for TypeScript implementation, bugfix, refactor, and review work.
