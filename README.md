# WebDev Agent Kit

A project-local operating kit for frontend coding agents.

WebDev Agent Kit helps AI coding agents plan, implement, debug, refactor, review, and visually verify frontend work without broad rewrites, unapproved packages, fake verification, or generic UI output.

Built for frontend projects that use React, Next.js, TypeScript, CSS Modules, Redux, TanStack, and Axios.

Use it when you want your coding agent to:

- understand the current frontend project before changing it;
- choose the right workflow for the task;
- keep small tasks small;
- avoid unapproved packages, tooling changes, and broad rewrites;
- verify changes with real evidence;
- preserve project-specific conventions across repeated work.

WebDev Agent Kit is not a UI library, component library, starter template, scaffolder, or test framework. It is a local instruction system that gives coding agents a safer operating model for frontend development.

## Demo

User prompt:

```text
The dashboard route renders blank on mobile.
Reproduce the symptom, fix the smallest cause, and run the relevant existing verification.
```

WebDev Agent Kit routes it as:

```text
frontend-bugfix-debugger
-> frontend-linter-manager when lint exists
-> frontend-visual-qa when rendered UI changed
-> frontend-quality-reviewer when review is requested or risk is high
```

Expected final report:

```text
Changed: files or surfaces touched
Why: root cause or implementation rationale
Verified: exact command, rendered check, or blocked check
Risks: unresolved or out-of-scope issues
Next: one useful follow-up, only when needed
```

The goal is compact evidence, not process theater. The agent should explain what changed, why it changed, how it was verified, what remains risky, and what the next useful step is when there is one.

## Quick Start

### 1. Install the kit into your frontend project

From the host project root, copy the kit into `.agents/`:

```bash
mkdir -p .agents
cp -R /path/to/webdev-agent-kit/. .agents/
```

### 2. Add a root `AGENTS.md` pointer

If your project does not already have a root `AGENTS.md`, create one:

```md
# AGENTS.md

Use the project-local agent policy in `.agents/AGENTS.md`.
```

Keep the full policy inside `.agents/AGENTS.md`. The root file should stay small and should not mirror the full bundled policy.

### 3. Ask the agent to adapt

```text
адаптируйся
```

or in English:

```text
Adapt this .agents bundle to the current frontend project.
```

Expected onboarding result:

- the agent reads the host project shape;
- detects whether the project fits the target stack;
- creates or refreshes local-only `.agents/project/**` overlays when approved;
- records stack, architecture, styling, verification, MCP/tool, and path-index facts;
- does not create app source files, install packages, or change runtime code during onboarding.

### 4. Give the agent a product-level task

```text
Implement this approved Design Implementation Spec in the pricing page.
Reuse existing CSS Modules and do not install packages.
Verify desktop and 375px mobile layout.
```

The agent should route the task through `.agents/AGENTS.md`, select the right workflow level, load only the matching skill package, and report evidence.

## Main Use Cases

### 1. Screenshot to frontend implementation

Turn screenshots, exported assets, copied inspect values, and written notes into an implementation-ready frontend spec and then into project-native code.

<!-- Add project walkthrough video, GIF, or screenshot here. -->

Best for:

- landing pages;
- pricing pages;
- dashboards;
- static product pages;
- redesign implementation;
- screenshot-derived UI work without live Figma inspection.

### 2. Evidence-first bug fixing

Make the agent reproduce the symptom, identify the smallest cause, fix the smallest safe scope, and rerun the relevant check.

<!-- Add project walkthrough video, GIF, or screenshot here. -->

Useful prompt:

```text
The settings page crashes after clicking Save.
Reproduce it, identify the smallest cause, fix it, and rerun the relevant check.
```

### 3. Safe frontend refactoring

Split components, remove duplication, simplify props, tighten TypeScript boundaries, and preserve behavior.

<!-- Add project walkthrough video, GIF, or screenshot here. -->

Useful prompt:

```text
Refactor this settings panel into smaller components without changing behavior.
Preserve public props and rendered output.
```

### 4. Pre-merge frontend review

Review frontend work for correctness, TypeScript safety, accessibility, performance, architecture fit, UX risks, and verification honesty.

