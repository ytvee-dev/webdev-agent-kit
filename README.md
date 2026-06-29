---
id: 'agents.readme'
title: 'Screenshot Frontend Assistant'
doc_type: 'readme'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/readme'
    - 'docs/onboarding'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[SUMMARY|Agent Documentation Summary]]'
depends_on: []
---

# Screenshot Frontend Assistant

This `.agents` bundle gives Codex a strict frontend workflow for turning
user-supplied Figma screenshots and copied visual inspect material into
production frontend code.

It is built for the official OpenAI Codex IDE extension workflow. It is not a
Figma MCP workflow and does not support Figma whiteboard workflows, Figma canvas
editing, Figma file creation, design-system generation, or Code Connect.

## Core Flow

```text
design-screenshot-spec
-> frontend-layout-implementer
-> frontend-visual-qa
```

1. `design-screenshot-spec` reads supplied screenshots, inspect panels, assets,
   and notes, then produces a `Design Implementation Spec`.
2. `frontend-layout-implementer` implements that spec in the current frontend
   project using project context and the actual stack.
3. `frontend-visual-qa` verifies the rendered UI with browser screenshots,
   viewport checks, console/runtime review, and visual diff review. When
   Playwright MCP is available, Codex runs those browser checks automatically
   after implementation without asking for separate confirmation.

For standard or deep work that needs goal clarity and task slicing before
implementation, use:

```text
goal-planner
-> execution-plan-manager
-> selected implementation or planning skill
```

Do not insert `goal-planner` or `execution-plan-manager` into lightweight
workflows unless the task escalates.

## Prompt Intent Routing

The bundle classifies prompt scale before selecting a skill chain:

```text
Lightweight Workflow
Standard Workflow
Deep Workflow
```

Small bugs, obvious type errors, small styling fixes, isolated component
changes, and direct file-scope requests stay lightweight. They should not create
persistent goal files, execution plans, progress logs, decision logs, broad
scans, or MCP installation checks unless targeted inspection proves the task is
larger than it first appeared.

Use `common/prompt-intent-routing-rules.md` when a prompt could be confused
between a narrow fix and a larger workflow.

## Source Material

Supported inputs:

- screenshots of Figma frames, components, pages, or inspect panels;
- copied visual inspect values;
- exported assets;
- dimensions, typography, colors, spacing, states, and written notes;
- existing project code and project overlays.

Unsupported inputs by themselves:

- Figma URL;
- file key;
- node id;
- Figma whiteboard reference.

When only unsupported input is provided, Codex must ask for screenshots,
exports, copied inspect values, assets, or a written brief.

## Skills

### `goal-planner`

Use this skill for standard or deep frontend work that needs a clear user goal,
scope, constraints, and done criteria before implementation. It must not run for
micro-fixes, obvious type errors, tiny styling changes, isolated component
edits, or direct file-scope changes unless the task escalates.

### `execution-plan-manager`

Use this skill after the goal is defined for standard or deep frontend work that
needs task slices, context budget, checkpoint rules, or stop/resume state. It
must not run for lightweight micro-fixes or isolated direct edits unless the task
escalates.

### `design-screenshot-spec`

Use this skill to create the implementation artifact. It outputs a structured
`Design Implementation Spec` with source inventory, layout, typography, color,
spacing, assets, states, responsive behavior, accessibility notes, acceptance
criteria, confidence, and unknowns.

### `frontend-layout-implementer`

Use this skill to implement the spec in the current frontend project. It is
framework-agnostic and must inspect the project before choosing patterns. It
supports React, Next.js, Vite, static HTML/CSS, Vue, Svelte, or another
frontend stack by following actual project conventions.

It uses these tools when available:

- Project Context MCP;
- Design Spec MCP;
- Visual Reference MCP;
- `context7`;
- MDN MCP;
- Browser or Playwright MCP;
- Visual Diff MCP.

If a named MCP is unavailable, Codex must report the missing capability before
using a lower-confidence fallback. Figma MCP is never a fallback.
Using available Browser or Playwright MCP for rendered UI verification does not
require separate user confirmation. Installing missing MCP servers, package
installs, commands that require approval, destructive actions, and production
access still require the approvals defined by the active environment.

