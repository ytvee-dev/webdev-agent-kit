---
id: 'agents.skills.frontend-review-and-fix.references.review-checklist'
title: 'Review Checklist'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-review-and-fix'
tags:
    - 'agents/skill-package'
    - 'frontend/review'
    - 'agents/reference'
parent:
    - '[[skills/frontend-review-and-fix/SKILL|Frontend Review and Fix]]'
related:
    []
depends_on:
    - '[[skills/frontend-review-and-fix/SKILL|Frontend Review and Fix]]'
---

# Review Checklist

## Code quality

- Does the change follow the current repo patterns and styling system?
- Is the data flow explicit and understandable?
- Are there unnecessary abstractions, wrappers, or hooks?
- Did the change introduce framework misuse or hidden coupling?
- Are types, boundary validation, and error states handled clearly?
- Did the change introduce duplicated code, duplicate component names, magic
  numbers, hardcoded reusable text/links, or hidden metadata/config?
- Did the change introduce object-literal `as const`, meaningless pass-through
  aliases, or repetitive defensive checks that the existing contract already
  covers?
- Did the change introduce `useCallback`, `void someFunc()`, `renderSomething`
  JSX variables, or `let isCancelled = false` cancellation guards?
- Did the change add code comments or feature tests without an explicit user
  request?
- Did the change add new packages or global tokens without an explicit user
  approval trail?

## Next.js 16 specifics

- Are `params`, `searchParams`, `cookies()`, `headers()` awaited before use?
- Is caching expressed via `'use cache'` rather than the legacy `cache: 'force-cache'`
  on individual `fetch()` calls?
- Is `notFound()` called outside any `<Suspense>` boundary?
- Does the root layout have `metadataBase` set if relative OG image paths are used?

## Performance

- Does the change add a large new client bundle entry when a Server Component
  would serve the same purpose?
- Are there `useEffect` calls that duplicate logic that could run during render
  or in an event handler?
- Is flexbox used where it would solve the layout without resorting to grid?
- If store, context, or selectors were touched, did the change widen
  subscriptions unnecessarily or introduce fresh object/array selector results
  without a stability strategy?
- If shared state was touched, did Redux or another store absorb transport logic
  or heavy processing that should live outside the state layer?
- If hook destructuring was introduced, is it backed by a stable service-hook
  contract rather than a reactive state object?

## Accessibility

- Do interactive elements have accessible labels (`aria-label`, `aria-labelledby`,
  or visible text)?
- Are images given descriptive `alt` attributes?
- Does keyboard navigation work for any new interactive elements?

## Security

- Are any environment variables that should be server-only accidentally prefixed
  with `NEXT_PUBLIC_`?
- Is user-supplied content rendered safely (no `dangerouslySetInnerHTML` on
  untrusted input)?
