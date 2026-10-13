---
id: 'agents.common.react-performance-rules'
title: 'Conditional React And Next Performance Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'frontend/react'
    - 'performance'
parent:
    - '[[profiles/react-typescript/PROFILE]]'
related:
    - '[[common/performance-review-rules]]'
    - '[[common/anti-patterns/no-use-callback-by-default]]'
    - '[[common/data-fetching-boundary-rules]]'
depends_on: []
---

# Conditional React And Next Performance Rules

Load the relevant section when React/Next work changes data loading, server/client
boundaries, imports, subscriptions or expensive rendering. Skip unrelated copy,
CSS and non-React work. These rules guide new code and scoped review; they do not
authorize a repository-wide optimization pass, dependency or configuration change.

## Evidence And Versions

Identify installed React, renderer/framework, router, compiler, bundler and data
library versions from the project. Read current official docs for APIs whose
availability or semantics affect the decision. Prioritize observed waterfalls,
payload and render cost over speculative micro-optimizations. Preserve correctness,
accessibility, error handling and project conventions. Compare the relevant
existing trace, build output or profiler result before and after when available;
without a measurement, report a hypothesis rather than a speedup percentage.

## Independent Work And Waterfalls

- Check cheap synchronous guards before avoidable work only when side effects,
  authorization, information disclosure and error ordering remain equivalent.
- Start independent permitted reads together; await dependent work when its
  inputs are ready. Use existing promise facilities rather than installing a
  concurrency library. Bound concurrency for large lists and rate-limited APIs.
- Attach error handling to eagerly started promises. Preserve cancellation,
  stale-result protection and partial-failure semantics; Promise.all is not a
  transaction and does not cancel the other requests when one rejects.
- In supported server rendering, compose independent data consumers and use
  meaningful Suspense boundaries with stable loading layout. Do not start
  protected reads before authorization or turn ordered mutations into parallel
  operations. Preserve error boundaries and critical-content requirements.

## Imports And Payload

- Inspect actual bundle/file-trace evidence for large imports. Prefer documented,
  typed package exports; do not bypass exports with private deep paths. Account
  for existing bundler/framework import optimization before changing barrels.
- Use statically analyzable import functions for bounded module maps. Lazy-load
  heavy optional UI through the installed framework, with loading/error states.
  A window guard alone does not prove exclusion from a server or client bundle.
- Defer noncritical third-party code within consent, diagnostic and dependency
  requirements. Preserve script execution order; async is not interchangeable
  with defer. Prefer existing framework script loading when applicable.
- Preload likely needed resources only with evidence of benefit and appropriate
  privacy/bandwidth limits; do not fetch every possible route on hover by default.

## Server Boundaries And Caches

- Treat server mutations as callable entrypoints: validate input, authenticate
  and authorize each operation. Client visibility or layout guards are not proof
  of authorization. Send only client-needed, permitted serializable data.
- Minimize repeated payloads without moving expensive or sensitive work to the
  client blindly. Measure serialization; object identity is not a universal
  network-size guarantee across renderer versions.
- Reuse existing request-scoped deduplication when supported. React cache is
  a Server Component facility, not a generic persistent application cache.
  Keep stable argument identity where the API requires it and verify error reuse.
- Never store mutable current-user/request state in server module scope.
  Cross-request caches need an approved owner, bounded lifetime/size, invalidation,
  authorization-safe tenant/user keys and deployment semantics. Do not introduce
  a global Map or LRU merely because two requests resemble one another.
- Only hoist immutable, request-independent assets when startup cost, memory,
  failure recovery and refresh behavior are acceptable. Do not hoist user data.
- Use supported post-response work only for operations allowed to complete later.
  Required persistence, security audit guarantees and correctness-critical cache
  invalidation must not become untracked best-effort background work.

## Client Data And State

- Reuse the installed data owner (for example TanStack Query or SWR) for keying,
  deduplication, invalidation and mutations. Do not introduce SWR to replace a
  working project convention. Shared listeners need cleanup and correct ownership.
