---
id: 'agents.common.anti-patterns.no-implicit-return-types'
title: 'No Implicit Return Types'
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

# No Implicit Return Types

## Rule

New or changed functions should declare explicit return types unless a local project convention clearly requires otherwise.

Apply this especially to exported functions, helpers, mappers, predicates, selectors, adapters, hooks, handlers, and non-trivial local functions.

## Avoid

```ts
const getTitle = (notification: Notification) => notification.content.title;
```

## Prefer

```ts
const getTitle = (notification: Notification): string => notification.content.title;
```

## Component Example

```tsx
const NotificationTitle = ({ notification }: Props): JSX.Element => {
  return <h2>{notification.content.title}</h2>;
};
```

## Apply When

Use this for TypeScript implementation, bugfix, refactor, and review work.
