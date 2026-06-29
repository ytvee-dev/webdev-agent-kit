# No Nested Array Pipelines

Avoid unreadable nested `map`, `filter`, `reduce`, and `flatMap` chains inside components.

Bad: nested filtering and mapping directly in JSX.

Good:

```tsx
const visibleCategories = getVisibleCategories(categories, selectedIds);

return <TagCategoryList categories={visibleCategories} />;
```

Move complex transformations into named helpers, selectors, adapters, or TanStack `select` functions when the project convention supports it.
