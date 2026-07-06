---
id: 'agents.audit-and-optimization-plan'
title: 'Audit And Optimization Status'
doc_type: 'audit-status'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/audit'
    - 'governance'
    - 'roadmap'
parent: []
related:
    - '[[AGENTS|Canonical Agent Policy]]'
    - '[[CONTRIBUTING|Contributing To WebDev Agent Kit]]'
    - '[[SECURITY|WebDev Agent Kit Security Policy]]'
    - '[[CHANGELOG|WebDev Agent Kit Changelog]]'
    - '[[common/cross-agent-compatibility-rules|Cross-Agent Compatibility Rules]]'
depends_on: []
---

# Audit And Optimization Status

This document is the current status record for the audit and optimization pass that led to WebDev Agent Kit `v0.1.0`. It replaces the original audit roadmap as the active source of truth for what is complete and what remains open.

## Review Role

Use the role of Principal AI Systems Architect and Staff Developer Experience Engineer. Review the bundle as an installable source bundle, a portable skill pack, a policy graph for frontend engineering workflows, and a package of executable agent instructions.

## Current Release Status

`v0.1.0` is the first release-ready baseline for WebDev Agent Kit.

The release baseline includes:

- source-bundle validation;
- schema validation;
- initial skill trigger evals;
- initial skill output evals;
- Codex and Claude portable target builds;
- Codex and Claude target validation;
- release workflow for tagged artifacts;
- Apache License 2.0;
- contribution and security governance;
- blocking Ruff lint, Ruff format, yamllint, and markdownlint quality gates;
- README runtime exclusion and human-only boundary;
- host compatibility matrix for source, Codex, Claude, Copilot, Cursor, Windsurf, and generic coding-agent adaptations.

## Completed Work

### Source And Runtime Model

- `AGENTS.md` is the canonical runtime policy entrypoint.
- `README.md` is human-facing only and excluded from agent runtime, routing, source inventory, and validation.
- `skills/**` contains executable skill instructions.
- `common/**` contains reusable runtime rules.
- `templates/**` contains optional local artifact templates.
- `project/**` is local-only host-project overlay state and must not be published.
- `dist/**` is generated release output and must not be edited as source.

### Packaging And Distribution

- `bundle-manifest.json` tracks source skill inventory, target paths, and publish exclusions.
- `.codex-plugin/plugin.json` is the Codex plugin entrypoint.
- `scripts/build_skill_targets.py` builds `dist/codex` and `dist/claude`.
- Codex target includes `.codex-plugin/plugin.json` and `skills/*/agents/openai.yaml`.
- Claude target excludes Codex-only `.codex-plugin` and `agents/openai.yaml` metadata.
- `project/**`, `.obsidian/**`, `node_modules/**`, and internal generated/source-only artifacts are excluded from distribution targets.

### Validation And CI

- `scripts/validate_skill_pack.py` orchestrates schema validation, source validation, eval validation, target build, and target validation.
- `scripts/validate_schemas.py` provides the first schema-first validation pass for bundle metadata, skill frontmatter, OpenAI agent metadata, and graph docs.
- `scripts/validate_source_bundle.py` validates graph metadata, source inventory, skill structure, stale names, license presence, and clean-checkout behavior.
- `scripts/validate_skill_evals.py` validates trigger and output eval fixtures.
- `scripts/validate_codex_skill_pack.py` validates the generated Codex target.
- `scripts/validate_claude_skill_pack.py` validates the generated Claude target.
- `.github/workflows/skill-pack-ci.yml` runs structural validation on pull requests and relevant pushes.
- `.github/workflows/quality-ci.yml` enforces Ruff lint, Ruff format, yamllint, and markdownlint quality gates.

### Eval Layer

- `evals/trigger-evals.json` contains initial should-trigger and should-not-trigger routing fixtures for high-value skills.
- `evals/output-evals.json` contains initial output contract fixtures for review, bugfix, visual QA, layout implementation, and bundle-maintenance workflows.
- `schemas/eval-suite.schema.json` and `schemas/eval-case.schema.json` define eval fixture structure.

### Governance And Release

- `LICENSE` uses Apache License 2.0.
- `CHANGELOG.md` records release behavior and validation changes.
- `CONTRIBUTING.md` documents contribution rules and review expectations.
- `SECURITY.md` documents supply-chain and executable-instruction safety rules.
- `.github/workflows/release.yml` builds and publishes Codex and Claude release artifacts from tags matching `v*.*.*`.

## Still Open

### P1: Replace Custom YAML Subset Parsing

Schema files exist, but some validators still parse frontmatter and `agents/openai.yaml` through local helper functions. Replace the custom YAML subset parser with a real schema-backed YAML loader, then keep custom Python checks only for semantic rules schemas cannot express.

Acceptance criteria:

- `SKILL.md` frontmatter is parsed by a standard YAML loader.
- `agents/openai.yaml` is parsed by a standard YAML loader.
- Existing schemas remain the structural contract.
- Error messages stay file-specific and actionable.
- `python scripts/validate_skill_pack.py` passes.

### P1: Expand Eval Coverage

The initial eval layer exists. Add more realistic fixtures before changing routing descriptions or adding new skills.

Acceptance criteria:

- every high-value skill has multiple should-trigger and should-not-trigger cases;
- output evals cover bugfix, visual QA, quality review, layout implementation, onboarding, and skill-authoring workflows;
- near-miss prompts test over-planning, false design escalation, false bugfix escalation, and unsupported target-stack behavior.

### P1: Add Link Checking

Add a link checker for Markdown links and official-source references.

Acceptance criteria:

- link checker runs in CI or a dedicated scheduled workflow;
- generated `dist/**` and local-only `project/**` are excluded;
- README remains human-only and is checked only as documentation, not as agent runtime source;
- official-source references fail clearly when moved or unavailable.

### P2: Usage-Trace Driven Rule Dedupe

The common layer is intentionally broad. Do not deduplicate based on taste alone. First collect which rules are loaded by which skills and which rules overlap in practice.

Candidate overlap areas:

- planning rules versus goal and execution planning skills;
- loop policy versus bounded retry and verification loop rules;
- routing boundary rules versus prompt intent and lightweight routing rules;
- token budget rules versus token economy and context compaction rules.

Acceptance criteria:

- each merge/split is supported by observed routing or maintenance friction;
- `AGENTS.md` remains a thin router and boundary document;
- common rules stay short, scoped, and progressively disclosed;
- skill output contracts and evals are updated when rule ownership changes.

### P2: Skill Maturity Metadata

Add maturity metadata when the release cadence needs stronger lifecycle control.

Suggested fields:

```yaml
metadata:
  version: '0.1.0'
  maturity: 'draft|beta|stable'
  owner: 'webdev-agent-kit'
  last-reviewed: 'YYYY-MM-DD'
  risk: 'low|medium|high'
```

Acceptance criteria:

- schema validates the metadata;
- all skills are assigned a maturity and risk level;
- release notes mention maturity changes;
- deprecated skills have explicit migration guidance.

## Historical Audit Notes

The original audit found a strong architecture with operational gaps. The highest-risk gaps from that audit have been resolved for `v0.1.0`:

- clean reusable-bundle validation no longer requires local `project/**` overlays;
- README is no longer part of runtime validation or routing;
- CI runs source, schema, eval, build, target, formatting, and Markdown checks;
- public OSS governance files exist;
- Codex and Claude target generation is release-driven;
- the initial eval layer exists;
- release artifacts are built from validated source.

Keep this document as a status tracker. Move completed future items into `CHANGELOG.md` and update the `Still Open` section instead of accumulating stale roadmap claims.
