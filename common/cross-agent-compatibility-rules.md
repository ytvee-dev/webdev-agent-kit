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
distribution targets.

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

