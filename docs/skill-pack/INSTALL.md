---
id: 'agents.docs.skill-pack.install'
title: 'Skill Pack Installation'
doc_type: 'install-guide'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/install'
    - 'docs/skill-pack'
parent:
    - '[[README|Screenshot Frontend Assistant README]]'
related:
    - '[[common/cross-agent-compatibility-rules|Cross-Agent Compatibility Rules]]'
depends_on: []
---

---
id: 'agents.docs.skill-pack.install'
title: 'Skill Pack Installation'
doc_type: 'install-guide'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/install'
    - 'docs/skill-pack'
parent:
    - '[[README|Screenshot Frontend Assistant README]]'
related:
    - '[[common/cross-agent-compatibility-rules|Cross-Agent Compatibility Rules]]'
depends_on: []
---

# Installation

Status: human-facing installation note. This file is not runtime context.

## Full Pack

Copy the publishable bundle into a project as `.agents/`, then keep the host
root `AGENTS.md` as a pointer to `.agents/AGENTS.md`.

Publishable source paths:

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
```

Do not copy local-only `project/**` facts into another repository.

## Build Targets

From `.agents/`:

```shell
python scripts/build_skill_targets.py
python scripts/validate_codex_skill_pack.py
python scripts/validate_claude_skill_pack.py
```

`dist/codex/**` includes Codex `agents/openai.yaml` metadata.

`dist/claude/**` includes portable `SKILL.md` packages without Codex-only
`agents/openai.yaml` metadata.

## One Skill

Copy one `skills/<skill-name>` package plus any referenced `common/**` docs and
templates it needs. Preserve `name` and `description` in `SKILL.md`.
