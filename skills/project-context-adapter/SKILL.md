---
name: project-context-adapter
description: Use when project overlays or frontend path indexes under project/** need refresh after stack, routing, styling, assets, verification commands, or source ownership changes. Keep facts local-only and framework-agnostic; do not rewrite reusable skills for project-specific details.
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
    - 'frontend/project-context'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/project-context-adapter/references/extraction-checklist|Extraction Checklist]]'
    - '[[skills/project-context-adapter/references/sync-procedure|Sync Procedure]]'
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Project Context Adapter

## Purpose

Refresh factual host-project context in `project/**` so reusable skills can
implement screenshot-derived specs without scanning the whole repository.

## When To Use

- Project structure, routes, entrypoints, styling systems, assets, or
  verification commands changed.
- A new frontend stack fact was discovered during implementation.
- Path indexes no longer match actual source files.

## When Not To Use

- First-time full onboarding in Plan Mode. Use `project-onboarding-adapter`.
- Reusable skill authoring. Use `agent-rules-skill-author`.
- Screenshot spec writing or implementation unless project facts changed.

## Required Context

1. Read `AGENTS.md`.
2. Read `SUMMARY.md`.
3. Read `common/documentation-maintenance.md`.
4. Read existing `project/**` overlays.
5. Inspect relevant manifests, configs, entrypoints, routes, components,
   styles, assets, and verification scripts.
6. Read `references/extraction-checklist.md`.
7. Read `references/sync-procedure.md`.

## Tool Contract

- Use Project Context MCP when available.
- Use filesystem reads and targeted search when Project Context MCP is
  unavailable.
- Do not use Figma MCP.
- Edit only `project/**` unless the user also requests bundle skill or policy
  changes.

## Workflow

1. Determine which project facts changed.
2. Update only affected overlays or path indexes.
3. Keep graph frontmatter current with `publishable: false` and
   `local_only: true`.
4. Keep host-project facts out of `AGENTS.md`, `SUMMARY.md`, `common/**`, and
   reusable `skills/**`.
5. Verify updated facts against actual files.

## Output Contract

Report:

- overlays updated;
- source facts used;
- project paths indexed or changed;
- verification performed;
- any project facts that remain unknown.

## Validation Gates

- `project/**` files must remain local-only.
- Path indexes must point to existing files or explicitly mark missing owners.
- Reusable skills must not receive host-specific facts.
- No Figma MCP or Figma whiteboard workflow may be introduced.

## Trigger Evals

Should trigger:

- "Refresh project context after this layout change."
- "Update .agents/project path indexes."
- "The styling profile is stale; sync it with the repo."

Should not trigger:

- "Create a design implementation spec from screenshots."
- "Implement this screen."
- "Plan first-time onboarding for a new project."

## Reference Map

- `references/extraction-checklist.md`
- `references/sync-procedure.md`
