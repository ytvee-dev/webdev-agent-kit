---
id: 'agents.common.documentation-maintenance'
title: 'Documentation Maintenance'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'docs/policy'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules Skill Author]]'
depends_on: []
---

# Documentation Maintenance

Purpose: keep the WebDev Agent Kit bundle internally consistent while keeping README content in the user-documentation layer.

## Required Context

Before changing bundle docs or skills:

1. Read `AGENTS.md`.
2. Read this file.
3. Read `skills/agent-rules-skill-author/SKILL.md`.
4. Read the affected `common/**`, `skills/**`, `project/**`, manifests, validators, templates, or examples for the requested change.
5. Exclude `README.md` from agent context gathering. It is user-facing documentation only.

## Layer Rules

- Put reusable policy in `common/**`.
- Put reusable workflows in `skills/**`.
- Put host-project facts in `project/**`.
- Keep `project/**` local-only.
- Keep the host-root `AGENTS.md` pointer out of ordinary bundle edits.
- Use bundle-local paths inside `AGENTS.md`, `common/**`, and `skills/**`.
- Keep `README.md` in the user-facing documentation layer. It is not routing input, runtime policy, verification input, or fallback context.
- Keep all rules, skills, references, common docs, and project overlays written in English.
- Keep MCP capability and official documentation facts in `project/mcp-profile.md`.
- Keep screenshot, exported asset, copied inspect, and design-reference boundaries in `project/design-reference-profile.md`.

## Markdown Rules

- Every Markdown file in this bundle must keep graph frontmatter current.
- In `SKILL.md`, keep `name` and `description` first.
- Treat graph frontmatter as navigation metadata only.
- Keep binding workflow instructions in the document body.
- Update manifests and owning graph links when skill names, workflow, routing, or publishable source structure changes.
- Update `README.md` only for explicit user-facing documentation work, and keep that work separate from runtime policy changes.

## Skill Package Rules

- Keep skill packages limited to `SKILL.md`, `agents/openai.yaml`, and needed `references/**`, `scripts/**`, or `assets/**`.
- Do not add auxiliary `README.md`, `CHANGELOG.md`, or quick-reference files inside skill packages.
- Keep references linked from the owning `SKILL.md`.
- Keep `agents/openai.yaml` aligned with the trigger, scope, and tool contract.
- Do not declare Figma MCP dependencies in this bundle.
- When onboarding or context refresh changes MCP dependencies, scan current `skills/*/agents/openai.yaml` files and update `project/mcp-profile.md`.

## Validation

Before finishing documentation or skill changes:

1. Validate each changed skill package.
2. Search for stale removed skill names and prohibited Figma/Jam routing.
3. Search changed docs and overlays for non-English rule text.
4. Verify actual `skills/**` directories match `bundle-manifest.json` and `.codex-plugin/plugin.json`.
5. Run Markdown formatting checks when available.
6. If the request explicitly changed README, report it as human-facing documentation work.
