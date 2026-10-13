---
id: 'agents.docs.architecture.react-performance-audit'
title: 'React Performance Coverage Audit'
doc_type: 'guide'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags:
    - 'frontend/react'
    - 'audit'
parent:
    - '[[docs/README]]'
related:
    - '[[common/react-performance-rules]]'
    - '[[docs/release/1.3.0-plan]]'
depends_on: []
---

# React Performance Coverage Audit

## Scope And Source

Issue #71 requested coverage against Vercel's React guidance. Reviewed on
2026-10-13 against [the pinned skill](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/skills/react-best-practices/SKILL.md)
and its 70 rule files at that revision. `_sections` and `_template` are authoring
files, not rules. This audit records original Kit decisions; upstream examples
are not vendored. It is an inventory/contract audit, not 70 executed benchmarks.

Baseline 1.2.0 had broad performance priorities, state/data boundaries and an
explicit restriction on speculative memoization. It did not establish complete
rule-by-rule coverage. The owning runtime synthesis is
[Conditional React And Next Performance Rules](../../common/react-performance-rules.md).
Its sections are loaded only for relevant React/Next work. Current React docs
were checked for cache, effects, Effect Events, transitions and hydration;
Next documentation was checked for server data security. Installed host versions
still determine applicability.

## Dispositions

- Added: an explicit missing instruction is now present.
- Clarified: an existing principle now has a concrete boundary.
- Adapted: preserve the goal while correcting scope or avoiding a prescribed dependency.
- Conditional: candidate technique, only with the stated version/evidence conditions.
- Not adopted: the blanket prescription is rejected; a scoped exception may be valid.

None of these labels means measured performance improvement. No policy requires
installing better-all, SWR, an LRU package, an optimizer or new test infrastructure.

## Coverage By Owner Section

The table groups map to sections of the runtime reference. Security, host
conventions and evidence requirements apply to every row.

### Independent Work And Waterfalls

| Upstream rule | Disposition | Kit decision and condition |
| --- | --- | --- |
| `async-api-routes` | Added | Overlap independent permitted work, preserve authorization and attach rejection handling. |
| `async-cheap-condition-before-await` | Added | Reorder only cheap independent guards without changing side effects or information disclosure. |
| `async-defer-await` | Added | Avoid unused work without changing required security and error ordering. |
| `async-dependencies` | Adapted | Use existing promise facilities; no mandatory better-all dependency. |
| `async-parallel` | Added | Parallelize independent reads with bounded concurrency; no ordered mutations or cancellation claims. |
| `async-suspense-boundaries` | Conditional | Use supported streaming with meaningful loading/error boundaries and stable layout. |

### Imports And Payload

| Upstream rule | Disposition | Kit decision and condition |
| --- | --- | --- |
| `bundle-analyzable-paths` | Added | Use bounded literal import functions and inspect actual output tracing. |
| `bundle-barrel-imports` | Adapted | Check bundle evidence, package exports/types and existing optimizer before changing imports. |
| `bundle-conditional` | Adapted | Lazy-load optional modules; a window check is not proof of bundle exclusion. |
| `bundle-defer-third-party` | Conditional | Preserve consent, diagnostics and script dependencies while deferring noncritical code. |
| `bundle-dynamic-imports` | Conditional | Use the installed framework and loading/error contracts, not next/dynamic in unrelated stacks. |
| `bundle-preload` | Conditional | Budget bandwidth and privacy; preload evidenced likely resources, not every route. |

### Server Boundaries And Caches

| Upstream rule | Disposition | Kit decision and condition |
| --- | --- | --- |
| `server-after-nonblocking` | Conditional | Check runtime guarantees; do not defer correctness-critical persistence/invalidation blindly. |
| `server-auth-actions` | Added | Validate input and authenticate/authorize every mutation entrypoint. |
| `server-cache-lru` | Not adopted | No blanket cross-request cache; require approved isolation, bounds, invalidation and deployment semantics. |
| `server-cache-react` | Conditional | Use only supported Server Component request scope; verify identity and cached errors. |
| `server-dedup-props` | Adapted | Measure payload; do not move costly or sensitive work to client or assume wire-size guarantees. |
| `server-hoist-static-io` | Conditional | Only immutable request-independent assets with bounded memory and failure/refresh behavior. |
| `server-no-shared-module-state` | Added | Keep mutable request/user data out of shared server module state. |
| `server-parallel-fetching` | Added | Compose independent permitted consumers without delaying them behind unrelated data. |
| `server-parallel-nested-fetching` | Adapted | Chain each item when ready with bounded fan-out and preserved failure handling. |
| `server-serialization` | Added | Send only required permitted fields; preserve server-only data boundaries. |

### Client Data And State

| Upstream rule | Disposition | Kit decision and condition |
| --- | --- | --- |
| `client-event-listeners` | Adapted | Share and clean up listeners through current ownership; do not require SWRSubscription. |
| `client-localstorage-schema` | Added | Minimal versioned non-sensitive values with validation, migration and failure handling. |
| `client-passive-event-listeners` | Conditional | Only passive listeners that never need preventDefault; preserve gesture behavior. |
| `client-swr-dedup` | Adapted | Keep installed TanStack/SWR ownership and keys; do not install or migrate data libraries. |

### Rendering And Scheduling

