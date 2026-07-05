---
id: 'agents.audit-and-optimization-plan'
title: 'Audit And Optimization Plan'
doc_type: 'audit-plan'
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
    - '[[README|WebDev Agent Kit README]]'
    - '[[AGENTS|Canonical Agent Policy]]'
    - '[[CONTRIBUTING|Contributing To WebDev Agent Kit]]'
    - '[[SECURITY|WebDev Agent Kit Security Policy]]'
    - '[[CHANGELOG|WebDev Agent Kit Changelog]]'
depends_on: []
---

# Audit And Optimization Plan

This document turns the external audit reports into a repository-local engineering plan. WebDev Agent Kit should behave like a source bundle that can be validated, packaged, reviewed, and safely installed into frontend projects.

## Review Role

Use the role of Principal AI Systems Architect and Staff Developer Experience Engineer. Review the bundle as an installable source bundle, a portable skill pack, a policy graph for frontend engineering workflows, and a package of executable agent instructions.

## High-Level Verdict

The architecture is strong, but operational maturity must improve.

Strengths:

- clear bundle entrypoint in `AGENTS.md`;
- explicit source model for `skills/**`, `common/**`, `templates/**`, `examples/**`, and local-only `project/**` overlays;
- broad skill coverage across onboarding, planning, design, implementation, lint, visual QA, review, refactor, and bugfix work;
- portable target idea through `dist/codex` and `dist/claude`;
- local validators already exist.

Main risks:

- validation must work on a clean reusable-bundle checkout without local `project/**` overlays;
- README inventory checks must track the current documentation structure;
- CI must run the same validators used locally;
- public OSS governance files must exist;
- schema-first validation, evals, and release discipline are not yet complete.

## File-By-File Audit Inventory

### Root And Infrastructure

| Path | Purpose | Finding | Priority |
| --- | --- | --- | --- |
| `AGENTS.md` | Canonical runtime router and policy entrypoint. | Strong routing and progressive disclosure. Keep it thin. | P1 |
| `README.md` | Human-facing install and usage guide. | Good guide, but validation must not depend on one obsolete heading name. | P0 |
| `bundle-manifest.json` | Source inventory and target map. | Good source of truth. Add schema validation later. | P1 |
| `.codex-plugin/plugin.json` | Codex plugin manifest. | Minimal and correct. Keep aligned with bundle version. | P2 |
| `.gitignore` | Excludes local overlays, generated targets, local notes, and noise. | Correctly excludes `project/**`; validators must treat it as optional. | P0 |
| `CHANGELOG.md` | Release notes. | Added to support versioned behavior changes. | P1 |
| `CONTRIBUTING.md` | Contribution policy. | Added to prevent skill drift and document review gates. | P1 |
| `SECURITY.md` | Security policy. | Added because agent skills are executable instructions. | P0 |
| `AUDIT_AND_OPTIMIZATION_PLAN.md` | Audit-to-roadmap bridge. | Added to keep follow-up work explicit and reviewable. | P1 |
| `.github/workflows/skill-pack-ci.yml` | Pull request and push validation. | Added to run structural validators in CI. | P0 |

### Scripts

| Path | Purpose | Finding | Priority |
| --- | --- | --- | --- |
| `scripts/validate_skill_pack.py` | Orchestrates source validation, target build, and target validation. | Correct orchestration. Add richer reporting later. | P1 |
| `scripts/validate_source_bundle.py` | Validates graph metadata, skill inventory, README inventory, and local positive path docs. | Hardened to skip absent local-only `project/**` overlays and accept the README `Skill Map`. | P0 |
| `scripts/build_skill_targets.py` | Builds portable Codex and Claude targets. | Updated to include public docs when present. Future pass should use a manifest-driven allowlist. | P1 |
| `scripts/validate_codex_skill_pack.py` | Validates generated Codex target. | Useful target checklist. Future pass should use shared constants and JSON Schema. | P1 |
| `scripts/validate_claude_skill_pack.py` | Validates generated Claude target. | Correctly blocks Codex-only metadata in Claude output. Future pass should share target validation logic. | P1 |
| `skills/agent-rules-skill-author/scripts/skill_common.py` | Shared skill parsing and generation helpers. | Useful, but still a custom YAML subset parser. Replace with schema-backed parsing later. | P1 |
| `skills/agent-rules-skill-author/scripts/validate_agent_skill.py` | Skill-level validation. | Good local validator. Extend with trigger-eval and schema checks later. | P1 |

### Common Rule Files

The common layer is valuable but broad. Each rule file should stay short, scoped, and loaded only by a matching skill or router decision.

