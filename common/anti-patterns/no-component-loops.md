---
id: 'agents.common.anti-patterns.no-component-loops'
title: 'No Component Loops'
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

# No Component Loops

## Rule

Do not use imperative loops inside React component bodies.

## Bad

```tsx
const TagsPanel = ({ tags }: TagsPanelProps) => {
    const badges = tags.reduce<JSX.Element[]>((items, tag) => {
        items.push(<TagBadge key={tag.id} tag={tag} />);
        return items;
    }, []);

    return <div>{badges}</div>;
};
```

## Good

```tsx
const TagsPanel = ({ tags }: TagsPanelProps) => {
    return <TagsList tags={tags} />;
};
```

```tsx
const TagsList = ({ tags }: TagsListProps) => {
    return (
        <div>
            {tags.map((tag) => (
                <TagBadge key={tag.id} tag={tag} />
            ))}
        </div>
    );
};
```

## Apply When

Do not prepare JSX with imperative loops, reducers, manual pushes, or hidden render arrays in component bodies. Use small list components and named data helpers.
