# WebDev Assistant — Remaining Work Plan

Branch: `architecture/webdev-assistant-skill-pack`  
Status date: 2026-06-29  
Purpose: concise checklist of what remains after the current implementation work.

## Current completed baseline

Already implemented in the architecture branch:

- Prompt intent / task scale routing.
- System skills:
  - `goal-planner`
  - `execution-plan-manager`
  - `mcp-toolchain-manager`
- Design intelligence layer:
  - `frontend-design-director`
  - design quality rubric
  - anti-template defaults
  - interface copy rules
  - motion rules
  - design direction contract template
  - visual memory template
- Frontend architecture / greenfield skills:
  - `frontend-architecture-planner`
  - `greenfield-project-builder`
- Lint verification layer:
  - `frontend-linter-manager`
  - `common/lint-verification-rules.md`
  - lint policy plan note
- README runtime boundary:
  - `README.md` is human-facing only and must not be used for agent runtime context.

## What remains

### 1. Finish Agent Operating System common files

Create reusable common rules and templates that support the already-added `goal-planner` and `execution-plan-manager`.

Files to add:

- `common/agent-operating-model.md`
- `common/goal-contract.md`
- `common/planning-rules.md`
- `common/execution-loops.md`
- `common/token-budget-rules.md`
- `common/checkpoint-rules.md`
- `templates/goal-contract.md`
- `templates/execution-plan.md`
- `templates/progress-log.md`
- `templates/decision-log.md`
- `templates/context-index.md`

Done when:

- goal and execution plan contracts are reusable;
- token budget rules are explicit;
- stop/resume behavior is concrete;
- no app source files are created;
- project-specific state remains local-only in `project/**`.

### 2. Add frontend boundary common files

The architecture and greenfield skills exist, but the reusable boundary policies are still missing.

Files to add:

- `common/framework-adaptation-policy.md`
- `common/framework-source-map.md`
- `common/state-ownership-rules.md`
- `common/routing-boundary-rules.md`
- `common/data-fetching-boundary-rules.md`
- `common/form-boundary-rules.md`
- `common/build-tool-boundary-rules.md`
- `common/frontend-integration-boundaries.md`

Optional local-only overlay templates / references:

- `project/docs-profile.md`
- `project/build-profile.md`
- `project/workspace-profile.md`
- `project/state-management-profile.md`
- `project/data-fetching-profile.md`

Done when:

- framework guidance prefers local project conventions first;
- state/data/form/routing ownership rules are explicit;
- no framework migration, package install, UI library, or testing workflow is introduced by default.

### 3. Add debugging and refactor skills

Skills to create:

- `skills/frontend-bugfix-debugger/SKILL.md`
- `skills/frontend-bugfix-debugger/agents/openai.yaml`
- `skills/frontend-refactor-surgeon/SKILL.md`
- `skills/frontend-refactor-surgeon/agents/openai.yaml`

Common files to add:

- `common/typescript-discipline.md`
- `common/debugging-evidence-rules.md`
- `common/refactor-safety-rules.md`

Done when:

- bugfix skill starts from evidence and symptom reproduction;
- refactor skill preserves behavior unless change is approved;
- lint verification is included after code changes;
- UI changes trigger visual QA when applicable;
- no testing skill or test-generation workflow is introduced.

### 4. Add frontend quality reviewer

Skill to create:

- `skills/frontend-quality-reviewer/SKILL.md`
- `skills/frontend-quality-reviewer/agents/openai.yaml`

Common files to add:

- `common/review-severity-model.md`
- `common/security-review-rules.md`
- `common/performance-review-rules.md`

May reuse / reference:

- `common/typescript-discipline.md`
- `common/build-tool-boundary-rules.md`
- `common/lint-verification-rules.md`
- `common/design-quality-rubric.md`

Done when:

- review verdict supports `pass`, `pass with concerns`, `fail`;
- severity labels exist: `blocking`, `high`, `medium`, `low`, `nit`, `praise`;
- review distinguishes required fixes from optional improvements;
- claims require evidence;
- lint result is checked when code changed;
- no broad rewrite is triggered by review findings.

### 5. Integrate existing screenshot pipeline

Existing skills to update:

- `skills/design-screenshot-spec/SKILL.md`
- `skills/frontend-layout-implementer/SKILL.md`
- `skills/frontend-visual-qa/SKILL.md`

Integration targets:

- connect screenshot spec with `frontend-design-director`;
- connect implementation with `frontend-architecture-planner` when structure matters;
- run `frontend-linter-manager` after code-changing implementation;
- run `frontend-quality-reviewer` before final reporting when quality review is requested or appropriate;
- preserve Figma boundary: screenshots/exports/inspect values only, no Figma MCP.

Done when:

- screenshot-to-code flow still works;
- implementation does not happen before spec/design direction when needed;
- rendered verification remains QA evidence, not a testing skill;
- README is not used for runtime context.

### 6. Implement Codex + Claude compatibility packaging

Architecture addendum exists, but implementation remains.

Files / targets to add:

- `common/cross-agent-compatibility-rules.md`
- `common/portable-skill-core-contract.md`
- `scripts/build_skill_targets.py`
- `scripts/validate_codex_skill_pack.py`
- `scripts/validate_claude_skill_pack.py`
- `dist/codex/**`
- `dist/claude/**`

Decisions to finalize:

- single-source skills vs generated `dist/**`;
- exact Claude-compatible package shape;
- whether extra graph metadata remains in source only;
- validation checklist for both targets.

Done when:

- Codex target validates;
- Claude target validates or has a documented manual checklist;
- `project/**` is not included in distributions;
- README remains human-facing only;
- no UI component library or testing skill is packaged.

### 7. Package for distribution

Files / assets to add:

- `plugin.json`
- `examples/**`
- `scripts/validate_skill_pack.py`
- `CHANGELOG.md`
- install documentation
- demo workflows

README work:

- update only as classic human-facing repo README;
- do not make README part of agent runtime flow.

Done when:

- install instructions are short;
- examples are realistic;
- skill descriptions are concise;
- validation script checks required files;
- local-only project facts are excluded;
- package excludes UI component libraries and testing skills.

### 8. Deferred optional verticals

Do not implement yet. Only consider after core skill pack stabilization and repeated demand:

- `frontend-video-adapter`
- `mobile-frontend-adapter`
- `frontend-auth-integration-adapter`
- `frontend-data-integration-adapter`

Rules:

- keep them frontend-boundary focused;
- require official docs and explicit user scope;
- do not turn the pack into backend, ORM, database, mobile-generalist, or testing tooling.

## Recommended next iterations

1. Add Agent Operating System common files and templates.
2. Add frontend boundary common files.
3. Add `frontend-bugfix-debugger`.
4. Add `frontend-refactor-surgeon`.
5. Add `frontend-quality-reviewer`.
6. Integrate existing screenshot pipeline with design, architecture, lint, and quality review.
7. Add Codex/Claude compatibility packaging.
8. Add distribution packaging.

## Current high-level status

The core routing and major planning/design/architecture/lint skills are in place. The remaining work is mostly about:

- common rule completeness;
- bugfix/refactor/quality skills;
- integration of old screenshot skills with new layers;
- distribution and cross-agent packaging.
