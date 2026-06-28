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
7. Frontend skill landscape integration notes
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
- Preserve the original concept: a disciplined frontend engineering skill pack with goal planning, project memory, MCP/tooling discipline, design intelligence, small-slice execution, and AI-slop filtering.
- Do not turn this pack into a marketplace mirror or a collection of unrelated third-party skills.

## Hard Exclusions

The `awesome-frontend-skills` landscape contains useful categories, but two categories are explicitly excluded from the WebDev Assistant plan.

Do not create, import, recommend, or package dedicated skills for:

```text
UI component libraries
Testing skills
```

This means the implementation plan must not add skills for shadcn/ui, Tailwind UI, component-library guides, Playwright test generation, E2E testing patterns, unit testing, component testing, visual regression testing, or similar testing-library workflows.

Allowed related behavior:

```text
- rendered UI verification as part of frontend-visual-qa;
- browser evidence for visual review;
- local project verification commands already present in the host project;
- code-quality checks that do not create testing workflows;
- framework-specific implementation guidance from official docs.
```

## Frontend Skill Landscape Integration Notes

The `awesome-frontend-skills` repository is useful as a landscape map, not as a source to copy directly. It shows that the frontend skill ecosystem clusters around frameworks, design, animation, code quality, TypeScript, build tools, auth, data, mobile, and skill management.

What to take:

```text
- installation UX patterns;
- framework-aware adapter strategy;
- official-source preference;
- code-quality severity model;
- TypeScript type-safety discipline;
- build-tool and monorepo awareness;
- auth/data integration boundaries for frontend work;
- optional vertical adapters for video or mobile only after core web skills are stable.
```

What not to take:

```text
- UI component library skills;
- testing skills;
- broad catalog duplication;
- stack-specific dependency inflation;
- package installation defaults;
- skills that bypass our goal-plan-checkpoint operating model.
```

## Landscape-Informed Additions To The Plan

### Installation UX

The pack should eventually provide installation documentation similar in clarity to skill directories that support:

```text
install one skill
list skills in the pack
install for specific agents
install the complete pack
```

This belongs in the packaging phase, not in early skill implementation.

### Framework Adapter Strategy

Do not create one giant framework skill. Create a shared framework-adaptation policy first, then add framework-specific references only when needed.

Target common files:

```text
common/framework-adaptation-policy.md
common/framework-source-map.md
project/docs-profile.md
project/stack-profile.md
```

Frameworks to support by policy:

```text
React
Next.js
Vue
Nuxt
Svelte / SvelteKit
Angular
Remix / React Router
TanStack Start / Router / Query
Vite
Astro when detected in a host project
```

Rules:

- prefer local project conventions before generic framework rules;
- prefer official framework docs before community advice;
- load only the detected framework reference;
- do not install framework packages as part of guidance;
- do not introduce a framework migration unless explicitly requested.

### State, Routing, Data, And Forms Boundaries

Take the category idea from state-management, routing, data-fetching, HTTP, and forms skills, but express it as frontend architecture boundaries rather than separate dependency-heavy skills.

Target files:

```text
common/state-ownership-rules.md
common/routing-boundary-rules.md
common/data-fetching-boundary-rules.md
common/form-boundary-rules.md
project/state-management-profile.md
project/data-fetching-profile.md
```

Rules:

- local UI state stays local by default;
- shared state requires an explicit owner and reason;
- derived state should not be stored unless the project convention requires it;
- routing patterns follow the detected router;
- data fetching follows the existing project layer;
- form handling follows the existing project convention;
- do not add state, data, or form libraries without approval.

### Code Quality Severity Model

Add a review model inspired by code-review skills, but keep it aligned with WebDev Assistant's anti-slop goals.

Target future file:

```text
common/review-severity-model.md
```

Severity labels:

```text
blocking
high
medium
low
nit
praise
```

Review output must distinguish:

```text
required fixes
optional improvements
observations
praise
unknowns
```

Rules:

- no broad rewrite from review findings;
- every blocking/high issue needs evidence;
- security findings require source-backed reasoning;
- visual findings require rendered evidence when available;
- architecture findings must cite local project conventions or official docs.

### TypeScript Discipline

Take the TypeScript category as a signal that type safety deserves a dedicated common rule set, not a standalone broad skill at first.

Target future file:

```text
common/typescript-discipline.md
```

Rules:

- preserve project TypeScript strictness;
- avoid `any` unless the project already uses it and no safe narrowing is available;
- prefer narrowing over casts;
- avoid forced casts that hide design errors;
- type component props explicitly;
- keep public types stable during refactors;
- align with official TypeScript docs and local tsconfig.

### Build Tool And Monorepo Awareness

Take build-tool skills as a signal that the pack needs build-profile awareness.

Target files:

```text
common/build-tool-boundary-rules.md
project/build-profile.md
project/workspace-profile.md
```

Supported awareness:

```text
Vite
Next.js build pipeline
Nuxt build pipeline
SvelteKit build pipeline
Angular CLI
Turborepo
Nx
pnpm workspaces
npm/yarn/bun workspaces
VitePress when detected
```

Rules:

- inspect the project before choosing commands;
- do not change build tooling without approval;
- do not add monorepo tooling unless the project already uses it or the user explicitly asks;
- cache build and workspace facts in project overlays;
- use build information to choose verification commands and affected paths.

### Auth And Data Integration Boundaries

Auth and database categories are relevant only as frontend integration boundaries. They must not turn WebDev Assistant into a backend, ORM, or database skill pack.

Target future file:

```text
common/frontend-integration-boundaries.md
```

Rules:

