---
id: 'agents.common.anti-patterns.prefer-object-destructuring'
title: 'Prefer Object Destructuring'
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

# Prefer Object Destructuring

## Rule

Prefer object destructuring when reading semantically named fields from an object, especially when the nested owner is already meaningful.

## Avoid

```ts
const title = notification.content.title;
const body = notification.content.body;
```

## Prefer

```ts
const { title, body } = notification.content;
```

## Single Field Example

Avoid repetitive deep property access when a named object boundary is clearer.

```ts
const { title } = notification.content;
```

## Exception

Do not destructure when it hides nullability, optional chaining, expensive getters, or a project convention that intentionally keeps the full path visible.

## Apply When

Use this for TypeScript implementation, bugfix, refactor, and review work.
