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
-> frontend-design-director when visual judgment is needed
-> frontend-architecture-planner when architecture boundaries matter
-> frontend-layout-implementer
-> frontend-linter-manager when code changed and lint is available
-> frontend-visual-qa
-> frontend-quality-reviewer when quality review is requested or appropriate
```

1. `design-screenshot-spec` reads supplied screenshots, inspect panels, assets,
   and notes, then produces a `Design Implementation Spec`.
2. `frontend-design-director` defines subject-grounded visual direction when the
   task needs redesign, polish, distinctive UI, or anti-template critique.
3. `frontend-layout-implementer` implements that spec or design direction in the
   current frontend project using project context and the actual stack.
4. `frontend-linter-manager` runs existing lint verification after code-changing
   work when a lint command exists.
5. `frontend-visual-qa` verifies the rendered UI with browser screenshots,
   viewport checks, console/runtime review, and visual diff review. When
   Playwright MCP is available, Codex runs those browser checks automatically
   after implementation without asking for separate confirmation.
6. `frontend-quality-reviewer` performs an evidence-backed quality pass when
   review is requested or appropriate.

For standard or deep work that needs goal clarity and task slicing before
implementation, use:

```text
goal-planner
-> execution-plan-manager
-> selected implementation or planning skill
```

Use `mcp-toolchain-manager` only when tool capability affects the current slice
or the user asks for MCP/tool setup, audit, validation, or troubleshooting.

Do not insert `goal-planner`, `execution-plan-manager`,
`mcp-toolchain-manager`, `frontend-design-director`,
`frontend-architecture-planner`, or `greenfield-project-builder` into
lightweight workflows unless the task escalates or the user directly asks for
that concern.

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

### `mcp-toolchain-manager`

Use this skill when frontend work needs MCP/tool capability detection,
missing-tool reporting, official install source verification, approval-gated
installation planning, or `project/mcp-profile.md` updates. It must not install
tools, run package installs, or change configs without explicit user approval.

### `frontend-design-director`

Use this skill for standard or deep UI work that needs subject-grounded visual
direction, redesign, visual polish, design critique, anti-template checks,
interface-copy stance, motion stance, or visual acceptance criteria before
implementation. It must not run for purely technical micro-fixes or isolated
code edits.

### `frontend-architecture-planner`

Use this skill for standard or deep frontend work that needs routing, state,
data, form, build, workspace, or component ownership decisions before
implementation. It follows local conventions first and does not install
packages, migrate frameworks, or create testing workflows by default.

### `greenfield-project-builder`

Use this skill for new or empty frontend projects. It defines the first vertical
slice, stack assumptions, approval gates, and onboarding handoff before any
scaffold or package installation.

### `frontend-bugfix-debugger`

Use this skill for evidence-first frontend bugfixes. It records the symptom,
reproduces or explains the reproduction blocker, fixes the smallest cause, and
verifies against the original behavior.

### `frontend-refactor-surgeon`

Use this skill for behavior-preserving frontend refactors. It defines the
behavior boundary first, keeps public contracts stable, and stops before
unapproved behavior changes.

### `frontend-quality-reviewer`

Use this skill for evidence-backed frontend quality review. It reports
`pass`, `pass with concerns`, or `fail`, uses `blocking`, `high`, `medium`,
`low`, `nit`, and `praise` labels, separates required fixes from optional
improvements, and does not trigger broad rewrites by itself.

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

## Design Intelligence Layer

The design layer includes:

```text
skills/frontend-design-director
common/design-quality-rubric.md
common/anti-template-defaults.md
common/interface-copy-rules.md
common/motion-rules.md
common/agent-operating-model.md
common/framework-adaptation-policy.md
common/typescript-discipline.md
templates/design-direction-contract.md
templates/visual-memory.md
```

It exists to prevent generic AI UI and to create a concrete design contract
before implementation when visual judgment is needed. It must not introduce UI
component libraries, testing workflows, animation libraries, or unapproved
packages.

## Path Model

Paths inside this bundle are bundle-local:

```text
AGENTS.md
SUMMARY.md
README.md
common/**
skills/**
templates/**
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
CHANGELOG.md
plugin.json
common/**
skills/**
templates/**
examples/**
scripts/**
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
project/visual-memory.md
project/react/path-index.md
project/next/path-index.md
project/docs-profile.md
project/build-profile.md
project/workspace-profile.md
project/state-management-profile.md
project/data-fetching-profile.md
```

`project/mcp-profile.md` caches required, available, missing, optional,
approved, installed, skipped, or blocked MCP capabilities for the current
skills. `project/design-reference-profile.md` caches screenshot, exported
asset, copied inspect, and design-reference boundaries without implying live
design-tool access. `project/visual-memory.md` is local-only and must be copied
from `templates/visual-memory.md` only when durable visual memory is useful.

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
- Do not add packages, styling systems, UI component libraries, animation
  libraries, global tokens, or architecture layers without explicit approval.
- Do not create testing workflows or testing skills.
- Do not interact with production systems or production data.

## Distribution

Build and validate generated targets from `.agents/`:

```shell
python scripts/validate_skill_pack.py
```

This creates:

```text
dist/codex/**
dist/claude/**
```

`dist/codex/**` includes Codex `agents/openai.yaml` metadata.
`dist/claude/**` omits Codex-only metadata and uses the local structural
compatibility checklist. Neither target includes local-only `project/**`.

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
