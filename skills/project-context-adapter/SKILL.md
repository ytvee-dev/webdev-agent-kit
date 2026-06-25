---
name: project-context-adapter
description: Use when project overlays or frontend path indexes under project/** need refresh after stack, routing, styling, assets, verification commands, docs/MCP selection, design-reference boundaries, patterns, anti-patterns, or source ownership changes. Keep facts local-only and framework-agnostic; do not rewrite reusable skills for project-specific details.
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
- Current skill MCP dependencies, available MCP servers, or official
  documentation choices changed.
- Design-reference boundaries, approved patterns, or anti-patterns changed.
- Path indexes no longer match actual source files.

## When Not To Use

- First-time full onboarding in Plan Mode. Use `project-onboarding-adapter`.
- Reusable skill authoring. Use `agent-rules-skill-author`.
- Screenshot spec writing or implementation unless project facts changed.

## Required Context

1. Read `AGENTS.md`.
2. Confirm the classified task is `project-context-refresh` or a project
   context cache update required by another task.
3. Read `common/documentation-maintenance.md`.
4. Read existing `project/**` overlays.
5. Inspect relevant manifests, configs, entrypoints, routes, components,
   styles, assets, skill `agents/openai.yaml` files, and verification scripts.
6. Read `references/extraction-checklist.md`.
7. Read `references/sync-procedure.md`.

## Tool Contract

- Use Project Context MCP when available.
- Use filesystem reads and targeted search when Project Context MCP is
  unavailable.
- Use `context7` and MDN only when refreshing official documentation choices or
  stack-specific pattern notes that depend on current external docs.
- Do not use Figma MCP.
- Edit only `project/**` unless the user also requests bundle skill or policy
  changes.

## Workflow

1. Determine which project facts changed.
2. Update only affected overlays or path indexes.
3. Refresh `project/mcp-profile.md` when skill dependencies, installed MCP
   servers, official docs choices, or verification capabilities changed.
4. Refresh `project/design-reference-profile.md` when screenshot, exported
   asset, copied inspect, or design-source boundaries changed.
5. Refresh `project/approved-patterns.md` and `project/anti-patterns.md` only
   from real project code or official documentation for the detected stack.
6. Keep graph frontmatter current with `publishable: false` and
   `local_only: true`.
7. Keep host-project facts out of `AGENTS.md`, `SUMMARY.md`, `common/**`, and
   reusable `skills/**`.
8. Verify updated facts against actual files or official documentation sources.

## Output Contract

Report:

- overlays updated;
- source facts used;
- official documentation or MCP facts refreshed;
- project paths indexed or changed;
- verification performed;
- any project facts that remain unknown.

## Validation Gates

- `project/**` files must remain local-only.
- Path indexes must point to existing files or explicitly mark missing owners.
- `project/mcp-profile.md` must match current `skills/*/agents/openai.yaml`
  dependency declarations when it is touched.
- `project/design-reference-profile.md` must not imply live design-tool access.
- Patterns and anti-patterns must cite real local code facts or official
  documentation choices, not generic preferences.
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
