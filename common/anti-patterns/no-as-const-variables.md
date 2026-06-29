---
id: 'agents.common.anti-patterns.no-as-const-variables'
title: 'No As Const Variables'
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
related: []
depends_on: []
---

# No As Const Variables

## Rule

Do not create variables by appending `as const` to values.

## Bad

```ts
const routeConfig = {
    path: '/agents',
    label: 'Agents',
} as const;
```

## Good

```ts
interface RouteConfig {
    path: string;
    label: string;
}

const routeConfig: RouteConfig = {
    path: '/agents',
    label: 'Agents',
};
```

## Apply When

Use explicit types for configs, filters, state, routes, and payloads.
