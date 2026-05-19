---
id: 'agents.skills.react-component-workflow.references.typescript-rules'
title: 'TypeScript Rules'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'react-component-workflow'
tags:
    - 'agents/skill-package'
    - 'frontend/react'
    - 'frontend/typescript'
    - 'agents/reference'
parent:
    - '[[skills/react-component-workflow/SKILL|React Component Workflow]]'
related:
    []
depends_on:
    - '[[skills/react-component-workflow/SKILL|React Component Workflow]]'
---

# TypeScript Rules

Use this reference when React work touches component props, exported helpers,
public component APIs, reusable utilities, narrowing, or type-heavy refactors.

## Core rules

- Preserve strict typing assumptions.
- Do not use `any`, `@ts-ignore`, unsafe double casts, `Function`, broad
  `object`, or broad `Record<string, unknown>` fallbacks when a concrete type
  exists.
- Use `import type` for type-only imports when supported by the project.
- Prefer inferred types from existing schemas, helpers, and component contracts
  over duplicated manual types.
- Reuse shared types instead of cloning parallel versions that can drift.
- Add explicit return types to exported functions when that clarifies the API.
- Use discriminated unions or proper type guards for behavior branches instead
  of asserting with `as`.

## React typing patterns

- Keep component props concrete and local to the owning component unless they
  are intentionally shared.
- Avoid exposing implementation detail through props just to make a split
  component compile.
- Prefer narrow event handler signatures over `Function` or untyped callback
  props.
- Keep generic component APIs rare and justified by real reuse.
- Type boundary data only after runtime validation has established the shape.

## Review points

- Check whether a type was copied from a source object or schema instead of
  derived.
- Check whether a type assertion hides a missing runtime guard.
- Check whether a public helper or component API is clear enough for another
  caller without reading implementation internals.
