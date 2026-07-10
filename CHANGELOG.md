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

- Added machine-readable runtime contracts for canonical Codex, Claude Code, and Cursor targets.
- Added `scripts/validate_target_contracts.py` to enforce canonical target, alias, entrypoint, skill-root, output, and validator declarations.
- Added `docs/architecture/runtime-target-contracts.md` as the human-readable target contract.
- Added a native Claude Code plugin manifest and structural artifact validator.
- Added a compact portable runtime core, evidence-gated React/TypeScript profile, and thin Claude Code, Codex, and Cursor adapters.
- Added runtime-layer validation for client neutrality, context budgets, manifest alignment, and generated adapter selection.
- Added a centralized eight-level policy precedence contract and validator for forbidden absolute authority claims.
- Added eight cross-client policy conflict evals covering every adjacent precedence boundary.
- Added a targeted README read/edit policy, technical evidence hierarchy, and six cross-model README behavior evals.
- Added a test change policy and eight evals separating existing-test maintenance from new tests and infrastructure.
- Added full 19-skill capability coverage, strict capability metadata validation, and eight cross-client capability behavior evals.
- Added deterministic budgets for the always-on entrypoint, runtime layers, skill-discovery descriptions, and Claude skill prelude.
- Added fact-based output evals and deterministic final-answer budgets, including a 180-word cap for lightweight workflows.
- Added a 12-case GPT/Claude parity suite covering routing, context, README, tests, precedence, capabilities, verification, output, onboarding, and scope control.
- Added independent Codex project, Codex plugin, Claude plugin, and Cursor target validators plus source/generated version consistency checks.
- Added deterministic release archive construction and extracted archive fixtures for native paths, exclusions, links, checksums, and root-instruction safety.
- Added `common/windows-shell-sandbox-rules.md` for Windows PowerShell package-manager fallbacks and sandbox-blocked build, dev-server, and browser verification.
- Added trigger and output eval coverage for Windows shell and sandbox verification blockers.
- Added trigger and output eval coverage for unauthorized component, helper, hook, or function test authoring during frontend implementation.

### Changed

- Replaced independent client target entries with three canonical targets and explicit compatibility aliases.
- Defined Claude Code as a native plugin target and VS Code client packages as aliases of their canonical runtimes.
- Claude Code now builds as a self-contained native plugin with portable skill frontmatter, stripped source graph metadata, and no Codex-only plugin or UI metadata.
- Legacy `claude` and `vs-code-claude` outputs now reuse the canonical `claude-code` artifact exactly.
- Claude project-policy onboarding now uses the exact `@.agents/AGENTS.md` import and requires approval before creating or merging host instructions.
- Runtime routing now loads core, project profile, client adapter, local conventions, and task skill as separate progressive-disclosure layers.
- Generated targets now ship the portable core, default profile, and exactly one canonical client adapter; Claude skills load those layers explicitly.
- Runtime skills, profiles, adapters, and project facts now resolve instruction conflicts through one shared precedence contract.
- README may now be read for relevant intent, setup, onboarding, audit, and drift questions, but it is never sufficient technical proof and cannot be edited without an explicit current user request.
- Relevant existing tests may now be run and maintained for confirmed contract changes; new tests remain explicit-request-only, infrastructure remains approval-gated, and routine skipped-test output is removed.
- README now documents Windows shell and sandbox verification behavior as a user-facing boundary.
- Lint, bounded retry, smart verification, rendered visual QA, and linter skill rules now stop repeated verification attempts after Windows shell or sandbox blockers and require honest blocked-check reporting.
- Tool capability metadata now represents approved out-of-sandbox fallback and repeated sandbox-blocked dev-server limits for rendered visual evidence.
- Codex `agents/openai.yaml` files now contain only UI and invocation metadata; optional MCP and native-provider candidates live exclusively in the client-neutral capability manifest.
- Capability availability now requires current-registry, validated-profile, or user-supplied-reference evidence; package, config, and provider names are explicitly non-proof.
- Replaced the long always-on policy catalog with a 19-skill compact index and progressive-disclosure routes while preserving detailed rules in owning common docs and skills.
- Compressed all skill discovery descriptions and stripped source graph frontmatter from every generated target.
- Final responses now default to `Changed`, `Verified`, and `Blocked` facts while omitting request echo, skill narration, empty headings, and raw logs.
- Aligned `bundle-manifest.json`, `.codex-plugin/plugin.json`, and `tool-capabilities-manifest.json` with the `0.3.0` next-release metadata.
- Expanded bundle manifest target metadata and schema validation to include `codex`, `claude`, `claude-code`, `cursor`, `vs-code-codex`, and `vs-code-claude` generated targets.
- Release workflow and full validation orchestrator now run schema validation with `--strict-graph`.
- New skill templates now quote the placeholder `description` value so generated drafts do not start with invalid YAML.
- README boundary wording now matches runtime policy: agents must not inspect host README content and must ask for excerpts instead.
- Test authoring rules now explicitly block component, hook, function or unit, integration, E2E, snapshot, fixture, mock, and visual regression tests unless the user explicitly asks and approves the exact scope.
- Codex archives extract runtime under `.agents/`; Cursor archives place shared runtime under `.agents/` and native rules under root `.cursor/`; Claude archives retain their native plugin root.
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
