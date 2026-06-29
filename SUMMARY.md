---
id: 'agents.summary'
title: 'Agent Documentation Summary'
doc_type: 'summary'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/summary'
    - 'docs/navigation'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[README|Screenshot Frontend Assistant README]]'
depends_on: []
---

# Agent Documentation Summary

Purpose: provide a manual catalog of the reduced screenshot-to-frontend
`.agents` bundle for humans.

All paths are bundle-local paths rooted at `.agents/`. The host-root
`AGENTS.md` pointer is handled only by `project-onboarding-adapter`.

This file is not part of normal agent runtime. Agents must not use this file
for prompt routing or required context unless the user explicitly asks to edit,
audit, or summarize `SUMMARY.md`.

## Manual Catalog Use

- Use this file to inspect the published bundle shape manually.
- Keep this file synchronized when skills, common docs, project overlay names,
  or user-facing workflows change.
- Do not copy host-project facts from `project/**` into this file.

## Common Docs

- `common/approved-patterns.md` - reusable frontend screenshot-to-code
  implementation patterns.
- `common/anti-patterns.md` - prohibited workflow, Figma, tooling, and frontend
  implementation patterns.
- `common/documentation-maintenance.md` - rules for changing bundle docs and
  skill packages.
- `common/prompt-intent-routing-rules.md` - task scale routing rules that keep
  narrow prompts lightweight and reserve planning, checkpoints, and deep scans
  for standard or deep workflows.

## Project Overlays

- `project/stack-profile.md` - host-project framework, runtime, package,
  tooling, and state snapshot.
- `project/architecture-map.md` - routes, pages, shared code, and frontend
  ownership map.
- `project/styling-profile.md` - local styling systems, tokens, breakpoints,
  and CSS conventions.
- `project/verification-profile.md` - local verification commands.
- `project/approved-patterns.md` - host-project implementation addenda.
- `project/anti-patterns.md` - host-project prohibited local patterns.
- `project/mcp-profile.md` - required, available, missing, optional, approved,
  installed, skipped, or blocked MCP capabilities for current skills.
- `project/design-reference-profile.md` - local screenshot, exported asset,
  copied inspect, and design-reference boundaries.
- `project/react/path-index.md` - React/client lookup index when present.
- `project/next/path-index.md` - Next.js lookup index when present.

`project/**` is local-only and must not be copied into publishable reusable
skills or common docs.

## Skills

- `skills/goal-planner` - define a clear user goal, scope, constraints, and
  done criteria for standard or deep frontend work before implementation. It
  must not run for lightweight micro-fixes unless the task escalates.
- `skills/design-screenshot-spec` - analyze user-supplied Figma screenshots,
  copied inspect panels, assets, and notes, then produce a strict
  `Design Implementation Spec`.
- `skills/frontend-layout-implementer` - implement a `Design Implementation
  Spec` in the current frontend project while adapting to the actual stack and
  project architecture, then run rendered visual QA when applicable.
- `skills/frontend-visual-qa` - verify rendered UI against the design spec and
  visual references with automatic available Playwright MCP browser checks,
  screenshots, viewport checks, and visual diff review.
- `skills/project-onboarding-adapter` - project onboarding, host-root
  `AGENTS.md` pointer handling, stack detection, official docs/MCP selection,
  MCP dependency audit, and first project overlay creation.
- `skills/project-context-adapter` - refresh factual project overlays and
  frontend path indexes after project structure, docs/MCP choices, or
  conventions change.
- `skills/agent-rules-skill-author` - create, edit, evaluate, and validate
  `.agents` skill packages and bundle rules.

## Screenshot-To-Frontend Pipeline

Use this chain for the main workflow:

```text
design-screenshot-spec
-> frontend-layout-implementer
-> frontend-visual-qa
```

The user supplies screenshots, copied visual inspect panels, exported assets,
or notes. The agent must not use Figma MCP or inspect live Figma files.

For standard or deep work that needs goal clarity before implementation, use:

```text
goal-planner
-> selected implementation or planning skill
```

Do not insert `goal-planner` into lightweight workflows unless the task escalates.

## Prompt Intent Routing

Use `common/prompt-intent-routing-rules.md` to choose the workflow weight before
selecting a skill chain:

```text
Lightweight Workflow
Standard Workflow
Deep Workflow
```

Small bugs, obvious type errors, small styling fixes, isolated component
changes, and direct file-scope requests must stay lightweight unless targeted
inspection proves the task is larger than it first appeared.

## Navigation Rules

- Use Project Context MCP when available for project facts; otherwise read
  `project/**` and affected source files directly.
- Use Design Spec MCP when available to store or read the
  `Design Implementation Spec`; otherwise keep the spec in the response or a
  user-approved local artifact.
- Use Visual Reference MCP when available for supplied screenshots and
  reference images; otherwise rely on attached images and local files supplied
  by the user.
- Use Visual Diff MCP when available for image comparison; otherwise use the
  manual visual-diff checklist in `frontend-visual-qa`.
- Use `context7` for current framework or library documentation.
- Use `mdn` for HTML, CSS, Web APIs, and browser compatibility.
- Use Browser or Playwright MCP for rendered frontend verification.
- Use already available Browser or Playwright MCP for rendered frontend
  verification without extra user confirmation. This does not install missing
  MCP servers or bypass approval requirements for commands, package installs,
  destructive actions, or production access.
- During onboarding, scan current `skills/*/agents/openai.yaml` files for MCP
  dependencies and cache required, available, missing, optional, approved,
  installed, skipped, or blocked capabilities in `project/mcp-profile.md`.
- Install missing MCP servers only after explicit user approval and verified
  official install source.
- Never use Figma MCP or Figma whiteboard tooling in this bundle.