- Use passive touch/wheel listeners only when they never need preventDefault.
- Persist minimal versioned non-sensitive data with parsing, migration and
  storage-failure handling. In-memory storage caches need same-tab, cross-tab and
  logout invalidation; do not cache credentials as a performance optimization.
- Derive values from current props/state during render instead of synchronizing
  duplicate state through effects. Keep interaction-specific work in handlers.
  Preserve real external synchronization and complete reactive dependencies.
- Subscribe to the value the UI actually needs. Read callback-only values on
  demand when that preserves freshness. Use functional updates for prior-state
  changes and pure lazy initializers for expensive initial state; initialization
  may be repeated in development and must be safe under SSR.
- Define component types outside parent renders to preserve identity/state.
  Separate unrelated effects/computations by dependencies, not arbitrary lines.
  Refs fit non-rendered transient values, not UI that must react to changes.

## Rendering And Scheduling

- Memoize only demonstrated expensive work or consumed identity boundaries;
  simple primitive expressions do not need memo. Consider compiler behavior.
  Immutable stable defaults/static JSX can help an existing boundary, but are
  not a reason to wrap every handler or component in memoization.
- Transitions/deferred values may improve expensive nonurgent rendering in
  supported React versions. Keep controlled input updates urgent. They do not
  debounce requests, cancel network operations or guarantee async result order;
  retain stale-response and error handling. Do not replace all loading state.
- Match server and initial client output. Prefer established framework theme/data
  initialization; do not inject arbitrary pre-hydration DOM scripts. An unavoidable
  isolated mismatch may use the documented escape hatch, never blanket warning
  suppression to hide a defect. Preserve CSP and deterministic identity.
- Consider content-visibility or supported Activity only with measured need and
  keyboard, focus, find-in-page, layout and effect-lifecycle checks. Verify APIs
  against installed versions; hidden UI is not automatically inert in every design.
- Optimize SVG precision or animation wrappers only after visual/profiler checks;
  preserve viewBox, accessible names and reduced-motion behavior. No universal
  GPU-acceleration or precision claim is made. Avoid rendering numeric falsy
  values accidentally; explicit booleans or a ternary both work.

## JavaScript And Advanced Hooks

Use suitable data structures and avoid repeated hot-path work when evidence
warrants it. Include the cost of constructing indexes/caches, memory and freshness.
Do not rewrite readable map/filter code to flatMap or loops without benefit.
Batch DOM reads/writes when interleaving causes forced layout. Preserve mutation,
ordering, getter and comparison semantics; use supported immutable array methods
or an explicit copy. Shared global/sticky regex objects carry mutable lastIndex.

Idle callbacks are for deferrable work, with cancellation and compatible fallback;
they must not become the only way a required save completes. Initialization and
subscriptions need lifecycle ownership, cleanup and retry behavior; a module
boolean must not hide a failed initialization or share user state across requests.

Where supported, Effect Events express nonreactive logic called from effects,
not arbitrary stable callbacks. Follow current React restrictions and lint rules;
do not add them to effect dependencies, pass them as general handlers, or use
refs/Effect Events to conceal missing reactive dependencies.

## Source Basis

The maintainer audit of Vercel's 70-rule inventory at commit
`063bee94c3f4df8453406c830b0a7df0f2860278` is in the source documentation. This
runtime reference is an original conditional synthesis, not copied examples or
an instruction to fetch the entire upstream skill. Official semantics checked:

- [React effects](https://react.dev/learn/you-might-not-need-an-effect)
- [React cache](https://react.dev/reference/react/cache)
- [Effect Events](https://react.dev/reference/react/useEffectEvent)
- [Transitions](https://react.dev/reference/react/useTransition)
- [Hydration](https://react.dev/reference/react-dom/client/hydrateRoot)
- [Next data security](https://nextjs.org/docs/app/guides/data-security)
