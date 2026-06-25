---
name: project-onboarding-adapter
description: Use in Plan Mode when adapting this .agents bundle to a host frontend project, creating or refreshing project overlays, and planning the host-root AGENTS.md pointer that references .agents/AGENTS.md. Produce a decision-complete onboarding plan only; do not edit files while Plan Mode is active.
id: 'agents.skills.project-onboarding-adapter.skill'
title: 'Project Onboarding Adapter'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'project-onboarding-adapter'
tags:
    - 'agents/skill-package'
    - 'agents/onboarding'
    - 'frontend/project-context'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/project-onboarding-adapter/references/adaptation-checklist|Adaptation Checklist]]'
    - '[[skills/project-onboarding-adapter/references/path-audit-checklist|Path Audit Checklist]]'
    - '[[skills/project-context-adapter/SKILL|Project Context Adapter]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Project Onboarding Adapter

## Purpose

Plan the first-time adaptation of this `.agents` bundle to a host frontend
project. This skill defines how a later execution step creates the host-root
`AGENTS.md` pointer and writes factual `project/**` overlays.

This skill is only for Plan Mode. It plans adaptation; it does not mutate files
while Plan Mode is active.

## When To Use

- The user asks to adapt this bundle to a new frontend project.
- The user asks to initialize or recreate project context.
- The user asks to create the host-root `AGENTS.md` pointer.

## When Not To Use

- Ordinary screenshot-to-code implementation. Use the three pipeline skills.
- Narrow `project/**` refresh after implementation. Use
  `project-context-adapter`.
- Skill authoring or bundle rule changes. Use `agent-rules-skill-author`.

## Required Context

1. Confirm active Plan Mode.
2. Read the host-root `AGENTS.md` if it exists.
3. Read bundle-local `AGENTS.md`, `SUMMARY.md`, and `README.md`.
4. Read `common/**`.
5. Read every current `skills/*/SKILL.md` and `skills/*/agents/openai.yaml`.
6. Read existing `project/**` overlays.
7. Inspect host project manifests, configs, source entrypoints, routes, styles,
   assets, tests, and verification scripts without generated/vendor/build/cache
   directories.
8. Read `references/adaptation-checklist.md`.
9. Read `references/path-audit-checklist.md`.

## Tool Contract

- Use Project Context MCP when available.
- Use filesystem reads and targeted search when MCP context is unavailable.
- Do not use Figma MCP.
- Do not mutate files while Plan Mode is active.

## Mode Gate

Before reading the whole project or changing any files, check the active
collaboration mode.

- If the active mode is not explicitly Plan Mode, stop immediately and answer
  exactly:

```text
Этот навык работает только в Plan Mode. Включите Plan Mode и повторите: "адаптируйся".
```

- If the mode is unclear, treat it as not Plan Mode and use the same response.
- Do not inspect the whole repository, create files, edit overlays, run
  adaptation commands, or produce a full adaptation plan outside Plan Mode.
- In Plan Mode, produce a decision-complete adaptation plan only. The user must
  request implementation separately after leaving Plan Mode.

## Workflow

When Plan Mode is active:

1. Read the host-root `AGENTS.md`, bundle-local `AGENTS.md`, `SUMMARY.md`, and
   `README.md`.
2. Read `common/**`.
3. Read every current `skills/*/SKILL.md`, every present
   `skills/*/agents/openai.yaml`, and only referenced skill references needed
   for path and workflow validation.
4. Read existing `project/**` overlays.
5. Inspect the host project without generated, vendor, build, and cache
   directories such as `node_modules`, `.next`, `dist`, `coverage`, `.cache`,
   and `.playwright-mcp`.
6. Use `references/adaptation-checklist.md` to collect project facts.
7. Use `references/path-audit-checklist.md` to find missing, stale, or
   template-only paths in bundle docs and skill reference maps.
8. Include graph frontmatter and Obsidian link updates for every planned
   `project/**` overlay and any publishable docs whose links drifted.
9. Produce a complete adaptation plan. Do not edit files in Plan Mode.

## Required Plan Contents

The adaptation plan must include:

- whether the host-root `AGENTS.md` exists and whether it should be created or
  replaced with the stable pointer to `.agents/AGENTS.md`;
- which `project/**` overlays should be created or updated;
- the discovered project type, stack, routing model, styling system, state
  layer, validation approach, and verification commands;
- concrete path indexes to write for React/client work and Next.js App Router
  work when those surfaces exist;
- path drift findings across bundle-local `AGENTS.md`, `SUMMARY.md`,
  `README.md`, `common/**`, `skills/**`, and `project/**`;
- graph frontmatter and wikilink updates needed after adaptation, including
  `publishable: false` and `local_only: true` for `project/**`;
- explicit exclusions for generated, vendor, build, cache, and local-only
  paths;
- verification commands to run after implementation;
- a statement that `project/**` stays local-only and host-project facts
  must not be written into publishable skills, common docs, or bundle policy.

## Implementation Defaults For The Future Execution Step

When the user later asks to execute the plan outside Plan Mode, the implementing
agent should:

- create or update only the host-root `AGENTS.md` pointer and `project/**`
  overlays unless the plan identifies stale publishable
  bundle links that must also be fixed;
- keep `.agents/AGENTS.md` canonical and never mirror it into the host-root
  `AGENTS.md`;
- write factual repo-specific context into `project/**`;
- create or update graph frontmatter and `.agents`-relative Obsidian wikilinks
  for every changed Markdown overlay;
- keep reusable instructions in `common/**` and `skills/**`;
- avoid generated, vendor, build, cache, production, and secret-bearing paths;
- run the verification commands listed in the plan.

## Validation Gates

Before finishing the Plan Mode response, verify:

- the response is a plan only and contains no applied changes;
- root pointer handling is explicit;
- every expected `project/**` overlay is accounted for;
- planned overlays include graph frontmatter and current links to relevant
  context skills;
- path audit results distinguish real missing paths from documented templates;
- no host-project facts are planned for publishable bundle docs;
- the plan names relevant verification commands or states why none were found.

## Output Contract

Return a plan containing:

- host-root `AGENTS.md` pointer action;
- project type and frontend stack facts;
- overlays to create or update;
- path indexes to create or update;
- stale bundle path findings;
- excluded paths;
- verification commands for the later execution step;
- confirmation that `project/**` remains local-only.

## Trigger Evals

Should trigger:

- "Adapt this .agents bundle to my project."
- "Initialize project context and create the root AGENTS.md pointer."
- "Plan onboarding for this frontend repo."

Should not trigger:

- "Implement this visual spec."
- "Refresh project overlays after this component change."
- "Create a new skill package."

## Reference Map

- `references/adaptation-checklist.md`
- `references/path-audit-checklist.md`
