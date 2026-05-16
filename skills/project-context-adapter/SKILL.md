---
name: project-context-adapter
description: Use when repo-local project overlays or framework path indexes need
    refresh so the current project can be navigated and implemented without
    scanning the whole repo.
---

# Project Context Adapter

## Goal

Refresh the factual repo-specific documentation in `.agents/project/` so the
generic skills can be reused in this repository without embedding project
details inside the skills themselves.

## Required workflow

1. Read `AGENTS.md`.
2. Inspect the project:
    - `package.json`
    - `tsconfig.json`
    - ESLint and Prettier config
    - route tree
    - styling system
    - component structure
    - validation stack
    - framework-specific lookup paths by request type
    - current source paths after code changes
3. Update only `.agents/project/**`.
4. Do not rewrite core reusable skills for repo-specific details.
5. Verify every updated project doc against the actual code and modules before
   treating it as current.

## Outputs

- `stack-profile.md`
- `architecture-map.md`
- `styling-profile.md`
- `verification-profile.md`
- `approved-patterns.md`
- `anti-patterns.md`
- `figma-profile.md`
- `react/path-index.md`
- `next/path-index.md`

## Reference map

- `references/sync-procedure.md`
- `references/extraction-checklist.md`
