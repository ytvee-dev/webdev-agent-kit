---
id: 'agents.common.frontend-design-system-rules'
title: 'Frontend Design System Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags: []
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/component-substitution-rules]]'
    - '[[common/project-fact-provenance-rules]]'
depends_on: []
---

# Frontend Design System Rules

Load when implementing or reviewing shared UI, tokens, variants, or component
wrappers. Start from the installed system and actual application usage.

## Discover Before Extending

Record the installed package version, exported component API, token source,
theme mechanism, and relevant existing examples. Compare local reference
checkouts with that version; never import runtime code from a separate checkout
or assume its newest API is already installed.

A design system includes semantic tokens, typography, spacing, interaction and
accessibility behavior, component variants, and composition guidance. Reuse
these contracts together. Do not replace an existing system or introduce a
second token vocabulary to solve one screen.

## Implement Within The Contract

- Prefer an existing component or primitive with the required behavior.
- Use verified variants and semantic tokens instead of guessed props, raw
  replacement colors, or undocumented selector overrides.
- Keep project-specific typography and styling conventions in local overlays.
  Plain CSS is valid when the project uses it; CSS Modules are conditional.
- Let primitives own their documented behavior: avoid double portals, competing
  focus management, duplicate subscriptions, or a second reconnect owner.
- Separate loading, empty, error, and disabled behavior using the actual
  component contract. Preserve focus and user state when presentation changes.
- Use composition for a domain wrapper; give it a domain name and a clear,
  deliberately bounded API.
- Propose a shared system extension only when repeated use demonstrates a gap
  and the requested scope includes that change.

## Verify

Inspect declarations and relevant implementation/examples for API claims.
For a wrapper or replacement, apply `common/component-substitution-rules.md`.
Use existing targeted checks and rendered evidence for changed interactions,
themes, responsive behavior, and visual states when required. A matching
screenshot alone does not prove keyboard, focus, or async behavior.