<!-- Add project walkthrough video, GIF, or screenshot here. -->

Useful prompt:

```text
Review this frontend change before merge.
Check correctness, TypeScript safety, accessibility, performance, architecture, and verification honesty.
Do not apply fixes.
```

### 5. Rendered visual QA

Check desktop, tablet, and mobile viewports with rendered evidence instead of source-only guessing.

<!-- Add project walkthrough video, GIF, or screenshot here. -->

Useful prompt:

```text
Verify the implemented page against these screenshots at desktop, tablet, and 375px mobile.
Report visual mismatches with viewport evidence.
```

### 6. Project onboarding and context caching

Let the agent inspect a frontend project once and store local-only project facts in `.agents/project/**`, so future tasks can use compact factual context instead of repeated broad scans.

<!-- Add project walkthrough video, GIF, or screenshot here. -->

Useful prompt:

```text
адаптируйся
```

### 7. Greenfield frontend planning

Plan the first version of a new React or Next.js project before scaffolding anything.

<!-- Add project walkthrough video, GIF, or screenshot here. -->

Useful prompt:

```text
Plan the first version of a new Next.js app for this product idea.
Do not scaffold yet.
```

## How It Works

```text
user prompt
-> AGENTS.md classifies the task
-> workflow level is selected
-> matching skill package is loaded
-> project overlays provide local project facts
-> agent executes the smallest approved scope
-> verification runs against existing project evidence
-> final report explains changes, risks, and blockers
```

The kit uses progressive disclosure. The agent does not read every rule for every task. It starts from `AGENTS.md`, selects the relevant workflow, then loads only the skill, project overlays, common rules, and references needed for the current task.

### Workflow levels

| Level | Use for | Behavior |
| --- | --- | --- |
| Fast Lookup | Locating a file, answering a narrow repo question, checking one rule | No heavy planning. Read only enough to answer. |
| Lightweight Workflow | One small bug, typo, styling tweak, obvious type error, direct local edit | Keep the task small. No durable plan unless it escalates. |
| Standard Workflow | Multi-file feature, meaningful bugfix, refactor, UI implementation, review | Use selected skills, relevant overlays, and verification. |
| Deep Workflow | Onboarding, greenfield planning, broad redesign, repeated failure, resumable work | Use goal contracts, execution plans, loop contracts, and local-only memory when useful. |

## Guardrails

WebDev Agent Kit is strict by design. It is meant to control coding agents, not merely advise them.

The agent must ask for approval before:

- installing packages;
- adding UI libraries;
- adding state, data, form, styling, animation, chart, icon, testing, or build tooling;
- changing package manager, scripts, bundler, monorepo tooling, or framework;
- creating testing infrastructure;
- changing auth persistence, session behavior, or data mutation flow;
- scaffolding a new app;
- touching production systems, secrets, or production data;
- performing broad rewrites outside the requested scope.

The kit also prevents common frontend-agent failure modes:

- broad rewrites from narrow requests;
- unnecessary planning for tiny fixes;
- fake verification claims;
- generic SaaS UI defaults;
- decorative dashboards with fake metrics;
- unapproved Figma MCP usage;
- package installation as a first resort;
- moving server communication, domain workflow, or data processing into Redux by default.

## Supported Scope

### Best fit

WebDev Agent Kit is optimized for frontend projects using:

- React;
- Next.js;
- TypeScript;
- CSS Modules;
- Redux;
- TanStack Query or TanStack Router;
- Axios.

Stack-specific implementation and architecture skills are strict about this scope. They should not pretend to support unrelated frameworks.

### Also useful for

Some workflows are framework-agnostic and can help with:

- project onboarding;
- project context refresh;
- design intake;
- screenshot-to-spec work;
- visual direction;
- rendered visual QA;
- frontend quality review;
- lint verification;
- MCP/tool capability detection;
- planning and execution contracts;
- skill authoring and bundle maintenance.

These workflows can still apply to Astro, Vue, Svelte, static HTML/CSS, or another frontend stack when the task does not depend on React/Next-specific implementation rules.

### Not intended for

WebDev Agent Kit is not:

