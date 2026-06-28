# Skill Pack Implementation Plan

Status: draft plan.
Scope: staged plan for turning the architecture into concrete skills later.

## Current Branch Goal

This branch captures the full architecture for the future WebDev Assistant skill pack.

This branch does not implement new runtime skills yet. It defines the target system so each future skill can be designed deliberately and reviewed independently.

## Current Scope

Completed in this architecture draft:

```text
1. Architecture index
2. Full skill pack blueprint
3. Agent operating model
4. MCP/tooling architecture
5. Design intelligence architecture
6. Implementation plan
```

Out of scope for this branch:

```text
- creating production-ready new skills
- renaming existing skills
- changing runtime routing
- creating a pull request
- installing MCP servers
- changing project source code
```

## Guiding Implementation Rules

- Implement one skill or common rule group per future branch.
- Keep each skill focused on one job.
- Write all reusable instructions in English.
- Keep host-project facts in `project/**` only.
- Use official docs before framework-specific claims.
- Use MCP/tool dependencies deliberately.
- Add validation gates before broadening scope.
- Do not create large unreviewable diffs.

## Phase 0: Architecture Draft

Status: in progress on this branch.

Deliverables:

```text
docs/skill-pack/README.md
docs/skill-pack/ARCHITECTURE.md
docs/skill-pack/OPERATING_MODEL.md
docs/skill-pack/MCP_TOOLING.md
docs/skill-pack/DESIGN_INTELLIGENCE.md
docs/skill-pack/IMPLEMENTATION_PLAN.md
```

Done when:

```text
- architecture is captured in English;
- future skill catalog is clear;
- operating model is explicit;
- MCP/tooling policy is explicit;
- design intelligence layer is captured;
- no PR is created.
```

## Phase 1: Stabilize Existing Skill Pack Foundation

Future branch suggestion:

```text
architecture/stabilize-existing-skill-pack
```

Goals:

- align current `AGENTS.md` with the broader WebDev Assistant architecture;
- preserve existing screenshot-to-frontend pipeline;
- keep existing skills working;
- update `SUMMARY.md` and README only after routing changes are approved;
- avoid creating new skills until the operating model is agreed.

Candidate changes:

```text
AGENTS.md
README.md
SUMMARY.md
common/approved-patterns.md
common/anti-patterns.md
```

Validation:

```text
- existing skill names still route correctly;
- screenshot-to-frontend workflow remains intact;
- no local-only project facts leak into publishable docs;
- no non-English reusable instructions are introduced.
```

## Phase 2: Add Agent Operating System Files

Future branch suggestion:

```text
feature/agent-operating-system
```

Goals:

- add common operating model rules;
- add planning and checkpoint templates;
- add project overlay templates for goals, plans, progress, decisions, and context index.

Candidate files:

```text
common/agent-operating-model.md
common/goal-contract.md
common/planning-rules.md
common/execution-loops.md
common/token-budget-rules.md
common/checkpoint-rules.md
templates/goal-contract.md
templates/execution-plan.md
templates/progress-log.md
templates/decision-log.md
templates/context-index.md
```

Validation:

```text
- rules are general and publishable;
- templates are local-project safe;
- no app source files are created;
- token budget rules are actionable;
- stop/resume contract is explicit.
```

## Phase 3: Add System Skills

Future branch suggestion:

```text
feature/system-skills
```

Skills to create:

```text
goal-planner
execution-plan-manager
mcp-toolchain-manager
```

Expected outputs:

```text
goal-planner -> project/active-goals.md or Goal Contract response
execution-plan-manager -> project/active-plan.md, progress updates, stop/resume state
mcp-toolchain-manager -> project/mcp-profile.md and safe MCP/tool installation plan
```

Validation:

```text
- each skill has a narrow trigger boundary;
- each skill has `agents/openai.yaml` dependencies where useful;
- no tool installation happens without explicit approval;
- missing tool limitations are reported honestly;
- skills do not perform frontend implementation directly.
```

## Phase 4: Add Design Intelligence Layer

Future branch suggestion:

```text
feature/design-intelligence-layer
```

Skills and files:

```text
skills/frontend-design-director/SKILL.md
skills/frontend-design-director/agents/openai.yaml
skills/frontend-design-director/references/design-direction-contract.md
common/design-quality-rubric.md
common/anti-template-defaults.md
common/interface-copy-rules.md
templates/design-direction-contract.md
templates/visual-memory.md
```

