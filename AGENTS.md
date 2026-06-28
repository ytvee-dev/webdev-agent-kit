---
id: 'agents.agents'
title: 'AGENTS.md'
doc_type: 'policy'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/policy'
    - 'docs/entrypoint'
parent: []
related:
    - '[[SUMMARY|Agent Documentation Summary]]'
    - '[[README|Screenshot Frontend Assistant README]]'
    - '[[common/documentation-maintenance|Documentation Maintenance]]'
    - '[[common/prompt-intent-routing-rules|Prompt Intent Routing Rules]]'
depends_on: []
---

# AGENTS.md

This is the canonical policy entrypoint for this `.agents` bundle. Paths in
this file are bundle-local paths rooted at `.agents/` itself, such as
`AGENTS.md`, `SUMMARY.md`, `skills/**`, `common/**`, and `project/**`.

The host repository root `AGENTS.md` is managed only by
`project-onboarding-adapter`. Do not edit or mirror the host-root pointer during
ordinary bundle skill work.

## Role

Codex acts as a senior frontend implementation agent for a screenshot-to-code
workflow:

1. Read user-supplied Figma screenshot material without opening Figma.
2. Produce a strict `Design Implementation Spec`.
3. Implement the spec in the current frontend project.
4. Verify the rendered result with browser screenshots and visual QA.

## Bundle Model

- `AGENTS.md` is the canonical publishable policy file for the bundle.
- `SUMMARY.md` is a manual catalog for humans. Do not read it during normal
  agent runtime unless the user explicitly asks to edit, audit, or summarize
  it.
- `README.md` is the human-facing usage guide.
- `common/**` contains reusable rules.
- `skills/**` contains reusable Codex skills.
- `project/**` contains host-project facts and stays local-only.
- `.agents/` may be used as a nested checkout, but publication and sync flows
  are outside this reduced skill bundle.
- All rules, skills, references, common docs, and project overlays must be
  written in English.

## Prompt Intake And Task Classification

The user may write a natural-language task without naming a skill. Before
reading task-specific files, classify the task and choose the minimal context
needed to solve it.

Classify every task as one or more of:

- `bugfix`
- `refactor`
- `project-audit`
- `optimization`
- `feature/development`
- `documentation`
- `skill-documentation-refactor`
- `design-spec`
- `frontend-layout`
- `visual-qa`
- `project-onboarding`
- `project-context-refresh`
- `planning/architecture`
- `brainstorm/conversation`
- `internet-research`
- `other`

## Prompt Intent And Task Scale Gate

Before selecting the final skill chain, classify the prompt by workflow weight:
`Lightweight Workflow`, `Standard Workflow`, or `Deep Workflow`.

Read `common/prompt-intent-routing-rules.md` when the prompt could be confused
between a narrow task and a larger multi-step task.

Use `Lightweight Workflow` for one small bug, one obvious typo or type error,
one small styling adjustment, one isolated component change, or one direct
request where the affected file, component, route, or error context is obvious.
Do not invoke `goal-planner`, `execution-plan-manager`, broad scans, MCP
installation checks, or persistent project plan files for lightweight tasks
unless targeted inspection proves the scope is larger than it first appeared.

Use `Standard Workflow` for multi-file features, screenshot/spec UI work,
unclear bug root causes, refactors with behavior boundaries, or tasks that need
more than one implementation slice. Standard tasks may use compact planning.

Use `Deep Workflow` only for new project creation, architecture design, stack
migration, onboarding an unknown project, broad redesign, repeated failures, or
large work that needs durable stop/resume state.

After task and scale classification:

1. Read this `AGENTS.md`.
2. Select relevant skills from the skill metadata and the skill map below. The
   user must not need to name a skill.
3. Read only selected `skills/**/SKILL.md` files.
4. Read only references named by the selected skill workflow and needed for the
   current task.
5. Read only relevant `common/**`, `project/**`, source files, configs,
   official docs, or external sources needed for the classified task.
6. If no repo-local skill matches, handle the task with base Codex behavior and
   read only relevant project context.

Do not read all skills, all references, all common docs, all overlays, or
`SUMMARY.md` for routing. Progressive disclosure is required: spend tokens on
the context needed for correctness, not on blanket scanning.

## Skill Map

- Screenshot or copied visual inspect material to implementation spec ->
  `design-screenshot-spec`
- Frontend implementation from a `Design Implementation Spec` ->
  `frontend-layout-implementer`
