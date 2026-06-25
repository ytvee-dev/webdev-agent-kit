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
    - '[[SUMMARY|Agent Documentation Summary]]'
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules Skill Author]]'
depends_on: []
---

# Documentation Maintenance

Purpose: keep the reduced screenshot-to-frontend bundle internally consistent.

## Required Context

Before changing bundle docs or skills:

1. Read `AGENTS.md`.
2. Read `SUMMARY.md`.
3. Read this file.
4. Read `skills/agent-rules-skill-author/SKILL.md`.
5. Read the affected docs, skills, references, and project overlays.

## Layer Rules

- Put reusable policy in `common/**`.
- Put reusable workflows in `skills/**`.
- Put host-project facts in `project/**`.
- Keep `project/**` local-only.
- Keep the host-root `AGENTS.md` pointer out of ordinary bundle edits.
- Use bundle-local paths inside `AGENTS.md`, `SUMMARY.md`, `README.md`,
  `common/**`, and `skills/**`.

## Markdown Rules

- Every Markdown file in this bundle must keep graph frontmatter current.
- In `SKILL.md`, keep `name` and `description` first.
- Treat graph frontmatter as navigation metadata only.
- Keep binding workflow instructions in the document body.
- Update `SUMMARY.md` and `README.md` when skill names, workflow, routing, or
  user-facing setup changes.

## Skill Package Rules

- Keep skill packages limited to `SKILL.md`, `agents/openai.yaml`, and needed
  `references/**`, `scripts/**`, or `assets/**`.
- Do not add auxiliary `README.md`, `CHANGELOG.md`, or quick-reference files
  inside skill packages.
- Keep references linked from the owning `SKILL.md`.
- Keep `agents/openai.yaml` aligned with the trigger, scope, and tool contract.
- Do not declare Figma MCP dependencies in this bundle.

## Validation

Before finishing documentation or skill changes:

1. Validate each changed skill package.
2. Search for stale removed skill names and prohibited Figma/Jam routing.
3. Verify actual `skills/**` directories match `SUMMARY.md` and `README.md`.
4. Run Markdown formatting checks when available.

