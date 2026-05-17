---
id: 'agents.skills.frontend-typescript-rules.references.typing-patterns'
title: 'Typing Patterns'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-typescript-rules'
tags:
    - 'agents/skill-package'
    - 'frontend/typescript'
    - 'agents/reference'
parent:
    - '[[skills/frontend-typescript-rules/SKILL|Frontend TypeScript Rules]]'
related:
    []
depends_on:
    - '[[skills/frontend-typescript-rules/SKILL|Frontend TypeScript Rules]]'
---

# Typing Patterns

- Export schemas and inferred types together when using schema libraries.
- Prefer local narrow helpers over broad unsafe casts.
- Type function boundaries clearly, especially exported helpers and reusable components.
- Reuse existing shared types instead of cloning parallel versions.
