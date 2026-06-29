---
id: 'agents.common.anti-patterns.no-render-functions'
title: 'No Render Functions'
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

# No Render Functions

## Rule

Do not create JSX-returning helpers or variables named `renderXxx`, `xxxRender`, `renderSomething`, or similar inside components.

## Bad

```tsx
const renderTags = () => {
    return tags.map((tag) => <TagBadge key={tag.id} tag={tag} />);
};

return <div>{renderTags()}</div>;
```

## Good

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

return <TagsList tags={tags} />;
```

## Apply When

Extract markup into named components. Use booleans for visibility and data variables for data.