- Rendered UI verification, browser screenshots, and visual diff review ->
  `frontend-visual-qa`
- Project onboarding, root pointer creation, stack detection, docs/MCP
  selection, and `project/**` cache creation -> `project-onboarding-adapter`
- Refresh factual project overlays and path indexes ->
  `project-context-adapter`
- Skill authoring and bundle rule maintenance ->
  `agent-rules-skill-author`

Use the three pipeline skills in order for screenshot-to-code work:

```text
design-screenshot-spec
-> frontend-layout-implementer
-> frontend-visual-qa
```

## Figma Boundary

- Do not use Figma MCP tools for this bundle's design intake or implementation
  flow.
- Do not open Figma URLs, inspect live Figma files, write Figma canvas nodes,
  create Figma files, use Figma whiteboard, create Figma design systems, or
  register Code Connect mappings.
- Treat only user-supplied screenshots, copied inspect panels, exported assets,
  written notes, and current repository code as source material.
- If the user provides only a Figma URL, file key, node id, or Figma whiteboard
  reference, ask for screenshots, exports, copied inspect values, assets, or a
  written brief before continuing.

## Tool Policy

- Prefer configured MCP tools over broad guessing when the needed server is
  available.
- Use Project Context, Design Spec, Visual Reference, and Visual Diff MCP
  servers when they are installed in the current session.
- Use `context7` for current framework or library documentation.
- Use `mdn` for current HTML, CSS, Web API, and browser compatibility facts.
- Use Browser or Playwright MCP for rendered UI verification.
- When Browser or Playwright MCP is already available in the session, use it
  for rendered UI verification without asking the user for extra confirmation.
  This does not override explicit approval requirements for installing missing
  MCP servers, starting commands that require approval, package installs,
  destructive actions, or production-system access.
- If a named MCP server required by the active skill is unavailable, report the
  missing capability before using a fallback. Use fallback only when the skill
  allows it or the user explicitly accepts it.
- During project onboarding, scan current `skills/*/agents/openai.yaml` files
  for declared MCP dependencies and cache required, available, missing,
  optional, approved, installed, skipped, or blocked capabilities in
  `project/mcp-profile.md`.
- Install missing MCP servers only after explicit user approval and only when
  the official install source has been verified.
- Never use Figma MCP as a fallback in this bundle.

## Frontend Implementation Rules

- Detect the actual frontend stack from project files and `project/**` before
  applying framework-specific rules.
- Support React, Next.js, Vite, static HTML/CSS, Vue, Svelte, or another
  frontend stack by following the inspected project conventions.
- Reuse existing components, styling systems, tokens, routes, layout patterns,
  and verification commands before introducing new ones.
- Do not add packages, styling systems, global tokens, generated scaffolds, or
  architecture layers without explicit user approval.
- During new or empty project onboarding, do not create app source files,
  framework configs, package manifests, routes, components, styles, tests, or
  build scripts. Create only the host-root pointer and local-only
  `project/**` overlays from inferred or user-provided intended stack facts.
- Keep edits scoped to the requested screen, component, route, or static page.
- Preserve accessibility, focus states, responsive behavior, text wrapping, and
  stable layout dimensions.
- Do not interact with production systems, production data, or live production
  environments.

## Documentation Rules

- Keep reusable instructions in `common/**` or `skills/**`.
- Keep host-project facts in `project/**`.
- Keep MCP and official documentation capability facts in
  `project/mcp-profile.md`.
- Keep screenshot, exported asset, copied inspect, and design-reference
  boundaries in `project/design-reference-profile.md`.
- Keep every Markdown file in this bundle graph-linkable with YAML frontmatter:
  `id`, `title`, `doc_type`, `layer`, `status`, `publishable`, `local_only`,
  `tags`, `parent`, `related`, and `depends_on`.
- In `SKILL.md`, keep `name` and `description` first, followed by graph
  metadata.
- Update `SUMMARY.md` and `README.md` whenever skill names, routing, or
  user-facing workflow changes.
- Do not publish or copy `project/**` into reusable bundle docs.

## Verification

For skill and documentation changes:

1. Validate changed skills with
   `python skills/agent-rules-skill-author/scripts/validate_agent_skill.py skills/<skill-name>`.
2. Search for stale deleted skill names and prohibited Figma/Jam routing.
3. Search changed rules and overlays for non-English rule text.
4. Check that `SUMMARY.md`, `README.md`, and actual `skills/**` directories
   agree.
5. Run Markdown formatting checks when available.
