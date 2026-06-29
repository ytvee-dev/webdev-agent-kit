---
name: project-onboarding-adapter
description: Use when adapting this .agents bundle to a host frontend project, planning or executing the host-root AGENTS.md pointer, project context overlays, stack detection, official docs/MCP selection, MCP dependency audit, and frontend context cache. In Plan Mode, produce a plan only; outside Plan Mode, execute only after user approval.
---

# Project Onboarding Adapter

## Purpose

Adapt this `.agents` bundle to a host frontend project. The adapter establishes
the host-root `AGENTS.md` pointer, detects the project stack, selects official
documentation and MCP capabilities, audits MCP dependencies declared by current
skills, and writes local-only `project/**` overlays that later agents can use
without repeatedly scanning the whole repository.

In Plan Mode, produce a decision-complete plan only. Outside Plan Mode, execute
the approved adaptation without creating application source files.

## When To Use

- The user asks to adapt this bundle to a new frontend project.
- The user asks to initialize or recreate project context.
- The user asks to create or verify the host-root `AGENTS.md` pointer.
- The user asks to audit or install MCP servers required by this bundle's
  current skills.
- The user asks to cache current frontend stack, documentation, patterns,
  anti-patterns, or verification facts for later agents.

## When Not To Use

- Ordinary screenshot-to-code implementation. Use the three pipeline skills.
- Narrow `project/**` refresh after implementation. Use
  `project-context-adapter`.
- Skill authoring or bundle rule changes. Use `agent-rules-skill-author`.
- Application scaffolding, feature creation, package installation, or source
  file creation for a new frontend app.

## Required Context

1. Check the active collaboration mode and decide whether this is planning or
   approved execution.
2. Read the host-root `AGENTS.md` if it exists.
3. Read bundle-local `AGENTS.md` and `README.md`.
4. Consult `SUMMARY.md` only when the task explicitly edits, audits, or
   verifies the manual catalog.
5. Read only `common/**` files needed for the onboarding task.
6. Read every current `skills/*/SKILL.md` and `skills/*/agents/openai.yaml`.
7. Read existing `project/**` overlays.
8. Inspect host project manifests, configs, source entrypoints, routes, styles,
   assets, tests, and verification scripts without generated/vendor/build/cache
   directories.
9. Read `references/adaptation-checklist.md`.
10. Read `references/path-audit-checklist.md`.

## Tool Contract

- Use Project Context MCP when available.
- Use filesystem reads and targeted search when MCP context is unavailable.
- Use `context7` only for current framework, library, CLI, or tooling
  documentation after resolving the relevant library id.
- Use MDN MCP for HTML, CSS, Web APIs, accessibility, and browser
  compatibility facts.
- Use Browser or Playwright MCP only for rendered verification of an existing
  app, never as a substitute for stack detection.
- Do not use Figma MCP.
- Do not mutate files while Plan Mode is active.
- Do not install MCP servers unless the user explicitly approves installation
  after the missing official MCP list is reported.
- Do not install broad, unofficial, design-tool, Figma, whiteboard, or
  live-design MCP servers as fallbacks.

## Mode Gate

Before reading the whole project or changing files, check the active
collaboration mode and user request.

- In Plan Mode, inspect only enough to produce a decision-complete adaptation
  plan. Do not create files, edit overlays, install MCP servers, or run
  adaptation commands.
- Outside Plan Mode, execute only when the user explicitly asks to implement,
  run, apply, or perform the adaptation. If the request is only exploratory,
  return an audit or plan instead.
- During execution, edit only the host-root `AGENTS.md` pointer and
  `.agents/project/**` overlays unless the user also asks for reusable bundle
  docs or skills to be updated.
- For a new or empty project, create or refresh only the host-root pointer and
  `.agents/project/**` overlays from inferred or user-provided intended stack
  facts. Do not create app source files, framework configs, package manifests,
  routes, components, styles, tests, or build scripts.
- If no stack can be inferred from files or user-provided intent, ask for the
  intended frontend stack before writing stack-specific facts.

## Workflow

Use this workflow for planning and approved execution:

1. Read the host-root `AGENTS.md`, bundle-local `AGENTS.md`, and `README.md`.
2. Consult `SUMMARY.md` only when the task explicitly edits, audits, or
   verifies the manual catalog.
3. Read only `common/**` files needed for the onboarding task.
4. Read every current `skills/*/SKILL.md`, every present
   `skills/*/agents/openai.yaml`, and only referenced skill references needed
   for path and workflow validation.
5. Read existing `project/**` overlays.
6. Inspect the host project without generated, vendor, build, and cache
   directories such as `node_modules`, `.next`, `dist`, `coverage`, `.cache`,
   and `.playwright-mcp`.
7. Determine whether the project is existing, new/empty, or partially
   initialized.
8. Detect the stack from manifests, lockfiles, framework configs, TypeScript or
   JavaScript configs, source roots, routes, styling files, test configs, and
   entrypoints. Ask for intended stack only when no reliable stack or user
   intent is available.
9. Select documentation and MCP capabilities from official sources:
   - MDN for HTML, CSS, Web APIs, accessibility, and browser compatibility.
   - `context7` for current framework, library, CLI, and tooling docs.
   - Browser or Playwright MCP for rendered verification of an existing app.
   - Next Devtools MCP only for a Next.js project that supports it and exposes
     the tool in the current session.
