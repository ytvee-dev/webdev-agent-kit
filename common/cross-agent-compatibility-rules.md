---
id: 'agents.common.cross-agent-compatibility-rules'
title: 'Cross-Agent Compatibility Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'packaging/compatibility'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/portable-skill-core-contract|Portable Skill Core Contract]]'
depends_on: []
---

# Cross-Agent Compatibility Rules

Purpose: keep the source bundle compatible with generated Codex and Claude
distribution targets while documenting what is portable across other coding-agent
hosts.

## Target Strategy

Use source plus generated targets:

```text
.agents/skills/**        source of truth
.agents/dist/codex/**    Codex package target
.agents/dist/claude/**   Claude package target
```

The source bundle has two distinct manifests:

- `bundle-manifest.json` is the internal inventory used to keep source skills,
  documentation, and validators synchronized;
- `.codex-plugin/plugin.json` is the native Codex plugin entrypoint and is
  included only in the Codex target.

## Host Compatibility Matrix

| Host | Supported artifact | Compatibility status | Notes |
| --- | --- | --- | --- |
| Source bundle | `AGENTS.md`, `common/**`, `skills/**`, `templates/**`, `examples/**`, validators, schemas, and evals | Canonical | Use this layer for authoring, validation, review, and release builds. Do not treat generated `dist/**` as source. |
| Codex | `dist/codex/**` plus `.codex-plugin/plugin.json` and `skills/*/agents/openai.yaml` | First-class generated target | Keep Codex-only plugin and UI metadata out of source portability assumptions and out of the Claude target. |
| Claude Skills | `dist/claude/**` with portable `SKILL.md`, references, scripts, assets, common rules, templates, and examples | Structural target | Validate locally until a stricter Claude package validator is adopted. Do not ship Codex-only `agents/openai.yaml` or `.codex-plugin`. |
| GitHub Copilot | Human-selected repository/custom-instruction adaptation | Advisory compatibility | Reuse source policies manually where applicable. Do not assume native skill-package semantics, graph metadata, or Codex plugin metadata. |
| Cursor | Human-selected rules adaptation | Advisory compatibility | Reuse concise rules and workflow fragments manually. Do not rely on this bundle's manifests or generated targets as Cursor-native packages. |
| Windsurf | Human-selected rules adaptation | Advisory compatibility | Reuse concise rules and workflow fragments manually. Do not rely on this bundle's manifests or generated targets as Windsurf-native packages. |
| Generic coding agents | `AGENTS.md` plus selected `common/**` and `skills/**/SKILL.md` procedures | Partial | Apply only the workflow text that matches the host's instruction model and available tools. Keep approval gates and local-only boundaries intact. |

## Portability Rules

- Treat `AGENTS.md`, `common/**`, `skills/**`, `templates/**`, `examples/**`,
  schemas, validators, and evals as the publishable source model.
- Treat `README.md` as human-facing only. Do not use it as agent runtime,
  routing, validation, inventory, or compatibility source material.
- Treat `project/**` as host-project local overlay state. Never publish it in
  reusable source docs or distribution targets.
- Treat `bundle-manifest.json` as internal inventory. Do not package it as a
  host-native runtime manifest.
- Treat `.codex-plugin/plugin.json` and `skills/*/agents/openai.yaml` as
  Codex-specific metadata.
- Treat generated `dist/**` as release output. Rebuild it from source rather than
  editing it directly.
- Treat host-specific rules for Copilot, Cursor, Windsurf, and generic agents as
  adaptations, not first-class package outputs, until dedicated validators and
  release artifacts exist.

## Rules

- Keep rich `.agents` graph metadata in source files.
- Generate portable `SKILL.md` frontmatter for distribution targets.
- Include `agents/openai.yaml` only in the Codex target.
- Include `.codex-plugin/plugin.json` only in the Codex target; do not expose
  the internal `bundle-manifest.json` as a platform manifest.
- Keep the Claude target free of Codex-only plugin and UI metadata.
- Do not include `project/**`, local-only overlays, host-project facts, build
  output, vendor files, caches, or dependency internals in distribution targets.
- Do not package UI component library skills or testing skills.
- Record Claude compatibility as validated by the local structural checklist
  until a stricter Claude package validator is adopted.
