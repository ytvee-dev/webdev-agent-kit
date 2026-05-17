---
id: 'agents.skills.nextjs-app-router.references.route-patterns'
title: 'Route Patterns'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'nextjs-app-router'
tags:
    - 'agents/skill-package'
    - 'frontend/nextjs'
    - 'agents/reference'
parent:
    - '[[skills/nextjs-app-router/SKILL|Next.js App Router]]'
related:
    []
depends_on:
    - '[[skills/nextjs-app-router/SKILL|Next.js App Router]]'
---

# Route Patterns

## Special file conventions

Use each file only for its intended Next.js App Router role:

| File | Role |
|---|---|
| `page.tsx` | Unique UI for the route segment |
| `layout.tsx` | Shared UI that persists across child navigations |
| `template.tsx` | Like layout but creates a new instance on every navigation — use when you need to reset client state or re-run effects on route change |
| `loading.tsx` | Suspense fallback shown while the segment streams |
| `error.tsx` | Error boundary for the segment; must be a Client Component |
| `global-error.tsx` | Error boundary for the root `layout.tsx`; required because `error.tsx` cannot catch errors in its own layout |
| `not-found.tsx` | Rendered when `notFound()` is called in the segment |
| `default.tsx` | Fallback for unmatched parallel route slots on hard navigation (browser refresh) |
| `proxy.ts` | Network boundary logic; replaces deprecated `middleware.ts` in Next.js 16. Runtime is Node.js only — edge runtime is not supported |

## Component rendering hierarchy

Within a segment, Next.js wraps files in this order (outermost first):

```
layout → template → error → loading → not-found → page
```

Key consequences:
- `loading.tsx` does NOT wrap `layout.tsx` or `error.tsx` in the same segment.
- `error.tsx` does NOT catch errors thrown inside `layout.tsx` of the same
  segment — for that use `global-error.tsx` at the root or a parent `error.tsx`.
- `template.tsx` sits between `layout.tsx` and `error.tsx`, so it re-mounts on
  every navigation while layout does not.

## Rendering mode exports

Control how a segment renders by exporting route config constants:

```ts
export const dynamic = 'auto'          // default: static when possible
export const dynamic = 'force-static'  // always static, no dynamic data
export const dynamic = 'force-dynamic' // always dynamic, skip cache

export const revalidate = 60           // ISR: revalidate every 60 seconds
export const revalidate = false        // cache indefinitely

export const dynamicParams = true      // default: allow unknown dynamic segments
export const dynamicParams = false     // return 404 for params not in generateStaticParams
```

## Static generation

- Add `generateStaticParams()` when static generation is intended and the app
  has a finite build-time list of segments.
- Pair with `dynamicParams = false` to hard-block runtime fallback.

## Fetching and caching (Next.js 16)

- Nothing is cached by default. Caching is opt-in via the `'use cache'`
  directive on a function or component.
- Use `'use cache'` at function level for data helpers, at component level for
  cacheable UI regions.
- `cache: 'force-cache'` on individual `fetch()` calls is a legacy v14 pattern;
  prefer `'use cache'` in v16.

## notFound() and Suspense

Do NOT call `notFound()` inside a component that is wrapped by `<Suspense>`.
When `notFound()` is triggered inside a Suspense boundary, Next.js returns
HTTP 200 instead of 404, which breaks SEO and crawler behavior.
Call `notFound()` at the page or layout level, before any Suspense boundary.

## General

- Keep page files thin and centered on composition.
- For dynamic resources, prefer `notFound()` over silent null rendering.
- Keep route-level fetching close to the route shell unless a reusable helper
  already owns that concern.
- Keep route metadata adjacent to the route it belongs to instead of hiding it
  inside the component body.
- Start route-oriented investigation from `.agents/project/next/path-index.md`
  before scanning the wider repo.