10. Scan `skills/*/agents/openai.yaml`, collect `dependencies.tools`, compare
   required tools with active or configured MCP capabilities, and record
   required, available, missing, optional, install source, and approval status.
11. Use `references/adaptation-checklist.md` to collect project facts.
12. Use `references/path-audit-checklist.md` to find missing, stale, or
   template-only paths in bundle docs and skill reference maps.
13. Include graph frontmatter and Obsidian link updates for every planned or
   changed `project/**` overlay and any publishable docs whose links drifted.
14. In Plan Mode, return the complete adaptation plan and stop.
15. In approved execution mode, create or update only the approved files, then
   run the validation gates.

## Required Plan Contents

The adaptation plan must include:

- whether the host-root `AGENTS.md` exists and whether it should be created or
  replaced with the stable pointer to `.agents/AGENTS.md`;
- which `project/**` overlays should be created or updated;
- the discovered project type, stack, routing model, styling system, state
  layer, validation approach, and verification commands;
- official documentation sources and MCP servers selected for the detected
  stack;
- MCP dependencies scanned from `skills/*/agents/openai.yaml`, including
  required, optional, available, missing, approved, and not-approved entries;
- concrete path indexes to write for React/client work and Next.js App Router
  work when those surfaces exist;
- stack-specific patterns and anti-patterns to cache, with sources from real
  project code or official documentation;
- path drift findings across bundle-local `AGENTS.md`, `SUMMARY.md`,
  `README.md`, `common/**`, `skills/**`, and `project/**`;
- graph frontmatter and wikilink updates needed after adaptation, including
  `publishable: false` and `local_only: true` for `project/**`;
- explicit exclusions for generated, vendor, build, cache, and local-only
  paths;
- verification commands to run after implementation;
- a statement that `project/**` stays local-only and host-project facts
  must not be written into publishable skills, common docs, or bundle policy.

## Implementation Defaults For The Future Execution Step

When the user asks to execute the plan outside Plan Mode, the implementing
agent must:

- create or update only the host-root `AGENTS.md` pointer and `project/**`
  overlays unless the plan identifies stale publishable
  bundle links that must also be fixed;
- keep `.agents/AGENTS.md` canonical and never mirror it into the host-root
  `AGENTS.md`;
- write factual repo-specific context into `project/**`;
- create or refresh `project/mcp-profile.md` with the skill dependency scan,
  official documentation selection, missing MCP list, and installation approval
  status;
- create or refresh `project/design-reference-profile.md` for screenshot and
  exported-design-source boundaries without implying live design-tool access;
- create or update graph frontmatter and `.agents`-relative Obsidian wikilinks
  for every changed Markdown overlay;
- keep reusable instructions in `common/**` and `skills/**`;
- avoid generated, vendor, build, cache, production, and secret-bearing paths;
- avoid creating app source files for new or empty projects;
- install only explicitly approved missing MCP servers whose official install
  source has been verified;
- run the verification commands listed in the plan.

## Validation Gates

Before finishing the Plan Mode response, verify:

- the response is a plan only and contains no applied changes;
- root pointer handling is explicit;
- every expected `project/**` overlay is accounted for;
- stack detection source and confidence are explicit;
- official documentation and MCP selection are explicit;
- missing MCP installation is reported but not performed without approval;
- planned overlays include graph frontmatter and current links to relevant
  context skills;
- path audit results distinguish real missing paths from documented templates;
- no host-project facts are planned for publishable bundle docs;
- the plan names relevant verification commands or states why none were found.

Before finishing approved execution, verify:

- the host-root `AGENTS.md` is either unchanged because it is already a stable
  pointer or updated to point to `.agents/AGENTS.md`;
- every changed `project/**` overlay has graph frontmatter with
  `publishable: false` and `local_only: true`;
- `project/mcp-profile.md` matches the current `skills/*/agents/openai.yaml`
  dependency scan;
- `project/design-reference-profile.md` exists and no stale design-source
  overlay reference remains;
- no application source files were created for a new or empty project;
- all changed rules and overlays are English-only;
- skill validation, stale-name search, docs/path consistency checks, and
  formatting checks were run or a blocker is reported.

## Output Contract

Return a plan containing:

- host-root `AGENTS.md` pointer action;
- project type and frontend stack facts;
- official docs and MCP selection;
- MCP dependency scan and installation approval status;
- overlays to create or update;
- path indexes to create or update;
- stack-specific approved patterns and anti-patterns to cache;
- stale bundle path findings;
- excluded paths;
- verification commands for the later execution step;
- confirmation that `project/**` remains local-only.

After approved execution, report:

- files created or updated;
- stack facts and docs/MCP choices cached;
- MCP servers scanned, missing, approved, installed, or skipped;
- validation commands run and results;
- any remaining unknown project facts or blocked MCP installations.

## Trigger Evals

Should trigger:

- "Adapt this .agents bundle to my project."
- "Initialize project context and create the root AGENTS.md pointer."
- "Plan onboarding for this frontend repo."
- "Scan the skills and install the MCP servers they require."
- "Cache the current frontend stack for later agents."

Should not trigger:

- "Implement this visual spec."
- "Refresh project overlays after this component change."
- "Create a new skill package."
- "Scaffold a new React app."

## Reference Map

- `references/adaptation-checklist.md`
- `references/path-audit-checklist.md`