### `frontend-visual-qa`

Use this skill after implementation. It verifies local app rendering, console
and runtime errors, desktop/tablet/mobile viewport fit, screenshot capture,
visual comparison, responsive behavior, text overflow, and interaction states.
When Playwright MCP is available, the skill runs those rendered checks directly
instead of only proposing or handing off browser QA.

### `project-onboarding-adapter`

Use this skill to adapt the bundle to a host frontend project. It plans or
executes the host-root `AGENTS.md` pointer, detects the frontend stack, selects
official documentation and MCP capabilities, scans current skill MCP
dependencies, and writes local-only `project/**` overlays.

In Plan Mode it produces a plan only. Outside Plan Mode it may execute an
approved adaptation, but it must not create application source files. For a new
or empty project it creates or refreshes only the host-root pointer and
`.agents/project/**` overlays from inferred or user-provided intended stack
facts.

It installs missing MCP servers only after explicit user approval and only when
the official install source has been verified.

### `project-context-adapter`

Use this skill to refresh `project/**` overlays, docs/MCP choices, design
reference boundaries, patterns, anti-patterns, and frontend path indexes after
project facts change.

### `agent-rules-skill-author`

Use this skill to create, evaluate, or edit `.agents` skills, rules, metadata,
and graph links.

## Path Model

Paths inside this bundle are bundle-local:

```text
AGENTS.md
SUMMARY.md
README.md
common/**
skills/**
project/**
```

The host-root `AGENTS.md` lives outside the bundle and should be a pointer to
`.agents/AGENTS.md`. Only `project-onboarding-adapter` owns creating or
recreating that pointer.

`SUMMARY.md` is a manual catalog for humans. Agents must not read it for normal
prompt routing or required context unless the user explicitly asks to edit,
audit, or summarize it.

## Publishable And Local-Only

Publishable bundle paths:

```text
AGENTS.md
SUMMARY.md
README.md
common/**
skills/**
.gitignore
```

Local-only paths:

```text
project/**
.obsidian/**
generated, vendor, build, cache, and host-project source paths
```

Project context cache files include:

```text
project/stack-profile.md
project/architecture-map.md
project/styling-profile.md
project/verification-profile.md
project/approved-patterns.md
project/anti-patterns.md
project/mcp-profile.md
project/design-reference-profile.md
project/react/path-index.md
project/next/path-index.md
```

`project/mcp-profile.md` caches required, available, missing, optional,
approved, installed, skipped, or blocked MCP capabilities for the current
skills. `project/design-reference-profile.md` caches screenshot, exported
asset, copied inspect, and design-reference boundaries without implying live
design-tool access.

## Prohibited Workflows

- Do not use Figma MCP.
- Do not inspect live Figma files.
- Do not create or edit Figma files.
- Do not use Figma whiteboard.
- Do not generate Figma design systems or Code Connect mappings.
- Do not install missing MCP servers without explicit user approval and a
  verified official install source.
- Do not scaffold app source files during new-project onboarding.
- Do not implement before a design spec exists.
- Do not add packages, styling systems, global tokens, or architecture layers
  without explicit approval.
- Do not interact with production systems or production data.

## Skill Authoring Standard

Every remaining skill uses:

- `name` and `description` first in frontmatter;
- graph metadata after native trigger fields;
- `Purpose`;
- `When To Use`;
- `When Not To Use`;
- `Required Context`;
- `Tool Contract`;
- `Workflow`;
- `Output Contract`;
- `Validation Gates`;
- `Trigger Evals`;
- `Reference Map`;
- synchronized `agents/openai.yaml`.

## Validation

For skill changes, run:

```shell
python skills/agent-rules-skill-author/scripts/validate_agent_skill.py skills/<skill-name>
```

From the host repository root, the equivalent path is:

```shell
python .agents/skills/agent-rules-skill-author/scripts/validate_agent_skill.py .agents/skills/<skill-name>
```

Also search for stale removed skill names and prohibited Figma/Jam routing
before finishing.