| Upstream rule | Disposition | Kit decision and condition |
| --- | --- | --- |
| `rendering-activity` | Conditional | Check installed API and hidden-subtree focus, state and effect semantics. |
| `rendering-animate-svg-wrapper` | Conditional | Profile and visually compare; no universal GPU acceleration claim. |
| `rendering-conditional-render` | Adapted | Prevent numeric falsy output; explicit boolean conditions are also valid. |
| `rendering-content-visibility` | Conditional | Measure and verify layout, focus, keyboard and find-in-page behavior. |
| `rendering-hoist-jsx` | Conditional | Keep truly static identity and account for compiler; avoid blanket hoisting. |
| `rendering-hydration-no-flicker` | Not adopted | No generic pre-hydration DOM injection; use approved framework initialization and CSP. |
| `rendering-hydration-suppress-warning` | Not adopted | Repair mismatches first; only narrow documented escape hatches for unavoidable differences. |
| `rendering-resource-hints` | Conditional | Verify installed APIs, expected resources, bandwidth and privacy impact. |
| `rendering-script-defer-async` | Adapted | Preserve dependency ordering; async and defer have different semantics. |
| `rendering-svg-precision` | Conditional | Verify visual fidelity and viewBox across sizes before lossy changes. |
| `rendering-usetransition-loading` | Not adopted | Do not replace every loading flag; transitions do not cancel or order network requests. |
| `rerender-defer-reads` | Conditional | Defer callback-only reads without making rendered state stale. |
| `rerender-dependencies` | Adapted | Keep complete reactive dependencies; narrow values by meaning, not lint suppression. |
| `rerender-derived-state-no-effect` | Added | Compute derived values without redundant state/effect synchronization. |
| `rerender-derived-state` | Added | Subscribe to the UI-needed value through existing state ownership. |
| `rerender-functional-setstate` | Added | Use pure prior-state updates to avoid stale closures; direct assignments remain valid. |
| `rerender-lazy-state-init` | Adapted | Keep initializer pure and SSR-safe; development can invoke it repeatedly. |
| `rerender-memo-with-default-value` | Conditional | Use immutable stable defaults only where identity affects an existing boundary. |
| `rerender-memo` | Clarified | Existing performance and callback policies already require evidence; account for compiler. |
| `rerender-move-effect-to-event` | Added | Run interaction-specific effects in their owning handler, preserving external synchronization. |
| `rerender-no-inline-components` | Added | Keep component type identity stable to preserve state and focus. |
| `rerender-simple-expression-in-memo` | Clarified | Existing no-speculative-memo policy applies; simple primitive work needs no cache. |
| `rerender-split-combined-hooks` | Conditional | Split independent dependencies when useful; preserve lifecycle ordering. |
| `rerender-transitions` | Adapted | Use for nonurgent supported rendering; preserve urgent input and race handling. |
| `rerender-use-deferred-value` | Conditional | Evaluate expensive rendering; deferred values are not network debouncing. |
| `rerender-use-ref-transient-values` | Adapted | Use refs for non-rendered transient values; visible UI still needs reactive state. |

### JavaScript And Advanced Hooks

| Upstream rule | Disposition | Kit decision and condition |
| --- | --- | --- |
| `advanced-effect-event-deps` | Conditional | Use only supported Effect Events; omit them from dependencies while retaining reactive values. |
| `advanced-event-handler-refs` | Adapted | Preserve subscription cleanup and freshness; Effect Events are not general stable handlers. |
| `advanced-init-once` | Adapted | Own initialization lifecycle and failure recovery; no request-shared user state or blind module guard. |
| `advanced-use-latest` | Adapted | Do not hide reactive dependencies; check installed React restrictions and lint behavior. |
| `js-batch-dom-css` | Added | Batch reads/writes for observed forced layout while preserving project styling conventions. |
| `js-cache-function-results` | Not adopted | No blanket module Map; require scope, size, invalidation and authorization-safe ownership. |
| `js-cache-property-access` | Conditional | Profile hot paths; property getters and dynamic values may change semantics. |
| `js-cache-storage` | Conditional | Require freshness and same-tab/cross-tab/logout invalidation; never cache credentials for speed. |
| `js-combine-iterations` | Conditional | Optimize measured work while preserving readable code, ordering and callback semantics. |
| `js-early-exit` | Conditional | Preserve required side effects and correctness before reducing work. |
| `js-flatmap-filter` | Not adopted | No blanket rewrite; flatMap allocations and truthiness changes require evidence. |
| `js-hoist-regexp` | Conditional | Account for global/sticky lastIndex and actual allocation cost. |
| `js-index-maps` | Conditional | Include index build/memory cost, duplicate-key behavior and freshness. |
| `js-length-check-first` | Conditional | Only when length is a necessary part of the required equality semantics. |
| `js-min-max-loop` | Conditional | Use suitable algorithms for measured work; preserve empty/NaN/tie behavior. |
| `js-request-idle-callback` | Adapted | Only deferrable work with cancellation/fallback; never the only required save path. |
| `js-set-map-lookups` | Conditional | Amortize construction and preserve identity/equality behavior. |
| `js-tosorted-immutable` | Adapted | Preserve props/state immutability using supported methods or explicit copies. |

## Verification And Follow-up

Inventory comparison found exactly 70 unique rows, matching the pinned upstream
rule files without omissions or extras. Prepared evaluation scenarios exercise
data-library preservation, authentication-before-protected-work, request cache
isolation, effect dependencies and false transition/cancellation claims. The
existing runner validates preparation and synthetic execution separately from
real model traces. No live React project speedup or agent-behavior pass is claimed.
