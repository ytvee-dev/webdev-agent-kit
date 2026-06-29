# No UseCallback By Default

Do not use `useCallback` when a normal named function works.

Bad:

```tsx
const handleSelect = useCallback((id: TagId) => onChange([id]), [onChange]);
```

Good:

```tsx
const handleSelect = (id: TagId) => {
    onChange([id]);
};
```

Allowed only when local code proves a stable reference is required.
