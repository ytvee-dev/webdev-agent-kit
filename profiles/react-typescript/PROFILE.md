---
id: 'agents.profiles.react-typescript.profile'
title: 'React TypeScript Project Profile'
doc_type: 'project-profile'
layer: 'profile'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/profile'
    - 'frontend/react'
    - 'frontend/typescript'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/target-stack-policy|Target Stack Policy]]'
    - '[[common/skill-applicability-policy|Skill Applicability Policy]]'
    - '[[common/typescript-discipline|TypeScript Discipline]]'
depends_on:
    - '[[common/core/runtime-core-policy|Portable Runtime Core Policy]]'
---

# React TypeScript Project Profile

Purpose: activate the bundle's React and TypeScript defaults only when repository evidence shows that they apply.

## Activation Evidence

Confirm the stack from manifests, lockfiles, configuration, imports, routes, source files, and existing verification scripts. Claims in a human-facing overview are never sufficient as the only source of truth.

Activate only the rules needed by the changed surface. Do not load the full profile rule set for a narrow task.

## Supported Defaults

- React components, hooks, composition, ownership, and render behavior.
- Next.js routing and server/client boundaries when the project uses Next.js.
- TypeScript with explicit public and boundary contracts.
- CSS Modules when already used or explicitly selected.
- Redux, TanStack libraries, and Axios only when detected or explicitly approved.

Use the owning policies rather than repeating them:

- stack scope and outside-stack behavior: `common/target-stack-policy.md` and `common/skill-applicability-policy.md`;
- TypeScript: `common/typescript-discipline.md`;
- component boundaries: `common/frontend-implementation-boundaries.md`;
- state and data: `common/state-ownership-rules.md`, `common/data-fetching-boundary-rules.md`, and `common/frontend-integration-boundaries.md`;
- routing and styling: `common/routing-boundary-rules.md` and `common/css-modules-specificity-rules.md`;
- verification: `common/diff-impact-verification-rules.md` and `common/smart-verification-budget.md`.

## Override Boundary

Local project conventions override profile defaults when they are verified in current source or configuration. They do not override the portable core's user constraints, approval requirements, safety boundaries, or evidence and verification rules.

If the project uses another stack, keep only framework-agnostic workflows whose normal trigger matches. Do not apply React, Next.js, CSS Modules, Redux, TanStack, or Axios implementation rules by analogy.

## Context Economy

Read this profile once to select the relevant owning policies, then load only those policies and skill references. Prefer nearby implementation patterns and exact changed-file dependencies over broad framework review.
