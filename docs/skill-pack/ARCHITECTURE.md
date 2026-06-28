# WebDev Assistant Skill Pack Architecture

Status: draft architecture.
Scope: proposed target architecture for a future installable frontend engineering skill pack.

## Product Role

WebDev Assistant is a frontend engineering skill pack for coding agents. It helps agents understand existing frontend projects, build new projects from scratch, implement UI from screenshots and specifications, plan architecture, debug frontend bugs, refactor safely, verify rendered interfaces, manage MCP/tooling, and filter AI-generated slop.

The pack must behave like a disciplined senior frontend engineer, not like a generic code generator.

## Core Principle

The agent must not start by coding. It must first define the goal, select the smallest relevant skill, load only the context required for that skill, use source-backed guidance, execute in small verified slices, and leave a clear checkpoint after each meaningful step.

## Distribution Model

WebDev Assistant should support three install modes:

1. Repository-local install through `.agents/skills`.
2. User-level install through a user skill directory or symlink.
3. Plugin distribution for reusable installation across teams.

Direct skill folders are suitable for local authoring and repository-scoped workflows. Plugin packaging is the target format once the skill pack contains multiple stable skills, shared assets, MCP configuration, and examples.

## Architectural Layers

```text
Install Layer
Routing Layer
Agent Operating System Layer
MCP Tooling Layer
Official Documentation Layer
Project Memory Layer
Design Intelligence Layer
Frontend Engineering Skills Layer
Verification Layer
Quality And Anti-Slop Layer
Skill Pack Maintenance Layer
```

## Install Layer

The install layer must make the pack easy to use without requiring users to copy long prompts.

Target install outputs:

```text
.agents/AGENTS.md
.agents/SUMMARY.md
.agents/common/**
.agents/skills/**
.agents/templates/**
.agents/examples/**
```

Local-only runtime state must stay under:

```text
.agents/project/**
```

`project/**` must not be published as reusable instructions, because it contains host-project facts.

## Routing Layer

`AGENTS.md` is the canonical router and policy entrypoint. Its job is to classify the user request and select the smallest relevant skill.

The router must not read all skills or all references. It should read only:

1. `AGENTS.md`.
2. The selected skill's `SKILL.md`.
3. References explicitly named by the selected skill.
4. Relevant `project/**` overlays.
5. Affected source files.

## Agent Operating System Layer

The operating system layer defines how the agent works before, during, and after a task.

It includes:

- goal setting;
- execution planning;
- context budget selection;
- MCP/tool availability checks;
- official documentation routing;
- small-slice execution loops;
- verification gates;
- checkpointing;
- stop/resume behavior;
- retrospective comparison against the original goal.

This layer prevents long, unbounded work sessions and keeps large tasks resumable.

## MCP Tooling Layer

The MCP tooling layer is responsible for detecting, selecting, installing, validating, and recording MCP servers and tools.

It must not install tools automatically. Missing MCP servers require:

1. Need detection.
2. Official install source verification.
3. User approval.
4. Installation.
5. Validation.
6. Recording in `project/mcp-profile.md`.

Core MCP servers for the future pack:

```text
filesystem_server
playwright
context7
mdn
openaiDeveloperDocs
```

Optional MCP servers:

```text
github
figma
browser/devtools
visual-diff
design-reference
linear/jira
docs/search
```

## Official Documentation Layer

Implementation guidance must be source-backed.

Source priority:

```text
1. Local project code and conventions
2. Official framework documentation
3. Official platform documentation
4. Official library documentation
5. Standards and specifications
6. Recognized style guides
7. Agent inference, explicitly marked as inferred
```

Default official sources:

```text
OpenAI Codex docs -> skills, plugins, AGENTS.md, MCP integration
MCP specification -> tool discovery, invocation, safety model
React docs -> component thinking, state structure, effects, accessibility-adjacent guidance
Next.js docs -> routing, rendering, data, app/pages router specifics
Vue/Nuxt docs -> Vue and Nuxt projects
Svelte/SvelteKit docs -> Svelte projects
Vite docs -> Vite projects
TypeScript docs -> typing behavior and compiler configuration
Redux docs -> store, reducers, side effects, state ownership
MDN -> HTML, CSS, Web APIs, responsive behavior, browser compatibility
W3C WAI/WCAG -> accessibility
web.dev -> performance
OWASP -> frontend security and XSS guidance
```

## Project Memory Layer

Project memory saves tokens by caching stable project facts in local-only overlays.

Target overlays:

```text
project/stack-profile.md
project/architecture-map.md
project/styling-profile.md
project/state-management-profile.md
project/data-fetching-profile.md
project/verification-profile.md
project/accessibility-profile.md
project/performance-profile.md
project/security-profile.md
project/approved-patterns.md
project/anti-patterns.md
project/path-index.md
project/mcp-profile.md
project/docs-profile.md
project/design-reference-profile.md
project/visual-memory.md
project/active-goals.md
project/active-plan.md
project/progress-log.md
project/decision-log.md
project/context-index.md
```

Rules:

