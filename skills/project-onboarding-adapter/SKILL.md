---
name: project-onboarding-adapter
description: Use when adapting this .agents bundle to a host frontend project with native client pointers, local-only project overlays, target-stack detection, skill applicability notes, docs/MCP capability selection, client profile creation, verification facts, optional loop-memory setup, and frontend context cache. Do not create app source files or overwrite host instructions without approval.
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
    - '[[common/core/runtime-core-policy|Portable Runtime Core Policy]]'
    - '[[common/readme-policy|README Read And Edit Policy]]'
    - '[[profiles/react-typescript/PROFILE|React TypeScript Profile]]'
    - '[[skills/project-onboarding-adapter/references/adaptation-checklist|Adaptation Checklist]]'
    - '[[skills/project-onboarding-adapter/references/path-audit-checklist|Path Audit Checklist]]'
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
    - '[[common/tool-capability-model|Tool Capability Model]]'
    - '[[common/mcp-installation-policy|MCP Installation Policy]]'
    - '[[common/target-stack-policy|Target Stack Policy]]'
    - '[[common/skill-applicability-policy|Skill Applicability Policy]]'
    - '[[common/context-compaction-rules|Context Compaction Rules]]'
    - '[[templates/project/client-profile|Client Profile Template]]'
    - '[[templates/project/mcp-profile|MCP Profile Template]]'
    - '[[skills/project-context-adapter/SKILL|Project Context Adapter]]'
    - '[[skills/mcp-toolchain-manager/SKILL|MCP Toolchain Manager]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Project Onboarding Adapter

## Purpose

Adapt this `.agents` bundle to a host frontend project without creating application source files. For React or Next.js, cache normal target-stack facts. For a non-target frontend project, cache only the detected stack boundary and the framework-agnostic skills that remain usable.

Onboarding must also adapt natively to the installed client target. It creates or refreshes the smallest appropriate host pointer, records client facts in local-only `project/client-profile.md`, and records tool capabilities in local-only `project/mcp-profile.md`.

## Natural Language Trigger Aliases

Route adaptation, initialization, and project-context bootstrap commands to this skill, including `адаптируйся`, `инициализируй .agents`, and `Adapt this .agents bundle to my project.`

## When To Use

- The user asks to adapt this bundle to a new React or Next.js project.
- The user asks to adapt this bundle to a non-target frontend project while keeping applicable design, QA, review, lint, planning, MCP, context, and skill-authoring workflows.
- The user asks to create or refresh the host-root pointer, native client pointer, local project overlays, MCP profile, client profile, design-reference profile, verification facts, loop memory, or path indexes.

## When Not To Use

- Ordinary screenshot-to-code implementation.
- Narrow project overlay refresh after implementation.
- Reusable skill authoring.
- Application scaffolding, package installation, or source file creation.
- Stack-specific React/Next architecture or implementation guidance for a non-target frontend project unless the user explicitly changes the supported stack.

## Required Context

1. Read the host-root native instruction pointer if present and needed for adaptation: `AGENTS.md`, `CLAUDE.md`, or client rules. Inspect only the minimal pointer section.
2. Read bundle-local `AGENTS.md` and `common/core/runtime-core-policy.md`.
3. Read `common/client-adaptation-policy.md` and only the adapter for the resolved canonical target.
4. Read `profiles/react-typescript/PROFILE.md` and its owning policies only when repository evidence confirms the profile.
5. Read `common/skill-applicability-policy.md` when the detected or suspected stack is outside the target stack.
6. Read `common/tool-capability-model.md` and `tool-capabilities-manifest.json` for capability selection.
7. Read `common/context-compaction-rules.md` when loop memory or resumable workflow setup is requested.
8. Read existing `project/**` overlays when present.
9. Inspect only relevant manifests, configs, source entrypoints, routes, styles, assets, and verification scripts.
10. Read `templates/project/client-profile.md` and `templates/project/mcp-profile.md` before creating those local-only profiles.

Read targeted README sections only when they help identify project intent, setup guidance, or documentation drift. Apply `common/readme-policy.md`, and confirm every cached technical fact through manifests, config, source, CI, package scripts, lockfiles, or real results.

## Tool Contract

