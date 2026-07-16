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
    - '[[docs/README|WebDev Agent Kit Documentation]]'
depends_on: []
---

# Runtime Target Contracts

[← All documentation](../README.md)

Purpose: define the native installation, policy entrypoint, skill discovery
root, alias ownership, and validation boundary for every release target.

`bundle-manifest.json` is the machine-readable source of truth for these
contracts. Generated `dist/**` files are build output and must not redefine
them.

## Canonical Targets

| Target | Kind | Install mode | Entrypoint | Skill root |
| --- | --- | --- | --- | --- |
| `codex` | Project bundle | Extract from the host project root | `.agents/AGENTS.md` through a minimal host-root `AGENTS.md` pointer | `.agents/skills` |
| `claude-code` | Plugin | Install through a local marketplace using the native Claude Code plugin flow | `.claude-plugin/plugin.json` through `.claude-plugin/marketplace.json` | `skills` inside the plugin root |
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

- `common/core/runtime-core-policy.md` owns the compact client-neutral behavior.
- `profiles/react-typescript/PROFILE.md` activates stack defaults only from repository evidence and defers details to owning common rules.
- `adapters/**` owns only native discovery, entrypoints, tool registries, sandbox, and configuration differences. Each generated target ships one canonical adapter; aliases reuse it.
- Source `skills/**` remains portable authoring source. Claude-generated skills load the core, conditional profile, and matching adapter explicitly.
- Codex-only `agents/openai.yaml` metadata is emitted only for Codex-compatible plugin or skill targets.
- Claude Code receives a self-contained native plugin installable through its local marketplace and must not depend on `.agents/skills` for native skill discovery.
- Project-local facts remain in host `.agents/project/**` overlays and are never published inside a reusable plugin.
- Generated targets exclude human-facing repository docs, local overlays, caches, dependencies, and internal bundle manifests.
- Generated targets strip source graph frontmatter from policy, common, profile, adapter, template, and reference Markdown. Generated skills retain only portable `name` and `description` frontmatter.

## Validation Boundary

`scripts/validate_target_contracts.py` validates the declaration layer:

- the canonical target set;
- the alias map;
- required contract fields;
- safe relative paths;
- unique canonical output paths;
- validator existence;
- plugin and project-bundle install-mode consistency.

Target construction is split into `build_codex_project_target()`,
`build_codex_plugin_target()`, `build_claude_plugin_target()`, and
`build_cursor_project_target()` so native packaging rules cannot leak between
clients.

`scripts/validate_codex_project_target.py`,
`scripts/validate_codex_plugin_target.py`,
`scripts/validate_claude_plugin_target.py` and
`scripts/validate_cursor_target.py` validate their native target contracts
independently. `scripts/validate_version_consistency.py` aligns source and
generated versions.

`scripts/validate_release_archive.py` builds and extracts release fixtures,
then verifies native skill paths, internal links, exclusions, checksum entries,
single `.agents` nesting, preservation of existing host-root instructions, and
the Claude marketplace manifest. Cursor archives place shared runtime under
`.agents/` and native rules under root `.cursor/`; Claude skills remain inside
the native plugin root.

`scripts/validate_runtime_layers.py` enforces the layer inventory, prevents
client-specific terms in the core and project profile, caps their context size,
and checks that generated targets contain exactly one matching adapter.
`scripts/validate_runtime_context_budget.py` exposes the release gate backed by
`scripts/validate_context_budgets.py`; it caps the compact entrypoint, runtime
layers, skill-discovery descriptions, and generated skill prelude while also
rejecting source graph metadata in runtime artifacts.

## Release-Ready State

Codex project and plugin surfaces, the native Claude Code plugin, and the Cursor
project target have independent builders and validators. Compatibility aliases
reuse canonical generated content. Release publication is gated by extracted
archive fixtures rather than directory inspection alone.

[← All documentation](../README.md) · [Installation guides](../install/README.md)
