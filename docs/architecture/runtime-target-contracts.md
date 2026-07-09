---
id: 'agents.docs.architecture.runtime-target-contracts'
title: 'Runtime Target Contracts'
doc_type: 'architecture'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags:
    - 'docs/architecture'
    - 'packaging/contracts'
parent:
    - '[[common/cross-agent-compatibility-rules|Cross-Agent Compatibility Rules]]'
related:
    - '[[common/portable-skill-core-contract|Portable Skill Core Contract]]'
depends_on: []
---

# Runtime Target Contracts

Purpose: define the native installation, policy entrypoint, skill discovery
root, alias ownership, and validation boundary for every release target.

`bundle-manifest.json` is the machine-readable source of truth for these
contracts. Generated `dist/**` files are build output and must not redefine
them.

## Canonical Targets

| Target | Kind | Install mode | Entrypoint | Skill root |
| --- | --- | --- | --- | --- |
| `codex` | Project bundle | Extract from the host project root | `.agents/AGENTS.md` through a minimal host-root `AGENTS.md` pointer | `.agents/skills` |
| `claude-code` | Plugin | Install through the native Claude Code plugin flow | `.claude-plugin/plugin.json` | `skills` inside the plugin root |
| `cursor` | Project bundle | Extract from the host project root | `.cursor/rules/webdev-agent-kit.mdc` plus the approved host-root pointer | `.agents/skills` through the shared project policy |

Canonical targets own build behavior. Each canonical target must declare one
safe output path, install mode, entrypoint, skills root, and contract validator.

## Target Aliases

Aliases reuse the canonical target contract and must not define independent
build or runtime behavior:

| Alias | Canonical target |
| --- | --- |
| `claude` | `claude-code` |
| `vs-code-claude` | `claude-code` |
| `vs-code-codex` | `codex` |

An alias may keep a compatibility download name, but its content, validation,
and release behavior come from the canonical target.

## Source And Runtime Boundaries

- Source `skills/**` and `common/**` remain client-neutral authoring sources.
- Codex-only `agents/openai.yaml` metadata is emitted only for Codex-compatible
  plugin or skill targets.
- Claude Code receives a self-contained native plugin and must not depend on
  `.agents/skills` for native skill discovery.
- Project-local facts remain in host `.agents/project/**` overlays and are never
  published inside a reusable plugin.
- Generated targets exclude human-facing repository docs, local overlays,
  caches, dependencies, and internal bundle manifests.

## Validation Boundary

`scripts/validate_target_contracts.py` validates the declaration layer:

- the canonical target set;
- the alias map;
- required contract fields;
- safe relative paths;
- unique canonical output paths;
- validator existence;
- plugin and project-bundle install-mode consistency.

Artifact layout, archive extraction, and native client discovery validators are
added with the corresponding target builders. A release must eventually pass
both contract validation and target artifact validation.

## Migration State

The contract is declared before target builders are migrated. During the
`v0.3.0` branch, temporary generated layouts may still reflect the older shared
archive model. They are not release-ready until the Claude plugin, Codex
project bundle, Cursor project bundle, alias build, and archive validators match
this document.