Goals:

- define subject-grounded design direction before UI implementation;
- block generic AI UI defaults;
- define visual acceptance criteria;
- integrate screenshot critique and visual memory.

Validation:

```text
- design skill does not implement code by default;
- design direction contract is concrete;
- anti-template defaults are not absolute style bans;
- visual memory remains local-only when project-specific.
```

## Phase 5: Add Frontend Architecture And Greenfield Skills

Future branch suggestion:

```text
feature/frontend-architecture-greenfield
```

Skills:

```text
greenfield-project-builder
frontend-architecture-planner
```

Goals:

- support starting projects from scratch without dependency inflation;
- support architecture planning in existing projects;
- define state ownership, routing, styling, data fetching, and verification strategy;
- require approval before scaffolding or package installation.

Validation:

```text
- greenfield skill produces plan before scaffold;
- architecture planner stops at plan unless implementation is requested;
- official docs and local project facts are used before framework-specific claims;
- architecture layers are justified by user goal and project scale.
```

## Phase 6: Add Debugging And Refactor Skills

Future branch suggestion:

```text
feature/debug-refactor-skills
```

Skills:

```text
frontend-bugfix-debugger
frontend-refactor-surgeon
```

Goals:

- debug from evidence;
- reproduce or record symptoms;
- fix the smallest cause;
- preserve behavior during refactors;
- verify using the same failing check or behavior contract.

Validation:

```text
- debugger does not rewrite unrelated code;
- refactor skill does not change behavior without explicit approval;
- verification is tied to the original symptom or behavior contract;
- UI changes trigger visual QA when applicable.
```

## Phase 7: Expand Quality And Anti-Slop Review

Future branch suggestion:

```text
feature/frontend-quality-reviewer
```

Skill:

```text
frontend-quality-reviewer
```

Goals:

- detect AI slop in architecture, code, UI, verification, security, and performance;
- provide pass / pass with concerns / fail verdict;
- distinguish required fixes from optional improvements;
- prevent claims without evidence.

Validation:

```text
- review output includes evidence;
- review does not become a broad rewrite;
- review respects project conventions;
- security findings use OWASP or official framework/platform docs when possible.
```

## Phase 8: Integrate Existing Screenshot Pipeline

Future branch suggestion:

```text
feature/screenshot-pipeline-integration
```

Goals:

- keep `design-screenshot-spec`;
- keep `frontend-layout-implementer`;
- keep `frontend-visual-qa`;
- integrate them with goal planning, execution planning, design direction, quality review, and project memory.

Validation:

```text
- screenshot-to-code flow still works;
- visual QA requires rendered evidence unless blocked;
- implementation does not happen before spec or design direction when needed;
- project overlays are used before broad scanning.
```

## Phase 9: Package For Distribution

Future branch suggestion:

```text
release/plugin-packaging
```

Goals:

- prepare plugin packaging;
- add installation instructions;
- add examples;
- add validation scripts;
- add demo workflows;
- decide public/private release model.

Candidate files:

```text
plugin.json
examples/**
scripts/validate_skill_pack.py
CHANGELOG.md
README.md updates
```

Validation:

```text
- install instructions are short;
- examples are realistic;
- skill descriptions fit context budget;
- plugin does not bundle local-only project facts;
- no non-English reusable instructions are introduced.
```

## Skill Work Order

Recommended order:

```text
1. goal-planner
2. execution-plan-manager
3. mcp-toolchain-manager
4. frontend-design-director
5. frontend-architecture-planner
6. greenfield-project-builder
7. frontend-bugfix-debugger
8. frontend-refactor-surgeon
9. frontend-quality-reviewer
10. project-context-adapter integration
11. screenshot pipeline integration
12. plugin packaging
```

## Definition Of Done For Each Future Skill

A skill is done when:

```text
- `SKILL.md` has concise name and trigger-oriented description.
- Required sections are present.
- `agents/openai.yaml` is aligned with the skill.
- Required context is minimal.
- Tool contract is explicit.
- Workflow is small-slice friendly.
- Output contract is testable.
- Validation gates are actionable.
- Trigger evals include should-trigger and should-not-trigger examples.
- References are linked and not bulk-required.
- No host-project facts are embedded.
- No non-English reusable instructions are present.
```

## Current Stop Point

This branch should stop after adding the architecture documents.

Next exact step after review:

```text
Review the architecture with the user.
Choose the first skill to implement.
Start a new branch for that single skill.
```