- support frontend integration with existing auth/data layers;
- follow existing project SDKs and official provider docs;
- do not create backend schemas, RLS policies, migrations, or database setup unless the user explicitly changes the scope;
- do not handle secrets in client code;
- ask for approval before changing auth flow or persistence behavior.

### Animation And Motion

Take only the motion discipline, not full animation-library specialization.

Target future file:

```text
common/motion-rules.md
```

Rules:

- use motion only when it clarifies state, hierarchy, transition, or subject atmosphere;
- prefer CSS-first motion when sufficient;
- prefer transform and opacity for lightweight UI motion;
- respect reduced motion;
- do not add animation libraries without approval;
- do not add motion to hide weak layout or generic content.

### Skill Management And Packaging

The skill ecosystem includes skill managers and package-based discovery. Use this as a packaging requirement later.

Packaging goals:

```text
- document one-skill install;
- document full-pack install;
- document agent-targeted install;
- document how to list available skills;
- document how to remove or update the pack;
- keep package installation optional until release phase.
```

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
- frontend skill landscape notes are integrated without adding excluded categories;
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
- avoid creating new skills until the operating model is agreed;
- add the hard exclusions for UI component libraries and testing skills to the reusable policy layer.

Candidate changes:

```text
AGENTS.md
README.md
SUMMARY.md
common/approved-patterns.md
common/anti-patterns.md
common/frontend-scope-boundaries.md
```

Validation:

```text
- existing skill names still route correctly;
- screenshot-to-frontend workflow remains intact;
- no local-only project facts leak into publishable docs;
- no non-English reusable instructions are introduced;
- no UI component library or testing skill is introduced.
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
common/motion-rules.md
templates/design-direction-contract.md
templates/visual-memory.md
```

Goals:

- define subject-grounded design direction before UI implementation;
- block generic AI UI defaults;
- define visual acceptance criteria;
- integrate screenshot critique and visual memory;
- add motion discipline without adding animation-library specialization.

Validation:

```text
- design skill does not implement code by default;
- design direction contract is concrete;
- anti-template defaults are not absolute style bans;
- visual memory remains local-only when project-specific;
- no UI component library skill or animation-library dependency is introduced.
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
- define state ownership, routing, styling, data fetching, forms, and verification strategy;
- require approval before scaffolding or package installation;
- add framework adapter policy before stack-specific references;
- add build-tool and workspace awareness without changing project tooling by default.

Candidate common files:

```text
common/framework-adaptation-policy.md
common/framework-source-map.md
common/state-ownership-rules.md
common/routing-boundary-rules.md
common/data-fetching-boundary-rules.md
common/form-boundary-rules.md
common/build-tool-boundary-rules.md
common/frontend-integration-boundaries.md
```

Candidate project overlays:

```text
project/docs-profile.md
project/build-profile.md
project/workspace-profile.md
project/state-management-profile.md
project/data-fetching-profile.md
```

Validation:

```text
- greenfield skill produces plan before scaffold;
- architecture planner stops at plan unless implementation is requested;
- official docs and local project facts are used before framework-specific claims;
- architecture layers are justified by user goal and project scale;
- no UI library, testing toolchain, or framework migration is introduced without explicit request.
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
- verify using the same failing check or behavior contract;
- apply TypeScript discipline during fixes and refactors.

Candidate common files:

```text
common/typescript-discipline.md
common/debugging-evidence-rules.md
common/refactor-safety-rules.md
```

Validation:

```text
- debugger does not rewrite unrelated code;
- refactor skill does not change behavior without explicit approval;
- verification is tied to the original symptom or behavior contract;
- UI changes trigger visual QA when applicable;
- no testing skill or test-generation workflow is introduced.
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

- detect AI slop in architecture, code, UI, verification, security, performance, TypeScript, build/workspace awareness, and frontend integration boundaries;
- provide pass / pass with concerns / fail verdict;
- distinguish required fixes from optional improvements;
- prevent claims without evidence;
- add review severity labels.

Candidate common files:

```text
common/review-severity-model.md
common/typescript-discipline.md
common/security-review-rules.md
common/performance-review-rules.md
common/build-tool-boundary-rules.md
```

Validation:

```text
- review output includes evidence;
- review does not become a broad rewrite;
- review respects project conventions;
- security findings use OWASP or official framework/platform docs when possible;
- severity labels are applied consistently;
- no UI component library or testing category is introduced.
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
- project overlays are used before broad scanning;
- rendered verification remains QA evidence and does not become a testing skill.
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
- decide public/private release model;
- document installation UX inspired by frontend skill directories without copying excluded categories.

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
- no non-English reusable instructions are introduced;
- no UI component library or testing skill is packaged.
```

## Deferred Optional Verticals

The landscape includes video, mobile, auth, and database categories. These should not be part of the initial concept.

Deferred verticals:

```text
frontend-video-adapter
mobile-frontend-adapter
frontend-auth-integration-adapter
frontend-data-integration-adapter
```

Rules:

- create only after the core web skill pack is stable;
- create only if there is repeated real demand;
- keep them frontend-boundary focused;
- require official docs and explicit user scope;
- never turn the pack into backend, ORM, database, or mobile-generalist tooling.

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
10. framework adaptation and frontend boundary common files
11. project-context-adapter integration
12. screenshot pipeline integration
13. plugin packaging
14. deferred optional verticals only after core stabilization
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
- No UI component library or testing workflow is introduced unless a future architecture decision explicitly reverses the hard exclusion.
```

## Current Stop Point

This branch should stop after adding the architecture documents and frontend skill landscape integration notes.

Next exact step after review:

```text
Review the architecture with the user.
Choose the first skill to implement.
Start a new branch for that single skill.
```
