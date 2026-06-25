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
   viewport checks, console/runtime review, and visual diff review.

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

### `frontend-visual-qa`

Use this skill after implementation. It verifies local app rendering, console
and runtime errors, desktop/tablet/mobile viewport fit, screenshot capture,
visual comparison, responsive behavior, text overflow, and interaction states.

### `project-onboarding-adapter`

Use this Plan Mode skill to adapt the bundle to a host frontend project. It
plans the host-root `AGENTS.md` pointer and the local-only `project/**`
overlays. It does not edit files while Plan Mode is active.

### `project-context-adapter`

Use this skill to refresh `project/**` overlays and frontend path indexes after
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

## Prohibited Workflows

- Do not use Figma MCP.
- Do not inspect live Figma files.
- Do not create or edit Figma files.
- Do not use Figma whiteboard.
- Do not generate Figma design systems or Code Connect mappings.
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