| Path | Audit action |
| --- | --- |
| `common/agent-loop-policy.md` | Keep; every loop needs objective, max attempts, stop conditions, and evidence. |
| `common/agent-operating-model.md` | Keep; avoid duplicate routing already in `AGENTS.md`. |
| `common/anti-patterns.md` | Keep; split only when a skill needs deeper details. |
| `common/anti-template-defaults.md` | Keep; tie examples to design skills. |
| `common/approved-patterns.md` | Keep; add examples only when reusable across projects. |
| `common/bounded-retry-rules.md` | Keep; use with loop workflows and visual repair. |
| `common/build-tool-boundary-rules.md` | Keep; require approval for package manager changes. |
| `common/checkpoint-rules.md` | Keep; route through planning and loop skills. |
| `common/codex-official-docs-policy.md` | Keep; use as primary reference for Codex-specific behavior. |
| `common/context-compaction-rules.md` | Keep; durable memory stays local-only. |
| `common/cross-agent-compatibility-rules.md` | Keep; use during packaging and skill authoring. |
| `common/css-modules-specificity-rules.md` | Keep; load only when CSS Modules change. |
| `common/data-fetching-boundary-rules.md` | Keep; connect to TanStack, Redux, and Axios guidance. |
| `common/data-visualization-rules.md` | Keep; load only for data visual surfaces. |
| `common/debugging-evidence-rules.md` | Keep; bugfix skill should be primary consumer. |
| `common/design-quality-rubric.md` | Keep; design director and visual QA should consume it. |
| `common/documentation-maintenance.md` | Keep; update after new governance files. |
| `common/execution-loops.md` | Review for overlap with loop policy and bounded retry. |
| `common/feedback-cycle-policy.md` | Keep if distinct from loop contracts; otherwise merge later. |
| `common/form-boundary-rules.md` | Keep; load only for form surfaces. |
| `common/form-feedback-rules.md` | Keep; connect with accessibility and validation evidence. |
| `common/framework-adaptation-policy.md` | Keep; important portability rule. |
| `common/framework-source-map.md` | Keep; verify links and supported stack boundaries. |
| `common/frontend-implementation-boundaries.md` | Keep; avoid duplicating `AGENTS.md` guardrails. |
| `common/frontend-integration-boundaries.md` | Keep; tie to architecture planning. |
| `common/goal-contract.md` | Keep; goal planner should own durable artifact generation. |
| `common/icon-quality-rules.md` | Keep; prevent new icon packages by default. |
| `common/independent-review-rules.md` | Keep; important for loop final judgment. |
| `common/interface-copy-rules.md` | Keep; load for interface text and forms. |
| `common/lightweight-routing-policy.md` | Keep; critical defense against over-planning. |
| `common/lint-verification-rules.md` | Keep; align with linter manager. |
| `common/mobile-responsive-rules.md` | Keep; load for layout and visual QA tasks. |
| `common/motion-rules.md` | Keep; avoid animation-library defaults. |
| `common/navigation-ux-rules.md` | Keep; load only when navigation changes. |
| `common/performance-review-rules.md` | Keep; add measurable checks when project profile exists. |
| `common/planning-rules.md` | Review for overlap with goal and execution skills. |
| `common/portable-skill-core-contract.md` | Keep; use in authoring and target validation. |
| `common/prompt-intent-routing-rules.md` | Keep; one of the most important router references. |
| `common/refactor-safety-rules.md` | Keep; refactor skill should consume it. |
| `common/rendered-visual-verification-policy.md` | Keep; visual QA should be primary consumer. |
| `common/review-severity-model.md` | Keep; align with contribution guide severity labels. |
| `common/routing-boundary-rules.md` | Review for overlap with prompt intent rules. |
| `common/rule-audit-findings.md` | Keep only if current; otherwise convert to this plan or changelog entries. |
| `common/security-review-rules.md` | Keep; align with `SECURITY.md`. |
| `common/skill-applicability-policy.md` | Keep; important outside target stack. |
| `common/state-ownership-rules.md` | Keep; architecture and implementation skills should consume it. |
| `common/stop-criteria-rules.md` | Keep; important for loops and blocked verification. |
| `common/target-stack-policy.md` | Keep; canonical stack boundary. |
| `common/token-budget-rules.md` | Keep; should remain short and operational. |
| `common/token-economy-rules.md` | Keep; avoid duplicate advice with token budget rules. |
| `common/typescript-discipline.md` | Keep; load for TypeScript-changing tasks. |
| `common/ui-ux-priority-checklist.md` | Keep; useful in review and implementation. |
| `common/verification-loop-rules.md` | Keep; align with linter, visual QA, and bugfix workflows. |
| `common/worktree-parallelism-rules.md` | Keep; load only for parallel execution tasks. |
| `common/anti-patterns/README.md` | Keep; useful progressive-disclosure entrypoint. |
| `common/anti-patterns/no-as-const-variables.md` | Keep; TypeScript-specific. |
| `common/anti-patterns/no-anonymous-functions.md` | Keep; implementation and review skills should use it. |
| `common/anti-patterns/no-use-callback-by-default.md` | Keep; good targeted rule. |
| `common/anti-patterns/no-render-functions.md` | Keep; implementation and refactor skills should use it. |
| `common/anti-patterns/no-nested-array-pipelines.md` | Keep; implementation and review skills should use it. |
| `common/anti-patterns/no-component-loops.md` | Keep; clarify examples if false positives appear. |
| `common/anti-patterns/no-unapproved-test-infrastructure.md` | Keep; important approval gate. |