- Use the `project_files` capability when available. Prefer configured filesystem/project-files MCP for direct project file reads; use host-native file tools when available; use targeted shell reads only as the fallback.
- Use MDN for HTML, CSS, Web APIs, accessibility, and browser behavior when official web platform facts matter.
- Use `context7` only for detected target-stack libraries or tooling when current docs matter.
- Determine Browser or Playwright availability from the current session tool registry or validated `project/mcp-profile.md` facts. Do not invoke either tool during onboarding or MCP detection.
- Do not infer MCP availability from `package.json`, lockfiles, `node_modules`, a running local app, or Playwright dependencies.
- Do not use Figma MCP.
- Missing MCP installation requires explicit user approval after reporting the official source.

## Workflow

1. Classify whether this is Plan Mode or approved execution.
2. Detect the installed target or current client surface. In source, resolve aliases through `bundle-manifest.json`; in a generated target, use its sole shipped adapter.
3. Read that one client adapter and apply its native discovery, pointer, tool, sandbox, and configuration rules. For a generic or unknown client, create no pointer unless the user explicitly requests one.
4. If an expected pointer already exists, do not overwrite it. Propose a merge when existing instructions are non-empty or ambiguous.
5. Detect whether the host project is existing, new/empty, or partially initialized.
6. Detect target-stack fit from manifests, configs, lockfiles, source roots, routes, styles, and entrypoints.
7. If the project fits the target stack, plan or write normal `project/**` overlays for stack, architecture, styling, state, data, verification, design references, MCP profile, client profile, and path indexes.
8. If the user asks for resumable iterative work or loop memory, plan or write local-only `project/loop-memory.md` using `templates/loop-memory.md` as the source pattern.
9. If the project is outside the target stack, continue with limited onboarding: record the stack boundary, skip React/Next path indexes and stack-specific patterns, and write `project/skill-applicability-profile.md` with applicable framework-agnostic skills from `common/skill-applicability-policy.md`.
10. Read `tool-capabilities-manifest.json` for declared capability needs and cache required, available, missing, optional, approved, installed, skipped, or blocked capabilities in `project/mcp-profile.md`.
11. Cache detected client target, native pointer, skill support, and MCP config locations in `project/client-profile.md`.
12. In Plan Mode, return the plan and stop.
13. In approved execution mode, create or update only the approved pointer and local-only overlays, then run available validation checks.

## Output Contract

```text
Installed package target or detected client
Native pointer action
Project type and stack facts
Target-stack fit
Applicable framework-agnostic skills when outside target stack
Docs and MCP capability choices
Client profile action
MCP profile action
Overlays to create or update
Loop memory setup
Verification commands
Validation run or blocked
Unknowns
```

## Validation Gates

- `project/**` overlays remain local-only.
- `project/client-profile.md` and `project/mcp-profile.md` are created from templates and marked local-only in copied overlays.
- Native pointers remain small. Claude uses the exact `@.agents/AGENTS.md` import when shared project policy is approved; other pointers reference `.agents/AGENTS.md` instead of mirroring the full policy.
- Existing host instructions are not overwritten without approval.
- README may supply targeted context but never the sole technical fact; README and host docs are not edited during onboarding unless the current user explicitly requests that documentation change.
- Loop memory stores tried, verified, and open facts only in local-only project files.
- Non-target frontend overlays do not claim React/Next implementation support.
- Non-target frontend projects list applicable framework-agnostic skills instead of reporting the whole bundle unusable.
- Capability detection uses `tool-capabilities-manifest.json` and does not depend on Codex-only `agents/openai.yaml` files.
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
- "Detect whether this install is Codex, Claude, Cursor, or VS Code and create the right pointer."

Should not trigger:

- "Implement this visual spec."
- "Refresh project overlays after this component change."
- "Create a new skill package."
- "Scaffold a new React app."

## Reference Map

- `common/client-adaptation-policy.md`
- `common/tool-capability-model.md`
- `common/mcp-installation-policy.md`
- `common/target-stack-policy.md`
- `common/skill-applicability-policy.md`
- `common/context-compaction-rules.md`
- `common/readme-policy.md`
- `tool-capabilities-manifest.json`
- `templates/project/client-profile.md`
- `templates/project/mcp-profile.md`
- `templates/loop-memory.md`
- `skills/project-context-adapter/SKILL.md`
- `skills/mcp-toolchain-manager/SKILL.md`
