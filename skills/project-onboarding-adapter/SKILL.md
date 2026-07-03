---
name: project-onboarding-adapter
description: Use when adapting this .agents bundle to a host React or Next.js project, or when creating limited local-only overlays for a non-target frontend project so framework-agnostic skills can still route correctly. Includes host-root AGENTS.md pointer planning, project overlays, target-stack detection, skill applicability notes, docs/MCP selection, MCP dependency audit, verification facts, optional loop-memory setup, and frontend context cache.
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
parent: []
related:
    - '[[skills/project-onboarding-adapter/references/adaptation-checklist|Adaptation Checklist]]'
    - '[[skills/project-onboarding-adapter/references/path-audit-checklist|Path Audit Checklist]]'
    - '[[common/target-stack-policy|Target Stack Policy]]'
    - '[[common/skill-applicability-policy|Skill Applicability Policy]]'
    - '[[common/context-compaction-rules|Context Compaction Rules]]'
    - '[[skills/project-context-adapter/SKILL|Project Context Adapter]]'
    - '[[skills/mcp-toolchain-manager/SKILL|MCP Toolchain Manager]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Project Onboarding Adapter

## Purpose

Adapt this `.agents` bundle to a host frontend project without creating application source files. For React or Next.js, cache normal target-stack facts. For a non-target frontend project, cache only the detected stack boundary and the framework-agnostic skills that remain usable.

Onboarding may prepare local-only loop memory files when the user wants resumable iterative work, but it must not create app source files or reusable project facts in publishable docs.

## Natural Language Trigger Aliases

Route adaptation, initialization, and project-context bootstrap commands to this skill, including `адаптируйся`, `инициализируй .agents`, and `Adapt this .agents bundle to my project.`

## When To Use

- The user asks to adapt this bundle to a new React or Next.js project.
- The user asks to adapt this bundle to a non-target frontend project while keeping applicable design, QA, review, lint, planning, MCP, context, and skill-authoring workflows.
- The user asks to create or refresh the host-root pointer, local project overlays, MCP profile, design-reference profile, verification facts, loop memory, or path indexes.

## When Not To Use

- Ordinary screenshot-to-code implementation.
- Narrow project overlay refresh after implementation.
- Reusable skill authoring.
- Application scaffolding, package installation, or source file creation.
- Stack-specific React/Next architecture or implementation guidance for a non-target frontend project unless the user explicitly changes the supported stack.

## Required Context

1. Read the host-root `AGENTS.md` if present.
2. Read bundle-local `AGENTS.md`.
3. Read `common/target-stack-policy.md`.
4. Read `common/skill-applicability-policy.md` when the detected or suspected stack is outside the target stack.
5. Read `common/context-compaction-rules.md` when loop memory or resumable workflow setup is requested.
6. Read existing `project/**` overlays when present.
7. Inspect only relevant manifests, configs, source entrypoints, routes, styles, assets, and verification scripts.
8. Read current `skills/*/agents/openai.yaml` files for MCP dependency scan.

## Tool Contract

- Use Project Context MCP when available; otherwise use targeted filesystem reads.
- Use MDN for HTML, CSS, Web APIs, accessibility, and browser behavior.
- Use `context7` only for detected target-stack libraries or tooling.
- Determine Browser or Playwright availability from the current session tool registry or configured capability facts. Do not invoke either tool during onboarding or MCP detection.
- Do not use Figma MCP.
- Missing MCP installation requires explicit user approval after reporting the official source.

## Workflow

1. Classify whether this is Plan Mode or approved execution.
2. Detect whether the host project is existing, new/empty, or partially initialized.
3. Detect target-stack fit from manifests, configs, lockfiles, source roots, routes, styles, and entrypoints.
4. If the project fits the target stack, plan or write normal `project/**` overlays for stack, architecture, styling, state, data, verification, design references, MCP profile, and path indexes.
5. If the user asks for resumable iterative work or loop memory, plan or write local-only `project/loop-memory.md` using `templates/loop-memory.md` as the source pattern.
6. If the project is outside the target stack, continue with limited onboarding: record the stack boundary, skip React/Next path indexes and stack-specific patterns, and write `project/skill-applicability-profile.md` with applicable framework-agnostic skills from `common/skill-applicability-policy.md`.
7. Scan `skills/*/agents/openai.yaml` for declared MCP dependencies and cache required, available, missing, optional, approved, installed, skipped, or blocked capabilities in `project/mcp-profile.md`.
8. In Plan Mode, return the plan and stop.
9. In approved execution mode, create or update only the approved pointer and local-only overlays, then run available validation checks.

## Output Contract

```text
Host-root pointer action
Project type and stack facts
Target-stack fit
Applicable framework-agnostic skills when outside target stack
Docs and MCP choices
Overlays to create or update
Loop memory setup
Verification commands
Validation run or blocked
Unknowns
```

## Validation Gates

- `project/**` overlays remain local-only.
- Loop memory stores tried, verified, and open facts only in local-only project files.
- Non-target frontend overlays do not claim React/Next implementation support.
- Non-target frontend projects list applicable framework-agnostic skills instead of reporting the whole bundle unusable.
- No application source files are created during onboarding.
- No package, MCP, UI library, styling system, or framework change is made without explicit approval.
- Changed Markdown keeps graph frontmatter and English reusable rules.

## Trigger Evals

Should trigger:

- "адаптируйся"
- "Adapt this .agents bundle to my project."
- "Plan onboarding for this frontend repo."
- "Adapt this bundle to an Astro project but keep only the skills that still apply."
- "Set up local loop memory for this project."

Should not trigger:

- "Implement this visual spec."
- "Refresh project overlays after this component change."
- "Create a new skill package."
- "Scaffold a new React app."

## Reference Map

- `common/target-stack-policy.md`
- `common/skill-applicability-policy.md`
- `common/context-compaction-rules.md`
- `templates/loop-memory.md`
- `skills/project-context-adapter/SKILL.md`
- `skills/mcp-toolchain-manager/SKILL.md`
