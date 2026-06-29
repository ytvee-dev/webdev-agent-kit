---
id: 'agents.common.anti-patterns.no-nested-array-pipelines'
title: 'No Nested Array Pipelines'
doc_type: 'anti-pattern-template'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'anti-patterns/readability'
parent:
    - '[[common/anti-patterns/README|Anti-Pattern Templates]]'
related: []
depends_on: []
---

# No Nested Array Pipelines

## Rule

Avoid unreadable nested `map`, `filter`, `reduce`, and `flatMap` chains inside components.

## Bad

```tsx
return (
    <div>
        {categories
            .filter((category) => category.tags.length > 0)
            .map((category) => (
                <section key={category.id}>
                    {category.tags
                        .filter((tag) => selectedIds.includes(tag.id))
                        .map((tag) => <TagBadge key={tag.id} tag={tag} />)}
                </section>
            ))}
    </div>
);
```

## Good

```tsx
const visibleCategories = getVisibleCategories(categories, selectedIds);

return <TagCategoryList categories={visibleCategories} />;
```

```ts
const getVisibleCategories = (
    categories: TagCategory[],
    selectedIds: string[],
): TagCategory[] => {
    return categories
        .map((category) => ({
            ...category,
            tags: category.tags.filter((tag) => selectedIds.includes(tag.id)),
        }))
        .filter((category) => category.tags.length > 0);
};
```

## Apply When

Move complex transformations into named helpers, selectors, adapters, or TanStack `select` functions when the project convention supports it.
