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

Purpose: keep the WebDev Agent Kit bundle internally consistent.

## Required Context

Before changing bundle docs or skills:

1. Read `AGENTS.md`.
2. Read this file.
3. Read `skills/agent-rules-skill-author/SKILL.md`.
4. Read the affected docs, skills, references, and project overlays.

## Layer Rules

- Put reusable policy in `common/**`.
- Put reusable workflows in `skills/**`.
- Put host-project facts in `project/**`.
- Keep `project/**` local-only.
- Keep the host-root `AGENTS.md` pointer out of ordinary bundle edits.
- Use bundle-local paths inside `AGENTS.md`, `README.md`, `common/**`, and
  `skills/**`.
- Keep all rules, skills, references, common docs, and project overlays written
  in English.
- Keep MCP capability and official documentation facts in
  `project/mcp-profile.md`.
- Keep screenshot, exported asset, copied inspect, and design-reference
  boundaries in `project/design-reference-profile.md`.

## Markdown Rules

- Every Markdown file in this bundle must keep graph frontmatter current.
- In `SKILL.md`, keep `name` and `description` first.
- Treat graph frontmatter as navigation metadata only.
- Keep binding workflow instructions in the document body.
- Update `README.md`, manifests, and owning graph links when skill names,
  workflow, routing, or user-facing setup changes.

## Skill Package Rules

- Keep skill packages limited to `SKILL.md`, `agents/openai.yaml`, and needed
  `references/**`, `scripts/**`, or `assets/**`.
- Do not add auxiliary `README.md`, `CHANGELOG.md`, or quick-reference files
  inside skill packages.
- Keep references linked from the owning `SKILL.md`.
- Keep `agents/openai.yaml` aligned with the trigger, scope, and tool contract.
- Do not declare Figma MCP dependencies in this bundle.
- When onboarding or context refresh changes MCP dependencies, scan current
  `skills/*/agents/openai.yaml` files and update `project/mcp-profile.md`.

## Validation

Before finishing documentation or skill changes:

1. Validate each changed skill package.
2. Search for stale removed skill names and prohibited Figma/Jam routing.
3. Search changed docs and overlays for non-English rule text.
4. Verify actual `skills/**` directories match `bundle-manifest.json`,
   `.codex-plugin/plugin.json`, and `README.md`.
5. Run Markdown formatting checks when available.
