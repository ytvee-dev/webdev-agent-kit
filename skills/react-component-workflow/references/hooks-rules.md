# Hooks Rules

## General rules

- Use hooks only where React requires them.
- Do not create effects for logic that can run during render or in event handlers.
- Keep dependency arrays accurate when effects are required.
- Avoid custom hooks that only hide trivial local logic.

## React 19 additions

**`ref` is now a regular prop.**
Function components accept `ref` directly — `forwardRef` is no longer needed.
Remove `forwardRef` wrappers when refactoring existing components; the old
pattern still works but is unnecessary.

```tsx
// React 19 — ref is a plain prop
function Input({ ref, ...props }) {
    return <input ref={ref} {...props} />
}
```

**`use()` — read Promises and Context.**
`use()` reads a Promise or Context value during render. Unlike other hooks it
can be called conditionally and inside loops. Integrates with Suspense and Error
Boundaries for Promise handling.

```tsx
'use client'
function UserCard({ userPromise }) {
    const user = use(userPromise) // suspends until resolved
    return <p>{user.name}</p>
}
```

**`useActionState()` — async action state.**
Manages state returned by an async action (typically a Server Action). Returns
`[state, dispatch, isPending]`. Use instead of manual `useState` + `useEffect`
patterns for form submission state.

**`useFormStatus()` — form submission status.**
Must be called from a component rendered inside a `<form>`. Returns `{ pending,
data, method, action }`. Use for disabling submit buttons or showing spinners
during submission.

**`useOptimistic()` — optimistic UI updates.**
Apply a temporary optimistic value immediately while an async operation is in
flight. Reverts automatically when the operation settles.

**`<Context>` as provider.**
Render `<ThemeContext value="dark">` directly instead of `<ThemeContext.Provider
value="dark">`. Both work; the shorter form is preferred in React 19.
