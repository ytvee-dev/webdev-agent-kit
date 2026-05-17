---
name: project-onboarding-adapter
description: Use when the user asks Codex to adapt to a new project, initialize or refresh Codex project context, connect `.agents`, create the host-root `AGENTS.md` pointer, or analyze the repository before writing `.agents/project/**`. Triggers include "адаптируйся", "адаптируй проект", "подключи .agents", "обнови контекст проекта", and "initialize Codex project context". This skill is Plan Mode only.
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
    - 'agents/skill'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/project-onboarding-adapter/references/adaptation-checklist|Adaptation Checklist]]'
    - '[[skills/project-onboarding-adapter/references/path-audit-checklist|Path Audit Checklist]]'
    - '[[skills/project-context-adapter/SKILL|Project Context Adapter]]'
    - '[[project/stack-profile|Stack Profile]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Project Onboarding Adapter

## Purpose

Plan the first-time adaptation of the shared `.agents` bundle to a host
project. Use this skill when the user wants Codex to learn the project,
prepare `.agents/project/**`, verify bundle paths, and ensure the host-root
`AGENTS.md` points to `.agents/AGENTS.md`.

This skill is only for Plan Mode. It plans adaptation; it does not mutate files
while Plan Mode is active.

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

## When To Use

Use for first-time or full-project onboarding prompts such as:

- `адаптируйся`
- `адаптируй этот проект под .agents`
- `подключи .agents`
- `проанализируй новый проект и запиши контекст для агента`
- `создай AGENTS.md pointer и обнови .agents/project`
- `initialize Codex project context`

Do not use for:

- normal React or Next.js feature, bugfix, refactor, or review work;
- narrow `.agents/project/**` refresh after code changes, where
  `project-context-adapter` is enough;
- reusable skill or policy authoring, where `agent-rules-skill-author` is the
  primary skill;
- sync-down, publish-up, branch, commit, push, or PR work, where
  `webdev-assistant-sync` is required.

## Plan Mode Workflow

When Plan Mode is active:

1. Read the root `AGENTS.md`, `.agents/AGENTS.md`, `.agents/SUMMARY.md`, and
   `.agents/README.md`.
2. Read `.agents/common/**`.
3. Read every `.agents/skills/*/SKILL.md`, every present
   `.agents/skills/*/agents/openai.yaml`, and only the referenced skill
   references needed for path and workflow validation.
4. Read existing `.agents/project/**` overlays.
5. Inspect the host project without generated, vendor, build, and cache
   directories such as `node_modules`, `.next`, `dist`, `coverage`, `.cache`,
   and `.playwright-mcp`.
6. Use `references/adaptation-checklist.md` to collect project facts.
7. Use `references/path-audit-checklist.md` to find missing, stale, or
   template-only paths in bundle docs and skill reference maps.
8. Produce a complete adaptation plan. Do not edit files in Plan Mode.

## Required Plan Contents

The adaptation plan must include:

- whether the host-root `AGENTS.md` exists and whether it should be created or
  replaced with the stable pointer to `.agents/AGENTS.md`;
- which `.agents/project/**` overlays should be created or updated;
- the discovered project type, stack, routing model, styling system, state
  layer, validation approach, and verification commands;
- concrete path indexes to write for React/client work and Next.js App Router
  work when those surfaces exist;
- path drift findings across `.agents/AGENTS.md`, `.agents/SUMMARY.md`,
  `.agents/README.md`, `.agents/common/**`, `.agents/skills/**`, and
  `.agents/project/**`;
- explicit exclusions for generated, vendor, build, cache, and local-only
  paths;
- verification commands to run after implementation;
- a statement that `.agents/project/**` stays local-only and host-project facts
  must not be written into publishable skills, common docs, or bundle policy.

## Implementation Defaults For The Future Execution Step

When the user later asks to execute the plan outside Plan Mode, the implementing
agent should:

- create or update only the host-root `AGENTS.md` pointer and
  `.agents/project/**` overlays unless the plan identifies stale publishable
  bundle links that must also be fixed;
- keep `.agents/AGENTS.md` canonical and never mirror it into the host-root
  `AGENTS.md`;
- write factual repo-specific context into `.agents/project/**`;
- keep reusable instructions in `.agents/common/**` and `.agents/skills/**`;
- avoid generated, vendor, build, cache, production, and secret-bearing paths;
- run the verification commands listed in the plan.

## Validation Gates

Before finishing the Plan Mode response, verify:

- the response is a plan only and contains no applied changes;
- root pointer handling is explicit;
- every expected `.agents/project/**` overlay is accounted for;
- path audit results distinguish real missing paths from documented templates;
- no host-project facts are planned for publishable bundle docs;
- the plan names relevant verification commands or states why none were found.

## Reference Map

- `references/adaptation-checklist.md`
- `references/path-audit-checklist.md`
