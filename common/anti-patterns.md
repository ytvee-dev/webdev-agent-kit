---
id: 'agents.common.anti-patterns'
title: 'Common Anti-Patterns'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'docs/policy'
    - 'anti-patterns'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[AGENTS|Canonical Agent Policy]]'
    - '[[common/frontend-implementation-boundaries|Frontend Implementation Boundaries]]'
    - '[[common/host-project-documentation-boundary|Host Project Documentation Boundary]]'
    - '[[common/anti-patterns/README|Anti-Pattern Templates]]'
    - '[[common/anti-patterns/no-console-file-read-before-filesystem-mcp|Filesystem First File Reads]]'
    - '[[common/anti-patterns/no-host-readme-or-docs-edits-without-approval|Host Docs Approval Boundary]]'
    - '[[skills/design-screenshot-spec/SKILL|Design Screenshot Spec]]'
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
depends_on: []
---

# Common Anti-Patterns

Purpose: define prohibited directions and route agents to small anti-pattern templates with examples.

Read `common/frontend-implementation-boundaries.md` before code-changing frontend work or frontend review.

## Concrete Code Templates

Load only the template relevant to the current code risk:

- `common/anti-patterns/no-as-const-variables.md` - do not create variables with `as const` casts.
- `common/anti-patterns/no-anonymous-functions.md` - use named components, handlers, callbacks, predicates, mappers, selectors, adapters, formatters, and helpers.
- `common/anti-patterns/no-function-declarations.md` - prefer arrow functions for new or changed functions.
- `common/anti-patterns/no-implicit-return-types.md` - add explicit return types for new or changed TypeScript functions.
- `common/anti-patterns/prefer-object-destructuring.md` - destructure named fields instead of repeating deep property access.
- `common/anti-patterns/no-parallel-status-booleans.md` - use one typed status discriminant for one lifecycle instead of mutually exclusive boolean flags.
- `common/anti-patterns/no-use-callback-by-default.md` - do not use `useCallback` when a normal function works.
- `common/anti-patterns/no-render-functions.md` - do not create `renderXxx`, `xxxRender`, or similar JSX helpers.
- `common/anti-patterns/no-nested-array-pipelines.md` - avoid unreadable chained collection expressions and split hard chains into named steps.
- `common/anti-patterns/no-component-loops.md` - avoid unclear render-side mutation and orchestration loops while allowing clear local iteration.
- `common/anti-patterns/no-test-authoring-by-default.md` - do not create or edit component, function, unit, integration, E2E, visual regression, fixture, mock, or snapshot tests unless the user explicitly asks and approves scope.
- `common/anti-patterns/no-unapproved-test-infrastructure.md` - do not add test infrastructure without approval.
- `common/anti-patterns/no-console-file-read-before-filesystem-mcp.md` - prefer the project file capability before shell file reads.
- `common/anti-patterns/no-host-readme-or-docs-edits-without-approval.md` - do not edit host README or docs without explicit documentation approval.

## Workflow Anti-Patterns

- Using Figma MCP, live Figma inspection, Figma canvas editing, Figma file creation, Figma whiteboard, design-system generation, or Code Connect workflows.
- Treating a Figma URL, file key, node id, or Figma whiteboard reference as sufficient source material.
- Implementing code before producing or receiving a `Design Implementation Spec`.
- Guessing hidden component states, assets, token names, breakpoints, or interactions when the source material does not provide them.
- Inventing CSS variables, tokens, theme names, breakpoint names, spacing names, typography names, or color names.
- Installing packages before checking whether project-native tools already solve the problem.
- Adding packages, new styling systems, global tokens, theme layers, or generated scaffolds without explicit user approval.
- Installing missing MCP servers without explicit user approval and a verified official install source.
- Creating or editing component, function, unit, integration, E2E, visual regression, fixture, mock, or snapshot tests unless the user explicitly asks for test authoring and approves the scope.
- Creating app source files, framework configs, package manifests, routes, components, styles, or build scripts during new-project onboarding.
- Replacing the project's frontend architecture with a preferred framework pattern that the project does not use.
- Hardcoding broad reusable colors, spacing, typography, or config when an existing token or local owner exists.
- Refactoring unrelated code while implementing a visual spec.
- Editing host README or host documentation as a side effect of implementation, bugfix, refactor, onboarding, visual QA, or review work.
- Using a dev server as a substitute for documented verification.
- Skipping rendered browser verification for visual implementation work when rendered visual QA is in scope.
- Interacting with production systems, production data, or live production environments.
- Publishing or copying `project/**` facts into reusable bundle docs.
