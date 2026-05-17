---
name: boundary-input-validation
description: Use when validating untrusted or boundary input in React or Next.js work without introducing new dependencies. Prefer existing project utilities, explicit parsing, and built-in TypeScript-safe guards before proposing package installs.
id: 'agents.skills.boundary-input-validation.skill'
title: 'Boundary Input Validation'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'boundary-input-validation'
tags:
    - 'agents/skill-package'
    - 'frontend/validation'
    - 'agents/skill'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/boundary-input-validation/references/no-new-deps-policy|No New Dependencies Policy]]'
    - '[[skills/boundary-input-validation/references/validation-patterns|Validation Patterns]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Boundary Input Validation

## Purpose

Validate untrusted input without defaulting to new dependencies.

## Required context

1. Read `AGENTS.md`.
2. Read `.agents/project/stack-profile.md`.
3. Read the relevant framework path index for the task.
4. Read the current parser, utility, route, or component that owns the boundary.
5. Check whether the repo already contains a helper or existing dependency that
   safely covers the same validation problem.

## Core rules

- Treat all user or external input as untrusted.
- Prefer no-new-dependency solutions first.
- Before proposing a package, check whether the package and the required version
  already exist in the repo and whether an existing helper already solves the need.
- Do not install or propose installing a package without explicit user approval.
- Keep validation at the boundary instead of scattering coercion and fallback
  logic downstream.
- If the validation strategy is not obvious from the prompt and repo, ask the
  user instead of choosing a library or schema style on your own.
- Do not introduce schema validation libraries unless the user explicitly
  approves them.

## Reference map

- `references/validation-patterns.md`
- `references/no-new-deps-policy.md`