- a UI library;
- a component library;
- a starter template;
- a scaffolder;
- a test framework;
- a framework generator;
- a backend framework;
- a production access tool;
- a replacement for project-specific architecture;
- a live Figma MCP workflow by default.

It does not:

- install packages automatically;
- install MCP servers automatically;
- create testing infrastructure by default;
- create app source files during onboarding;
- generate a full application from a vague idea without approval gates;
- migrate routers, state layers, styling systems, build tools, or frameworks by default;
- access production systems, secrets, or production data.

## Installation

Install the kit inside a host frontend repository as `.agents/`.

Recommended project shape:

```text
your-frontend-project/
├── AGENTS.md
├── .agents/
│   ├── AGENTS.md
│   ├── README.md
│   ├── bundle-manifest.json
│   ├── common/
│   ├── examples/
│   ├── skills/
│   ├── templates/
│   └── project/              # local-only overlays, created during onboarding
├── package.json
└── src/ or app/
```

### Option A: Use a release artifact

Recommended for normal usage after versioned releases are published.

Download the Codex or Claude target from GitHub Releases and copy it into your project as `.agents/`.

Release artifacts are built as:

```text
webdev-agent-kit-codex-<version>.tar.gz
webdev-agent-kit-claude-<version>.tar.gz
SHA256SUMS
```

### Option B: Copy the source bundle

Best for local experimentation or active kit development.

From the host project root:

```bash
mkdir -p .agents
cp -R /path/to/webdev-agent-kit/. .agents/
```

Then create a small root `AGENTS.md` pointer if the project does not already have one:

```md
# AGENTS.md

Use the project-local agent policy in `.agents/AGENTS.md`.
```

### Option C: Track it as a nested checkout or submodule

Best when you want to update the kit independently from the host app.

Keep the kit as a nested checkout or submodule under `.agents/`. The host app should still treat `.agents/AGENTS.md` as the canonical policy for agent behavior.

### After installation

Run onboarding through the agent:

```text
адаптируйся
```

Review the proposed `.agents/project/**` overlays before accepting durable project facts. The overlays are local-only and should not be published upstream with the reusable kit.

## Prompt Recipes

### Adapt the kit to a project

```text
адаптируйся
```

or:

```text
Adapt this .agents bundle to the current frontend project.
```

### Implement an approved UI spec

```text
Implement this approved Design Implementation Spec in the pricing page.
Reuse existing components and CSS Modules. Do not install packages.
```

### Convert screenshots into an implementation spec

```text
Use these screenshots and copied inspect notes to write a Design Implementation Spec.
Do not implement the page yet.
```

### Fix a frontend bug

```text
The settings page crashes after clicking Save.
Reproduce it, identify the smallest cause, fix it, and rerun the relevant check.
```

### Refactor safely

```text
Refactor this settings panel into smaller components without changing behavior.
Preserve public props and rendered output.
```

### Review before merge

```text
Review this frontend change before merge.
Check correctness, TypeScript safety, accessibility, performance, architecture, and verification honesty.
Do not apply fixes.
```

### Run rendered visual QA

```text
Verify the implemented page against these screenshots at desktop, tablet, and 375px mobile.
Report visual mismatches with viewport evidence.
```

### Check MCP/tooling gaps

```text
Check which MCP tools are missing for rendered visual QA.
Report the official install sources. Do not install anything yet.
```

### Plan a new frontend project

```text
Plan the first version of a new Next.js app for this product idea.
Do not scaffold yet.
```

## Architecture

### Source model

| Layer | Path | Purpose |
| --- | --- | --- |
| Runtime policy | `AGENTS.md` | Canonical routing, workflow levels, global rules, and source-of-truth model. |
| Skill packages | `skills/**` | Executable workflows selected by user intent. |
| Common rules | `common/**` | Reusable policies, boundaries, anti-patterns, verification rules, UX gates, and token economy rules. |
| Templates | `templates/**` | Optional durable artifacts such as goal contracts, execution plans, loop contracts, visual memory, and progress logs. |
| Examples | `examples/**` | Human-readable example prompts and expected skill chains. |
| Project overlays | `project/**` | Local-only host-project facts. These are ignored by the reusable bundle and should not be published. |
| Distribution output | `dist/**` | Generated release output. Do not patch it directly. |
| README | `README.md` | Human-facing guide. Not runtime policy. |

