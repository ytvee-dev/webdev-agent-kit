---
name: nextjs-app-router
description: Use when working on Next.js App Router routes, layouts, metadata, server/client boundaries, dynamic segments, and route-level UX states.
id: 'agents.skills.nextjs-app-router.skill'
title: 'Next.js App Router'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'nextjs-app-router'
tags:
    - 'agents/skill-package'
    - 'frontend/nextjs'
    - 'agents/skill'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/nextjs-app-router/references/anti-patterns|Anti-Patterns]]'
    - '[[skills/nextjs-app-router/references/figma-implementation|Figma Implementation]]'
    - '[[skills/nextjs-app-router/references/metadata-patterns|Metadata Patterns]]'
    - '[[skills/nextjs-app-router/references/route-patterns|Route Patterns]]'
    - '[[skills/nextjs-app-router/references/server-client-boundaries|Server/Client Boundaries]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Next.js App Router

## When to use

- Add or edit routes, layouts, loading states, or metadata
- Work with dynamic segments and static params
- Adjust server/client boundaries in a Next.js app
- Implement Figma-driven pages or sections inside a Next.js repository

## Required context

Before editing:

1. Read `AGENTS.md`.
2. Read `.agents/project/stack-profile.md` — framework version and project type.
3. Read `.agents/project/next/path-index.md` — targeted lookup for route work.
4. Read `.agents/project/architecture-map.md` — route tree and shared code locations.
5. Read `.agents/common/approved-patterns.md` — bundle-wide approved implementation patterns.
6. Read `.agents/project/approved-patterns.md` — host-project-specific additions and examples.
7. Read `.agents/common/anti-patterns.md` — bundle-wide patterns to avoid.
8. Read `.agents/project/anti-patterns.md` — host-project-specific additions and exceptions.
9. Read `.agents/project/styling-profile.md` — token system and styling conventions.
10. Read `.agents/project/figma-profile.md` — only when the task starts from design.

## Core rules

- Prefer MCP tools and project indexes before broad repo scanning.
- Use this lookup fallback order: `.agents/project/next/path-index.md` ->
  targeted repo search -> user clarification.
- Keep route special files focused on composition.
- Move reusable logic into helpers, feature modules, or shared code.
- Choose server/client boundaries intentionally; default to server-first.
- Derive metadata from validated or trusted data sources.
- Handle loading, error, and empty states intentionally.
- Reuse the project's existing styling system instead of introducing a new one.
- After route, metadata, helper, or component structure changes, verify whether
  `.agents/project/next/path-index.md` or related overlays need updates.

## Figma

When a task starts from a Figma URL:

1. Use the built-in Figma capabilities first.
2. Inspect component structure, variables, spacing, and layout behavior.
3. Rebuild the UI with the repo's existing patterns, tokens, and breakpoints.
4. Avoid one-off hardcoded values when a reusable token or pattern fits.
5. If Figma access fails, ask the user for screenshots and use
   `screenshot-design-inspector` before implementing UI.

## Reference map

- `references/route-patterns.md`
- `references/server-client-boundaries.md`
- `references/metadata-patterns.md`
- `references/anti-patterns.md`
- `references/figma-implementation.md`
