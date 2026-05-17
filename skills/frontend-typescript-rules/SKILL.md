---
name: frontend-typescript-rules
description: Use when enforcing strict TypeScript, exported API typing, safe
    narrowing, and maintainable refactors in React or Next.js codebases.
id: 'agents.skills.frontend-typescript-rules.skill'
title: 'Frontend TypeScript Rules'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-typescript-rules'
tags:
    - 'agents/skill-package'
    - 'frontend/typescript'
    - 'agents/skill'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/frontend-typescript-rules/references/anti-patterns|Anti-Patterns]]'
    - '[[skills/frontend-typescript-rules/references/ts-rules|TypeScript Rules]]'
    - '[[skills/frontend-typescript-rules/references/typing-patterns|Typing Patterns]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Frontend TypeScript Rules

## When to use

- Refactors that touch types
- New public helpers, components, or utilities
- Boundary parsing where type inference matters
- Any task where type safety is part of the change

## Core rules

- Keep strict typing intact.
- Avoid `any` and `@ts-ignore`.
- Use `import type` for type-only imports when supported.
- Prefer inferred types from schemas and helpers over duplicated manual types.
- Add explicit return types to exported functions when it improves clarity.

## Reference map

- `references/ts-rules.md`
- `references/typing-patterns.md`
- `references/anti-patterns.md`
