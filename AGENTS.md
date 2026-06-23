---
id: 'agents.agents'
title: 'AGENTS.md'
doc_type: 'policy'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/policy'
    - 'docs/entrypoint'
parent:
    []
related:
    - '[[SUMMARY|Agent Documentation Summary]]'
    - '[[README|webdev-assistant README]]'
    - '[[common/documentation-maintenance|Documentation Maintenance]]'
depends_on:
    []
---

# AGENTS.md

This file is the canonical policy entrypoint for the embedded `.agents/`
bundle. The host-project root `AGENTS.md` is only a stable pointer to this file,
not a synchronized copy.

## Bundle Model

- The host-root `AGENTS.md` holds only the stable pointer to
  `.agents/AGENTS.md`.
- `.agents/AGENTS.md` is the canonical publishable policy file.
- `.agents/common/**` holds reusable shared rules that may be published to the
  shared `webdev-assistant` repository.
- `.agents/project/**` holds host-repo facts, examples, overlays, and local
  addenda only.
- `.agents/skills/**` holds reusable workflows that may be published to the
  shared `webdev-assistant` repository.
- `.agents/` itself is the local checkout of the shared
  `git@github.com:ytvee-dev/webdev-assistant.git` repository.
- `.agents/project/**` is intentionally local-only inside that nested checkout
  and must never be published upstream.
- Changes inside `.agents/` do not require updating the host-root `AGENTS.md`
  unless the canonical policy path itself changes.

## Inspect First

Before implementation work:

1. Read `AGENTS.md`.
2. Read `.agents/SUMMARY.md`.
3. Load the relevant skill from `.agents/skills/`.
4. Read the relevant `.agents/common/**` docs and `.agents/project/**` overlays.
5. Read the affected source files and configs before changing anything.

Do not skip this order when the task changes code, agent policy, or bundle
structure. Select skills from the user prompt and repo context; the user does
not need to name a skill explicitly.

## Host Project Rules

- Detect project type, stack, routing model, styling system, and verification
  commands from the inspected host repository and `.agents/project/**`.
- Do not store host-project stack facts, architecture, or local examples in
  `AGENTS.md`, `.agents/common/**`, or reusable skill packages.
- Treat `.agents/project/**` as the current host-project context, not as static
  notes.
- After changing host code or documentation structure, update the relevant local
  `.agents/project/**` overlays in the same task.
- Every Markdown file in `.agents/**` must keep graph frontmatter current.
  Treat it as navigation metadata only; workflow instructions belong in the
  document body.

## Generic Workflow Rules

- Prefer MCP tools and repo-local documentation over broad guesswork whenever
  the required tool or context is available.
- For file inspection, prefer filesystem MCP tools such as `read_text_file`,
  `read_multiple_files`, `list_directory`, and `directory_tree` when they are
  available for the target path. Use shell file reads only when filesystem MCP
  access is unavailable, blocked, or when command output is the source of truth
  for the task.
- For HTML, CSS, Web APIs, HTTP, browser compatibility, and other web platform
  behavior, prefer the configured MDN MCP server `mdn` when it is available.
  If `mdn` is unavailable, use official MDN documentation before broad web
  search. Treat the MDN MCP server as experimental and verify current behavior
  against official MDN docs or MCP output.
- Prefer solutions that do not require installing new packages.
- Before proposing or installing a package, check whether it already exists in
  the host repo and get explicit user approval before installation.
- Do not interact with production systems, production data, or live production
  environments.
- Do not invent architecture, API contracts, or missing implementation details;
  narrow the search and then ask the user if the repo still does not define the
  needed fact.
- Do not modify the host repository root `README.md` unless the user explicitly
  asks for it.

## Upstream Bundle Rules

- Publishable checkout-root bundle content inside `.agents/` is limited to
  `AGENTS.md`, `SUMMARY.md`, `common/**`, `skills/**`, `README.md`, and
  `.gitignore`.
- For `.agents/` documentation git work, use branch names in the form
  `[fix|feat]-[description]`.
- Keep `description` to 1-3 lowercase kebab-case words that summarize the
  grouped documentation commits.