### Examples And Templates

| Path | Audit action |
| --- | --- |
| `examples/bugfix-refactor-review.md` | Update old aliases if any remain from previous project names. |
| `examples/screenshot-to-frontend.md` | Keep source-first and no-Figma boundary explicit. |
| `templates/context-index.md` | Keep local-only usage clear. |
| `templates/decision-log.md` | Keep concise; do not duplicate progress log. |
| `templates/design-direction-contract.md` | Keep tied to design director output. |
| `templates/execution-plan.md` | Keep slice, verification, context budget, and stop/resume fields. |
| `templates/goal-contract.md` | Keep done criteria explicit. |
| `templates/loop-memory.md` | Keep local-only; never publish host facts. |
| `templates/loop-workflow-contract.md` | Keep max attempts, retry strategy, and final judgment fields. |
| `templates/progress-log.md` | Keep factual and compact. |
| `templates/visual-memory.md` | Keep only accepted facts and evidence. |

### Skill Packages

| Skill | Audit action |
| --- | --- |
| `agent-rules-skill-author` | Highest leverage. Continue moving audit policy into validators and contribution checks. |
| `design-screenshot-spec` | Keep Figma boundary explicit and avoid live-link assumptions. |
| `execution-plan-manager` | Add evals for over-planning versus appropriate planning. |
| `frontend-architecture-planner` | Keep target-stack-specific and avoid non-target framework claims. |
| `frontend-bugfix-debugger` | Add trigger evals for bug reports versus broad refactors. |
| `frontend-design-director` | Keep separate from implementation. |
| `frontend-design-intelligence` | Keep as pre-implementation design reasoning. |
| `frontend-layout-implementer` | Keep dependency, token, styling, and architecture approval gates strict. |
| `frontend-linter-manager` | Keep no-setup-without-approval rule. |
| `frontend-quality-reviewer` | Maintain severity model and independent review boundaries. |
| `frontend-refactor-surgeon` | Keep refactor distinct from redesign and feature work. |
| `frontend-visual-qa` | Keep rendered evidence-driven. |
| `goal-planner` | Keep goal, constraints, non-goals, and done criteria measurable. |
| `greenfield-project-builder` | Keep scaffold approval gates and package boundaries explicit. |
| `loop-workflow-planner` | Keep retry limits and final independent judgment explicit. |
| `mcp-toolchain-manager` | Never install or configure tools without approval. |
| `project-context-adapter` | Keep writes local-only and evidence-backed. |
| `project-onboarding-adapter` | Must not be required for clean source validation. |

## Rule Audit Summary

Fixed in this branch:

- source validation no longer assumes local-only `project/**` files exist;
- README inventory validation now accepts the actual `Skill Map` structure;
- CI now runs the source and target validators;
- contribution, security, and changelog docs now exist;
- distribution builds copy public OSS docs when present.

Remaining high-value improvements:

1. Add JSON Schema or Pydantic validation for `SKILL.md` frontmatter and `agents/openai.yaml`.
2. Add trigger eval files for every high-value skill.
3. Add link checking for Markdown and official-source references.
4. Normalize Markdown wrapping and Python formatting after the validator passes in CI.
5. Deduplicate overlapping common rules only after usage traces show real overlap.
6. Add a release workflow that builds `dist/codex` and `dist/claude` artifacts from a tag.

## Roadmap

### Phase 0: Stabilize The Bundle

- Keep CI green on every pull request.
- Ensure clean checkout validation does not need local overlays.
- Keep README, manifest, plugin metadata, and skill directories aligned.

### Phase 1: Make Validation Schema-First

- Add schemas for skill frontmatter, `agents/openai.yaml`, bundle manifest, and plugin manifest.
- Replace custom YAML subset parsing with schema-backed loaders.
- Keep custom semantic checks only where schemas cannot express the rule.

### Phase 2: Add Evals

- Add skill-local eval fixtures for should-trigger and should-not-trigger prompts.
- Add output-quality fixtures for bugfix, visual QA, quality review, and layout implementation.
- Record pass/fail criteria in each skill.

### Phase 3: Improve Distribution And Release Discipline

- Add release notes discipline through `CHANGELOG.md`.
- Build release artifacts for Codex and Claude targets.
- Add manual inspection steps for executable instructions.

### Phase 4: Optimize Rule Surface

- Measure which common rules are loaded by which skills.
- Merge or split rules based on observed routing, not taste.
- Keep `AGENTS.md` as router and boundary document, not a full encyclopedia.

## Definition Of Done For This Optimization Pass

This branch is ready for review when:

- `python scripts/validate_skill_pack.py` passes in CI;
- public governance files are present and graph-valid;
- source validation works without `project/**`;
- README inventory drift is no longer caused by heading-name mismatch;
- follow-up work is tracked in this file and `CHANGELOG.md`.