### Runtime flow

```text
classify prompt
-> choose workflow level
-> read minimum authoritative context
-> select one or more skills
-> plan the smallest useful slice
-> execute only approved scope
-> verify with the smallest relevant existing check
-> report evidence and blockers
```

### Skill map

| User need | Primary skill | Notes |
| --- | --- | --- |
| Adapt the kit to a project | `project-onboarding-adapter` | Creates or refreshes local-only project overlays when approved. |
| Refresh stale project context | `project-context-adapter` | Updates only affected `.agents/project/**` facts. |
| Define a goal before work | `goal-planner` | Standard/deep work only. Not for tiny fixes. |
| Split work into slices | `execution-plan-manager` | Adds context budget, verification per slice, stop/resume state. |
| Plan bounded iteration | `loop-workflow-planner` | Required for measurable retry loops and independent review contracts. |
| Convert screenshots into spec | `design-screenshot-spec` | Screenshot/inspect/assets only. No live Figma workflow. |
| Ground design choices | `frontend-design-intelligence` | Product category, page pattern, design dials, anti-patterns. |
| Define visual direction | `frontend-design-director` | Design Direction Contract before implementation. |
| Plan frontend architecture | `frontend-architecture-planner` | React/Next target-stack architecture decisions. |
| Implement approved UI spec | `frontend-layout-implementer` | React/Next implementation with existing project conventions. |
| Fix frontend defects | `frontend-bugfix-debugger` | Evidence-first, one hypothesis, smallest fix. |
| Refactor safely | `frontend-refactor-surgeon` | Behavior-preserving refactors only. |
| Run lint verification | `frontend-linter-manager` | Uses existing lint command; no setup without approval. |
| Verify rendered UI | `frontend-visual-qa` | Rendered evidence only when visual QA is in scope. |
| Review frontend quality | `frontend-quality-reviewer` | Evidence-backed verdict and severity labels. |
| Manage MCP/tool capability | `mcp-toolchain-manager` | Missing tools, official sources, approval gates. |
| Maintain the kit | `agent-rules-skill-author` | Skills, rules, manifests, README, validators. |
| Plan new frontend project | `greenfield-project-builder` | Deep workflow; approval gates before scaffolding. |

### Release targets

WebDev Agent Kit builds portable targets for:

- Codex;
- Claude.

Generated targets are built into `dist/**` and packaged as GitHub Release artifacts when a version tag is published.

The release workflow validates schemas, source bundle, skill evals, generated Codex target, generated Claude target, and excluded-path rules before publishing artifacts.

## Maintenance

### Validate the source bundle

```bash
python scripts/validate_source_bundle.py
```

### Build portable targets

```bash
python scripts/build_skill_targets.py
```

### Validate the full skill pack

```bash
python scripts/validate_skill_pack.py
```

### Release

Push a version tag:

```bash
git tag v0.1.0
git push origin v0.1.0
```

The release workflow builds and publishes portable Codex and Claude targets.

### Maintenance checklist

When adding, renaming, or deleting skills:

- update `skills/<skill>/SKILL.md`;
- update `skills/<skill>/agents/openai.yaml`;
- update references under `skills/<skill>/references/**` when needed;
- update `bundle-manifest.json`;
- update `.codex-plugin/plugin.json` when native plugin metadata changes;
- update this README when user-facing workflow, installation, or skill lists change;
- run the local skill validator for changed skill packages when available;
- check for stale skill names, stale paths, and prohibited Figma routing.

## Contributing

Contributions should keep README, `AGENTS.md`, `bundle-manifest.json`, `.codex-plugin/plugin.json`, skills, references, validators, and release targets aligned.

Do not publish host-project facts from `.agents/project/**` into the reusable bundle.

Do not patch generated `dist/**` output directly. Update source files, then regenerate distribution output through the repository release process.

## License

Apache-2.0. See [LICENSE](LICENSE).
