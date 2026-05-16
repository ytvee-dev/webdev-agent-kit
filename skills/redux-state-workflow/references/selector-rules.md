# Selector Rules

## Subscription shape

- Prefer narrow `useSelector` or typed-selector subscriptions that expose only
  the values a component really renders or uses for control flow.
- Do not subscribe to root state or a broad slice object and then destructure a
  few fields unless the full object is the real dependency.
- Keep grouped derived reads in named selectors near the owning slice instead
  of repeating deep inline lookups across components.

## Stability rules

- If a selector must return an object or array, memoize it so unchanged inputs
  keep the same output reference.
- Do not create fresh object or array references inside non-memoized inline
  selectors.
- Use an explicit `equalityFn` only for a confirmed case where a granular
  selector would be worse, not as the default pattern.
- Distinguish stable service hooks from reactive state hooks: destructuring is
  safe only when the hook contract explicitly guarantees stable callback
  references.
