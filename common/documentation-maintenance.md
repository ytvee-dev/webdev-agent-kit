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
    - '[[common/readme-policy|README Read And Edit Policy]]'
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
5. Read `README.md` only when the request concerns README, setup or run guidance, project intent, onboarding, audit, or documentation drift; apply `common/readme-policy.md`.

## Layer Rules

- Put reusable policy in `common/**`.
- Put reusable workflows in `skills/**`.
- Put host-project facts in `project/**`.
- Keep `project/**` local-only.
- Keep the host-root `AGENTS.md` pointer out of ordinary bundle edits.
- Use bundle-local paths inside `AGENTS.md`, `common/**`, and `skills/**`.
- Keep `README.md` in the user-facing documentation layer. It may locate claims but is not routing input, runtime policy, validator truth, or sufficient technical evidence.
- Keep all rules, skills, references, common docs, and project overlays written in English.
- Keep MCP capability and official documentation facts in `project/mcp-profile.md`.
- Keep screenshot, exported asset, copied inspect, and design-reference boundaries in `project/design-reference-profile.md`.

## Markdown Rules

- Every source Markdown file in this bundle must keep graph frontmatter current.
- In `SKILL.md`, keep `name` and `description` first.
- Treat graph frontmatter as navigation metadata only.
- Strip graph navigation metadata from every generated runtime target; keep only
  portable `name` and `description` frontmatter on generated skills.
- Keep binding workflow instructions in the document body.
- Update manifests and owning graph links when skill names, workflow, routing, or publishable source structure changes.
- Update an existing `README.md` only when the current user explicitly requests that README change, verify technical claims against higher evidence, and keep the edit separate from runtime policy changes.

## Skill Package Rules

- Keep skill packages limited to `SKILL.md`, `agents/openai.yaml`, and needed `references/**`, `scripts/**`, or `assets/**`.
- Do not add auxiliary `README.md`, `CHANGELOG.md`, or quick-reference files inside skill packages.
- Keep references linked from the owning `SKILL.md`.
- Keep `agents/openai.yaml` aligned with Codex UI and invocation policy. Keep
  cross-client capability requirements in `tool-capabilities-manifest.json`.
- Do not declare Figma MCP dependencies in this bundle.
- When onboarding or context refresh changes capability facts, read
  `tool-capabilities-manifest.json` and update `project/mcp-profile.md` from
  current-registry or validated-profile evidence.

## Validation

Before finishing documentation or skill changes:

1. Validate each changed skill package.
2. Search for stale removed skill names and prohibited Figma/Jam routing.
3. Search changed docs and overlays for non-English rule text.
4. Verify actual `skills/**` directories match `bundle-manifest.json` and `.codex-plugin/plugin.json`.
5. Run Markdown formatting checks when available.
6. If the request explicitly changed README, report it as human-facing documentation work and name the higher evidence used for technical claims.
