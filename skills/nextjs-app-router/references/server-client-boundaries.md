# Server/Client Boundaries

## Default: server-first

Every component is a Server Component by default. Add `'use client'` only when
the component needs hooks, browser APIs, event handlers, or user interaction.

## Push `'use client'` to the leaf

Place the `'use client'` directive as deep in the tree as possible — on the
small interactive component, not on the layout or section that contains it.
Marking a parent as a Client Component forces its entire subtree into the client
bundle, losing Server Component benefits for everything below.

## Pass Server Components as children to Client Components

A Server Component can be passed as `children` or any prop to a Client
Component. The Server Component renders on the server; only the Client Component
shell ships to the browser. This is the primary way to keep interactive wrappers
small while keeping content server-rendered:

```tsx
// Server Component — no 'use client'
async function Article() {
    const content = await fetchContent()
    return <InteractiveShell>{content}</InteractiveShell>
}

// Client Component — only this crosses the boundary
'use client'
function InteractiveShell({ children }) {
    const [open, setOpen] = useState(false)
    return <div onClick={() => setOpen(!open)}>{children}</div>
}
```

## Protect server-only modules

Add `import 'server-only'` at the top of any module that must never run in the
browser (database access, secret reads, server-side parsers). This causes a
build-time error if the module is imported into a Client Component.

## Rules

- Do not import server-only modules into client code.
- Do not fetch your own route handlers from server-side code when direct module
  access is available.
- Keep async and data-loading concerns outside leaf presentation components.
- Context API and any `use*` hooks are client-only; a component that uses them
  must be marked `'use client'`.
