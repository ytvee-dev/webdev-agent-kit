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
    - '[[common/core/runtime-core-policy|Portable Runtime Core Policy]]'
    - '[[profiles/react-typescript/PROFILE|React TypeScript Profile]]'
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
    - '[[common/portable-skill-core-contract|Portable Skill Core Contract]]'
    - '[[docs/architecture/runtime-target-contracts|Runtime Target Contracts]]'
depends_on: []
---

# Cross-Agent Compatibility Rules

Purpose: keep the source bundle compatible with generated Codex and Claude
distribution targets while documenting what is portable across other coding-agent
hosts.

## Target Strategy

Use one portable source with three canonical runtime targets:

```text
common/core/**        compact portable behavior
profiles/**           evidence-gated project defaults
adapters/**           thin client differences
skills/**             portable procedures
dist/codex/**         Codex project bundle
dist/claude-code/**   Claude Code plugin
dist/cursor/**        Cursor project bundle
```

`docs/architecture/runtime-target-contracts.md` defines native entrypoints,
installation modes, skill roots, aliases, and validation ownership.

The source bundle has client and inventory manifests with separate purposes:

- `bundle-manifest.json` is the internal inventory used to keep source skills,
  target contracts, aliases, documentation, and validators synchronized;
- `.codex-plugin/plugin.json` is the native Codex plugin entrypoint and is
  included only in a Codex plugin target;
- `.claude-plugin/plugin.json` is the native Claude Code plugin entrypoint and
  is included only in the Claude Code plugin target.

`vs-code-codex`, `vs-code-claude`, and legacy `claude` are aliases. They must
reuse canonical target build and validation behavior rather than define new
runtime implementations.

## Host Compatibility Matrix

| Host | Supported artifact | Compatibility status | Notes |
| --- | --- | --- | --- |
| Source bundle | `AGENTS.md`, `common/**`, `profiles/**`, `adapters/**`, `skills/**`, `templates/**`, `examples/**`, validators, schemas, and evals | Canonical | Use this layer for authoring, validation, review, and release builds. Do not treat generated `dist/**` as source. |
| Codex | `dist/codex/**` project bundle with `.agents/AGENTS.md` and `.agents/skills/**` after extraction | Canonical target | Keep Codex-only plugin and UI metadata out of Claude output. |
| Claude Code | `dist/claude-code/**` self-contained plugin with `.claude-plugin/plugin.json` and `skills/**` | Canonical target | Use native plugin discovery. Do not depend on `.agents/skills`, `agents/openai.yaml`, or `.codex-plugin`. |
| GitHub Copilot | Human-selected repository/custom-instruction adaptation | Advisory compatibility | Reuse source policies manually where applicable. Do not assume native skill-package semantics, graph metadata, or Codex plugin metadata. |
| Cursor | `dist/cursor/**` project bundle with root `.cursor/rules/**` and the approved shared policy pointer | Canonical target | Keep Cursor entrypoints at the host project root after extraction. |
| Windsurf | Human-selected rules adaptation | Advisory compatibility | Reuse concise rules and workflow fragments manually. Do not rely on this bundle's manifests or generated targets as Windsurf-native packages. |
| Generic coding agents | `AGENTS.md` plus selected `common/**` and `skills/**/SKILL.md` procedures | Partial | Apply only the workflow text that matches the host's instruction model and available tools. Keep approval gates and local-only boundaries intact. |

## Portability Rules

- Treat `AGENTS.md`, `common/**`, `profiles/**`, `adapters/**`, `skills/**`,
  `templates/**`, `examples/**`, schemas, validators, and evals as the
  publishable source model.
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
- Treat host-specific rules for Copilot, Windsurf, and generic agents as
  adaptations, not first-class package outputs, until dedicated contracts,
  validators, and release artifacts exist.

## Rules

- Keep rich `.agents` graph metadata in source files.
- Strip source graph metadata from every generated target so maintenance links
  do not consume runtime context.
- Generate portable `SKILL.md` frontmatter for distribution targets.
- Ship the portable core, default profile, and exactly one matching canonical
  adapter in every generated target.
- Include `agents/openai.yaml` only in Codex-compatible skill or plugin output.
- Include `.codex-plugin/plugin.json` only in Codex plugin output; do not expose
  the internal `bundle-manifest.json` as a platform manifest.
- Build Claude Code as a self-contained native plugin with
  `.claude-plugin/plugin.json` and `skills/**`.
- Keep Claude Code output free of Codex-only plugin and UI metadata.
- Keep target aliases declarative and reuse the canonical target implementation.
- Do not include `project/**`, local-only overlays, host-project facts, build
  output, vendor files, caches, or dependency internals in distribution targets.
- Do not package UI component library skills or testing skills.
- Require target contract validation before building generated output.
- Require native artifact validation before publishing a canonical target.