- Reusable skills must not contain host-project facts.
- Host-project facts live only in `project/**`.
- Stable discoveries must be cached instead of repeatedly rediscovered.
- Large scans must update `context-index.md` or a relevant overlay.

## Design Intelligence Layer

The design layer prevents generic AI UI and supports distinctive, subject-grounded frontend design.

It includes:

- `frontend-design-director`;
- design direction contracts;
- visual identity rubric;
- anti-template defaults;
- visual memory;
- interface copy rules;
- screenshot repair loops;
- CSS specificity checks;
- motion restraint rules.

This layer is used before UI implementation when the user asks for new UI, redesign, visual polish, landing pages, dashboards, or anything that requires aesthetic judgment.

## Frontend Engineering Skills Layer

Future skill catalog:

### System Skills

```text
mcp-toolchain-manager
goal-planner
execution-plan-manager
project-onboarding-adapter
project-context-adapter
skill-pack-maintainer
```

### Frontend Skills

```text
greenfield-project-builder
frontend-design-director
design-screenshot-spec
frontend-layout-implementer
frontend-architecture-planner
frontend-bugfix-debugger
frontend-refactor-surgeon
frontend-visual-qa
frontend-quality-reviewer
```

## Skill Routing Map

```text
First use in existing project
-> project-onboarding-adapter

New project from scratch
-> goal-planner
-> execution-plan-manager
-> greenfield-project-builder
-> project-context-adapter

Large task or vague goal
-> goal-planner
-> execution-plan-manager

MCP/tooling setup or missing tool
-> mcp-toolchain-manager

Screenshot, exported asset, copied inspect value, visual reference
-> design-screenshot-spec
-> frontend-design-director when design judgment is needed
-> frontend-layout-implementer
-> frontend-visual-qa
-> frontend-quality-reviewer

New UI, redesign, visual polish, landing page, dashboard
-> frontend-design-director
-> frontend-layout-implementer
-> frontend-visual-qa
-> frontend-quality-reviewer

Feature or rendered frontend implementation
-> frontend-layout-implementer
-> frontend-visual-qa
-> frontend-quality-reviewer

Architecture, state ownership, folder structure, routing, API layer
-> frontend-architecture-planner

Bug, console error, failing build, broken UI, hydration issue
-> frontend-bugfix-debugger
-> frontend-visual-qa when rendered UI changed

Behavior-preserving code cleanup
-> frontend-refactor-surgeon
-> frontend-quality-reviewer

Review, PR audit, AI slop detection, risk analysis
-> frontend-quality-reviewer

Skill pack editing
-> skill-pack-maintainer
```

## Standard Skill Package Shape

```text
skills/<skill-name>/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/
  assets/
```

Required `SKILL.md` sections:

```text
Purpose
When To Use
When Not To Use
Required Context
Tool Contract
Workflow
Output Contract
Validation Gates
Trigger Evals
Reference Map
```

The `name` and `description` frontmatter keys must be concise and trigger-oriented. The description must front-load the most important trigger words because skill descriptions may be shortened when many skills are installed.

## Core Workflow For Any Large Task

```text
1. Intake
2. Classify
3. Create or update Goal Contract
4. Select Context Budget
5. Create or update Execution Plan
6. Check required MCP/tools
7. Execute one small slice
8. Verify the slice
9. Compare result with goal and plan
10. Update checkpoint
11. Decide next step or stop
```

## Default Pipelines

### Existing Project UI Implementation

```text
project-onboarding-adapter when overlays are missing
-> goal-planner
-> execution-plan-manager
-> frontend-design-director when visual direction is needed
-> frontend-layout-implementer
-> frontend-visual-qa
-> frontend-quality-reviewer
-> project-context-adapter when project facts changed
```

### Greenfield Project

```text
goal-planner
-> execution-plan-manager
-> greenfield-project-builder
-> frontend-architecture-planner
-> frontend-design-director when UI direction is needed
-> frontend-layout-implementer
-> frontend-visual-qa
-> frontend-quality-reviewer
-> project-context-adapter
```

### Bugfix

```text
frontend-bugfix-debugger
-> targeted evidence collection
-> minimal fix
-> same failing check
-> frontend-visual-qa when rendered UI changed
-> frontend-quality-reviewer
```

### Refactor

```text
frontend-refactor-surgeon
-> behavior contract
-> small refactor slice
-> same behavior verification
-> frontend-quality-reviewer
```

## Anti-Slop Philosophy

The pack must block work that looks productive but does not solve the user's goal.

AI slop includes:

- broad rewrites for narrow tasks;
- dependencies added without demonstrated need;
- architecture layers created for appearance;
- global state used for local UI state;
- duplicated components or tokens;
- fake design systems;
- generic SaaS UI;
- unverified claims;
- visual QA replaced by lint/build;
- hidden uncertainty;
- huge diffs without checkpoints.

## Completion Contract

A task is complete only when:

1. The original goal is restated.
2. The completed scope is named.
3. Deviations and unknowns are explicit.
4. Verification evidence is reported.
5. The plan is compared against the result.
6. The next step is clear if work remains.
