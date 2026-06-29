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
related: []
depends_on: []
---

# No UseCallback By Default

## Rule

Do not use `useCallback` when the same behavior can be implemented with a normal named function.

## Bad

```tsx
const handleSelectTag = useCallback(
    (tagId: TagId) => {
        onChange([...selectedTagIds, tagId]);
    },
    [onChange, selectedTagIds],
);
```

## Good

```tsx
const handleSelectTag = (tagId: TagId) => {
    onChange([...selectedTagIds, tagId]);
};
```

## Allowed Only When

- A memoized child requires a stable function reference and local code proves it.
- A hook dependency would otherwise cause a real repeated side effect.
- Existing project convention requires it.

Do not use `useCallback` to make code look optimized.
