---
id: 'agents.changelog'
title: 'WebDev Agent Kit Changelog'
doc_type: 'changelog'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/changelog'
    - 'release-management'
parent: []
related:
    - '[[README|WebDev Agent Kit README]]'
    - '[[AGENTS|Canonical Agent Policy]]'
    - '[[docs/install/README|Installation Guides]]'
depends_on: []
---

# Changelog

All notable changes to WebDev Agent Kit should be recorded in this file.

Use this changelog for source-bundle and distribution-target changes that affect routing, skills, rules, validation, packaging, security, or installation behavior.

## Unreleased

### Added

- Added trigger and output eval coverage for unauthorized component, helper, hook, or function test authoring during frontend implementation.

### Changed

- Aligned `bundle-manifest.json`, `.codex-plugin/plugin.json`, and `tool-capabilities-manifest.json` with the `0.3.0` next-release metadata.
- Expanded bundle manifest target metadata and schema validation to include `codex`, `claude`, `claude-code`, `cursor`, `vs-code-codex`, and `vs-code-claude` generated targets.
- Release workflow and full validation orchestrator now run schema validation with `--strict-graph`.
- New skill templates now quote the placeholder `description` value so generated drafts do not start with invalid YAML.
- README boundary wording now matches runtime policy: agents must not inspect host README content and must ask for excerpts instead.
- Test authoring rules now explicitly block component, hook, function or unit, integration, E2E, snapshot, fixture, mock, and visual regression tests unless the user explicitly asks and approves the exact scope.
- Runtime release archives now extract to a top-level `.agents/` directory regardless of client package.
- Runtime targets no longer include human-facing root files: `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, or `SECURITY.md`.
- Runtime targets no longer include `examples/`.
- Codex and VS Code Codex targets keep `.codex-plugin/`; Claude Code, VS Code Claude, Cursor, and legacy Claude targets do not include it.
- Restored repository-side installation guide drafts so README links and local link checks remain valid after release cleanup.

## 0.2.3 - 2026-07-07

### Added

- Added capability-first tool policy and portable tool capability metadata.
- Added native client adaptation policy and local-only client/tool profile templates.
- Added smart verification budget and diff-impact verification rules to avoid over-testing small visual changes.
- Added host-project documentation boundary rules and README-boundary validation.
- Added Markdown link checking and a scheduled link-check workflow.
- Added stricter TypeScript and frontend anti-patterns for return types, arrow functions, destructuring, status modeling, test authoring, file reads, and callback memoization.
- Added `pattern-library-manager` for reusable pattern and anti-pattern maintenance.
- Added root pointer templates for Codex, VS Code Codex, Cursor, and Claude Code.
- Added Russian draft installation guides under `docs/install/**`.

### Changed

- Toolchain management now reports missing capabilities, fallbacks, approval requirements, and confidence impact.
- Project onboarding now records client and tool profile facts in local-only project overlays.
- Target building now includes legacy Codex/Claude targets plus client-specific targets for Claude Code, Cursor, VS Code Codex, and VS Code Claude.
- The release workflow now publishes stable and versioned client archives.
- `common/anti-patterns/no-use-callback-by-default.md` now requires proof before callback memoization.
- `AUDIT_AND_OPTIMIZATION_PLAN.md` now tracks next-release preparation state.

## 0.1.0 - 2026-07-06

### Added

- Added host compatibility matrix for source, Codex, Claude, Copilot, Cursor, Windsurf, and generic coding-agent adaptation.
- Added formatting and linting configuration for Ruff, markdownlint-cli2, and yamllint.
- Added `quality-ci` workflow for Python, Markdown, and YAML quality checks.
- Added tagged release workflow for validated Codex and Claude portable target artifacts.
- Added initial skill trigger eval fixtures for high-value routing decisions.
- Added initial skill output eval fixtures for review, bugfix, visual QA, layout implementation, and bundle maintenance workflows.
- Added `scripts/validate_skill_evals.py` and JSON schemas for eval suites and eval cases.
- Added repository JSON schemas for bundle manifest metadata, skill frontmatter, OpenAI agent metadata, and graph document frontmatter.
- Added `scripts/validate_schemas.py` as a first schema-first validation pass before source and target validation.
- Added Apache License 2.0 through root `LICENSE` and bundle manifest metadata.
- Added a GitHub Actions validation workflow for source-bundle and generated-target checks.
- Added public contribution and security guidance for the reusable skill bundle.
- Added an audit-driven optimization plan that turns the prior research findings into tracked engineering work.

### Changed

- Cleaned Markdown hygiene issues and made markdownlint a blocking `quality-ci` gate.
- `quality-ci` now treats Ruff lint, Ruff format, yamllint, and markdownlint checks as blocking gates.
- Standardized the Ruff formatter line length for the existing Python formatting baseline.
- Clarified cross-agent portability boundaries for source, generated targets, host-specific metadata, and advisory host adaptations.
- Calibrated markdownlint for this bundle's frontmatter-heavy documents and source-reference files.
- Applied Ruff import and formatting cleanup to Python validation and packaging scripts.
- CI now validates skill eval fixtures before building portable targets.
- `scripts/validate_skill_pack.py` now runs eval validation before build and target validation.
- Hardened source validation so a clean reusable-bundle checkout does not require local-only `project/**` overlays.
- Removed README inventory checks from source validation because `README.md` is human-facing documentation, not an agent runtime or validation source.
- Clarified in runtime policy and authoring rules that `README.md` stays user-facing and outside agent reads.
- Included public OSS docs and `LICENSE` in generated Codex and Claude distribution targets when those files exist.
- `scripts/validate_skill_pack.py` now runs schema validation before legacy source, build, and target validators.