- Do not use numbers, timestamps, ticket ids, repo names, or placeholders such
  as `webdev`, `assistant`, or `bundle` in `.agents/` documentation branch
  names unless the word is the real subject of the change.
- When committing publishable documentation changes in `.agents/`, use
  `fix(docs): <short description>` or `feat(docs): <short description>`.
- Keep the local `.agents/` checkout on `main` by default; treat feature
  branches as push/PR transport only.
- Commit publishable documentation changes locally on `main`.
- Do not create a publication branch, push, open a PR, or report publication
  success while eligible publishable documentation changes remain uncommitted.
- After committing publishable documentation, verify that eligible publishable
  paths have no remaining staged or unstaged changes before continuing.
- Do not switch `.agents/` branches while uncommitted or unmerged changes are
  present; resolve, commit, or stop and report the exact paths first.
- Stage and commit only eligible publishable paths before creating a push
  branch.
- Never push local `main` directly to `origin`.
- Before pushing a documentation branch, run `git pull --rebase origin main`
  while on local `main`.
- After that pull, create the new `[fix|feat]-[description]` branch from local
  `main`, push it, open the PR to `main`, and then return the local checkout to
  `main`.
- Reuse the same core description in the branch name, commit subject, and PR
  title when `webdev-assistant-sync` opens a PR.
- Never publish `project/**`, old helper paths such as `upstream/**`, source
  code, or other host-project files to `webdev-assistant`.
- Do not mirror `.agents/AGENTS.md` into the host-root `AGENTS.md`; keep the
  root file as a stable pointer.
- Use `webdev-assistant-sync` for bundle sync and publication tasks.
- Do not run git publication commands from the host project repository root; run
  them only inside the nested `.agents/` git repository.

## Skill Map

- Task classification and workflow routing -> `webapp-task-protocol`
- Next.js App Router work -> `nextjs-app-router`
- React component architecture, strict TypeScript, and implementation ->
  `react-component-workflow`
- React shared state, context, Redux, selectors, and store-like hooks ->
  `react-state-workflow`
- Visual design, Figma/screenshot translation, responsive polish, and
  generative UI -> `frontend-design-workflow`
- Read-only Figma inspection, screenshots, variables, and MCP troubleshooting ->
  `figma-design-reader`
- Figma-to-code implementation in the repo -> `figma-design-to-code`
- Low-level Figma canvas mutation through `use_figma` ->
  `figma-canvas-editing`
- Full-screen and multi-section generation inside Figma ->
  `figma-screen-generation`
- Figma design system and component library building ->
  `figma-design-system-builder`
- Figma Code Connect mappings -> `figma-code-connect`
- New blank Figma or FigJam file creation -> `figma-create-file`
- Boundary validation without new dependencies -> `boundary-input-validation`
- Review pass and verification -> `frontend-review-and-fix`
- Interactive browser QA with Playwright, screenshots, and viewport checks ->
  `playwright-interactive`
- First-time host project adaptation and `.agents/project/**` planning ->
  `project-onboarding-adapter`
- Agent rules and skill authoring -> `agent-rules-skill-author`
- Human-facing `.agents/README.md` maintenance -> `readme-maintainer`
- Bundle sync and upstream publication -> `webdev-assistant-sync`
- Screenshot-based design inspection -> `screenshot-design-inspector`
- Architecture planning from user specs, with no implicit edits ->
  `architecture-from-spec`
- Source-backed technical SEO audit/fixes, webmaster setup, external content
  taxonomy, and AI-agent discoverability -> `technical-seo-app`
- Security audit/reporting -> `frontend-security-inspector`
- Refresh of `.agents/project/*` docs -> `project-context-adapter`

## Common Bundle Docs

- `.agents/common/approved-patterns.md`
- `.agents/common/anti-patterns.md`
- `.agents/common/documentation-maintenance.md`

## Local Project Overlay Docs

- `.agents/project/stack-profile.md`
- `.agents/project/architecture-map.md`
- `.agents/project/styling-profile.md`
- `.agents/project/seo-profile.md`
- `.agents/project/verification-profile.md`
- `.agents/project/approved-patterns.md`
- `.agents/project/anti-patterns.md`
- `.agents/project/figma-profile.md`
- `.agents/project/react/path-index.md`
- `.agents/project/next/path-index.md`
