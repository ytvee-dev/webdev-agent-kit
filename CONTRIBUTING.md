---
id: 'agents.contributing'
title: 'Contributing To WebDev Agent Kit'
doc_type: 'contribution-guide'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/contributing'
    - 'governance'
parent: []
related:
    - '[[AGENTS|Canonical Agent Policy]]'
    - '[[CHANGELOG|WebDev Agent Kit Changelog]]'
depends_on: []
---

# Contributing

WebDev Agent Kit is a reusable source bundle for coding-agent workflows. Contributions must keep the bundle portable, progressively disclosed, and safe to install into a host project.

## Contribution Principles

- Keep reusable policy in `common/**` and task-specific procedures in `skills/**`.
- Keep host-project facts in local-only `project/**` overlays. Do not publish current project state in reusable bundle files.
- Prefer precise workflow instructions over broad slogans such as "follow best practices".
- Treat skill `description` fields as routing triggers. Include what the skill does, when to use it, and important non-use boundaries.
- Keep `SKILL.md` files compact. Move durable details into `references/**`, deterministic helpers into `scripts/**`, and templates or sample artifacts into `assets/**`.
- Keep `README.md` human-maintained. Do not use it as an agent source, routing source, or validation source.
- Do not add dependencies, supported stacks, MCP tools, or generated scaffolds without an explicit policy and validation update.

## Required Checks Before A Pull Request

Run the full structural validation:

```bash
python scripts/validate_skill_pack.py
```

For a changed skill, also run the skill-level validator:

```bash
python skills/agent-rules-skill-author/scripts/validate_agent_skill.py skills/<skill-name>
```

If validation cannot run because the environment is incomplete, state the blocker in the pull request and include the exact command that was attempted.

## Pull Request Checklist

A pull request that changes rules or skills should include:

- the user-facing problem or agent failure mode being fixed;
- the changed files and the layer they belong to;
- trigger examples that should use the skill;
- near-miss examples that should not use the skill;
- validation commands run and their results;
- any new portability, security, or host-agent compatibility risks;
- a `CHANGELOG.md` entry for behavior, packaging, validation, or security changes.

## Adding Or Changing A Skill

Every skill package must keep the following files aligned:

```text
skills/<skill-name>/
├── SKILL.md
└── agents/openai.yaml
```

Use `references/**`, `scripts/**`, and `assets/**` only when they reduce repeated context or make execution more deterministic. Do not add resource directories as decoration.

A skill is ready for review only when:

- `name` matches the directory name;
- `description` is specific enough for routing;
- all required sections are present;
- referenced resource paths exist;
- `agents/openai.yaml` has a useful interface and valid policy fields;
- trigger and negative-trigger examples are documented in the skill;
- the manifest is updated when the published skill inventory changes;
- proposed human-facing README text is supplied separately when public docs need an update.

## Review Severity

Use this severity model for review comments:

- `blocking`: breaks validation, packaging, routing, safety, or source-bundle installation;
- `high`: creates likely false routing, broad context loading, undocumented behavior change, or portability drift;
- `medium`: hurts maintainability, discoverability, or future extension;
- `low`: improves wording, formatting, or local clarity without changing behavior.
