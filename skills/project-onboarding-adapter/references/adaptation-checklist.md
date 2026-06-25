---
id: 'agents.skills.project-onboarding-adapter.references.adaptation-checklist'
title: 'Adaptation Checklist'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'project-onboarding-adapter'
tags:
    - 'agents/skill-package'
    - 'agents/onboarding'
    - 'agents/reference'
parent:
    - '[[skills/project-onboarding-adapter/SKILL|Project Onboarding Adapter]]'
related:
    []
depends_on:
    - '[[skills/project-onboarding-adapter/SKILL|Project Onboarding Adapter]]'
---

# Adaptation Checklist

Use this checklist to build the project adaptation plan or to execute an
approved onboarding adaptation. Do not edit files while using the checklist in
Plan Mode.

## Host Root

- Confirm whether `AGENTS.md` exists at the host project root.
- If missing, plan to create it as a stable pointer to `.agents/AGENTS.md`.
- If present, check whether it mirrors `.agents/AGENTS.md`, points elsewhere,
  or contains unrelated host instructions.
- Plan to keep only the stable pointer unless the canonical policy path itself
  changes.
- During approved execution, update the host-root `AGENTS.md` only when it is
  missing, stale, or mirrors bundle policy instead of pointing to it.

## Project Shape And Stack Detection

Inspect source and config paths while excluding generated, vendor, build, cache,
and tool-output directories.

Collect:

- repository state: existing app, empty/new project, or partially initialized
  project;
- package manager and scripts;
- framework and router model;
- React version and rendering model;
- non-React frontend framework, static HTML/CSS model, or custom build model
  when present;
- TypeScript strictness and module aliases;
- app/source roots;
- route, layout, metadata, sitemap, robots, API route, and server action paths;
- component, hook, utility, content, data, and shared module paths;
- styling system, tokens, global styles, CSS Modules, Tailwind, or design
  system entry points;
- state-management layer, providers, stores, selectors, and client caches;
- validation helpers, schema libraries, route-param parsing, and public
  boundary handling;
- auth, session, secrets, environment variables, public entry points, and other
  security-sensitive surfaces;
- SEO surfaces, structured data, social preview, canonical URL, and crawlability
  implementation;
- screenshot, exported asset, copied inspect, and design-reference constraints
  when present;
- test, lint, typecheck, formatting, build, and preview commands.

Detect stack in this order:

1. Package manifests and lockfiles.
2. Framework and bundler configs.
3. TypeScript, JavaScript, lint, format, and test configs.
4. Source entrypoints and route trees.
5. Styling files, token files, and design-system imports.
6. Existing project overlays.
7. User-provided intended stack when files do not identify a stack.

If no stack can be inferred from files or user-provided intent, ask the user for
the intended frontend stack before writing stack-specific facts.

For a new or empty project, do not create app source files. Create or refresh
only the host-root pointer and local-only `project/**` overlays from known or
user-provided intended stack facts.

## Official Documentation And MCP Selection

Map the detected stack to official documentation and MCP sources:

- Use MDN for HTML, CSS, Web APIs, accessibility, and browser compatibility.
- Use `context7` for current framework, library, CLI, and tooling docs after
  resolving the library id.
- Use Browser or Playwright MCP for rendered verification when an app can run.
- Use Next Devtools MCP only when the host project is Next.js, the project
  version supports it, and the tool is available in the current session.

Never use or install Figma MCP, whiteboard, live-design inspection, Figma
canvas, Figma file creation, design-system generation, or Code Connect tooling.

## MCP Dependency Scan

Scan every `skills/*/agents/openai.yaml` and collect `dependencies.tools`.

Record:

- required tool name;
- declaring skill package;
- purpose from the dependency description;
- whether the tool is active in the current session;
- whether the tool is configured in the host Codex environment when that can be
  safely inspected;
- whether the tool is optional, required, missing, approved for installation,
  installed, skipped, or blocked;
- official install source or command when verified.

Report missing official MCP servers before installing them. Install only after
explicit user approval. Stop and ask when an official install source or command
cannot be verified.

## Overlay Plan

Plan updates for the local-only overlays:

- `project/stack-profile.md` - framework, runtime, tooling, package manager,
  TypeScript, state, validation, and verification summary.
- `project/architecture-map.md` - route tree, app/source roots, shared code,
  server/client zones, data flow, and key feature areas.
- `project/styling-profile.md` - styling system, token sources, breakpoints,
  global styles, component styles, and naming conventions.
- `project/verification-profile.md` - relevant checks, order, scope, and known
  blockers.
- `project/approved-patterns.md` - project-specific allowed patterns and local
  examples only, backed by real project code or official documentation for the
  detected stack.
- `project/anti-patterns.md` - project-specific prohibited patterns,
  exceptions, and local examples only, backed by real project code or official
  documentation for the detected stack.
- `project/mcp-profile.md` - required, available, missing, optional, approved,
  installed, and blocked MCP capabilities for current skills.
- `project/design-reference-profile.md` - screenshot, exported asset, copied
  inspect, and design-reference boundaries for the current project.
- `project/react/path-index.md` - component, hook, state, style, asset, utility,
  and client UI lookup paths.
- `project/next/path-index.md` - App Router route, layout, metadata, server,
  API, sitemap, robots, and SEO lookup paths when Next.js exists.

## Plan Output

The final Plan Mode response must tell the future implementer exactly which
files to create or update, what facts to put in each overlay, which MCP servers
are required or missing, which paths to avoid, and which verification commands
to run after implementation.

The approved execution report must list files changed, MCP scan results,
installation approvals or blockers, validation commands, and remaining unknown
facts.
