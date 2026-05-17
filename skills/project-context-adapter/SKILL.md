---
name: project-context-adapter
description: Use when repo-local project overlays or framework path indexes need
    refresh so the current project can be navigated and implemented without
    scanning the whole repo.
id: 'agents.skills.project-context-adapter.skill'
title: 'Project Context Adapter'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'project-context-adapter'
tags:
    - 'agents/skill-package'
    - 'agents/project-context'
    - 'agents/skill'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/project-context-adapter/references/extraction-checklist|Extraction Checklist]]'
    - '[[skills/project-context-adapter/references/sync-procedure|Sync Procedure]]'
    - '[[project/stack-profile|Stack Profile]]'
    - '[[project/react/path-index|React Path Index]]'
    - '[[project/next/path-index|Next Path Index]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
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
