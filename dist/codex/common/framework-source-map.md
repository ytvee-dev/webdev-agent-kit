---
id: 'agents.common.framework-source-map'
title: 'Framework Source Map'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'frontend/frameworks'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/framework-adaptation-policy|Framework Adaptation Policy]]'
depends_on: []
---

# Framework Source Map

Purpose: choose authoritative documentation sources for detected frontend
stacks.

## Preferred Source Order

1. Current project overlays and configs.
2. Existing source patterns in nearby files.
3. Official framework documentation through configured docs MCP or official
   websites.
4. MDN for browser platform behavior.

## Frameworks Covered By Policy

React, Next.js, Vue, Nuxt, Svelte/SvelteKit, Angular, Remix/React Router,
TanStack Router/Query/Start, Vite, Astro, and static HTML/CSS are supported by
policy when detected in a host project.

Do not infer a stack-specific rule when local project evidence is absent.

