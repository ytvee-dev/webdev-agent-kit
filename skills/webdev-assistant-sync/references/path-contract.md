---
id: 'agents.skills.webdev-assistant-sync.references.path-contract'
title: 'Path Contract'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'webdev-assistant-sync'
tags:
    - 'agents/skill-package'
    - 'agents/sync'
    - 'agents/reference'
parent:
    - '[[skills/webdev-assistant-sync/SKILL|Webdev Assistant Sync]]'
related:
    []
depends_on:
    - '[[skills/webdev-assistant-sync/SKILL|Webdev Assistant Sync]]'
---

# Path Contract

## Canonical paths

- Host project root: the repository where the agent is currently working
- Nested upstream checkout root: `.agents/`
- Canonical publishable AGENTS copy: `.agents/AGENTS.md`
- Host-root pointer: `AGENTS.md`
- Local host-project overlays: `.agents/project/**`
- Publishable bundle docs: `.agents/common/**`
- Publishable reusable workflows: `.agents/skills/**`

## Publishable checkout-root paths

- `AGENTS.md`
- `SUMMARY.md`
- `common/**`
- `skills/**`
- `README.md`
- `.gitignore`

## Local-only paths

- `project/**`
- old helper folders such as `upstream/**`
- any application source code, tests, configs, build outputs, and any other
  host-project files outside the nested `.agents/` repo surface

## Host-root pointer rule

- `.agents/AGENTS.md` is the canonical publishable policy file
- host-root `AGENTS.md` is a stable pointer to `.agents/AGENTS.md`, not a
  synchronized mirror
- changes inside `.agents/` do not require host-root `AGENTS.md` changes unless
  the canonical policy path changes
- `README.md` and `.gitignore` live only at `.agents/` checkout root and are
  not mirrored into the host repository root
