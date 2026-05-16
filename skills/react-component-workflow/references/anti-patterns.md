# Anti-Patterns

## General

- Duplicated state that can be derived
- Effects used as routine control flow
- Deep wrapper stacks with unclear ownership
- Over-abstracted hooks for one component
- Styling or data concerns hidden inside otherwise presentational components
- Pulling broad store, context, or custom store-like hook objects into render
  and then destructuring only a few fields
- Returning fresh objects or arrays from selector-like hooks without a
  memoization or stability strategy
- Assuming destructuring from any hook result is safe without checking whether
  the hook returns stable callbacks or reactive state
- Running `npm run dev` as part of routine task work
- Any interaction with production systems or production data
- Inventing component behavior, architecture, or missing requirements instead of
  narrowing the search and asking the user
- Installing packages before checking whether the package and version already
  exist and before getting user approval
- Adding code comments without an explicit user request or a real safety need
- Hardcoding reusable copy or links directly in JSX
- Leaving magic numbers unnamed when an existing token or clear constant should
  carry the meaning
- Adding meaningless pass-through aliases or repetitive defensive checks when
  the existing contract is already explicit
- Using function declarations where arrow functions fit the same job
- Using `useCallback`
- Using `void someFunc()`
- Using `let isCancelled = false` cancellation guards instead of `AbortController`
- Building JSX in `renderSomething` variables instead of extracting a component
- Hiding metadata or config inside component bodies instead of keeping it adjacent
- Adding duplicate component names or duplicate helper code
- Creating new global styling tokens, or using CSS grid by default, without
  explicit user approval
- Falling back to broad repo scanning before checking `.agents/project/react/path-index.md`

## React 19 specific

- Wrapping function components in `forwardRef` — refs are plain props in React 19;
  `forwardRef` is unnecessary and adds noise
- Using `useState` + `useEffect` to manage async action state when `useActionState`
  covers the same pattern more directly
- Ignoring `use()` for reading Promises in client components and falling back to
  `useEffect`-based fetching patterns that require more boilerplate
- Manually wiring up form pending state with `useState` when `useFormStatus`
  already provides `pending` from the parent `<form>`
