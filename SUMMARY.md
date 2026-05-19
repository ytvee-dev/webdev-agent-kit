---
id: 'agents.summary'
title: 'Agent Documentation Summary'
doc_type: 'summary'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/summary'
    - 'docs/navigation'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[README|webdev-assistant README]]'
depends_on:
    []
---

# Agent Documentation Summary

Purpose: explain the current `.agents/` tree, reading order, and the split
between upstream-managed bundle docs, reusable workflows, and host-project
overlays.

All Markdown files under `.agents/` carry graph frontmatter for Obsidian-style
navigation. Treat `.agents` as the vault root when reading `parent`, `related`,
and `depends_on` wikilinks.

Graph frontmatter is required metadata, not a replacement for document body
instructions. New or changed Markdown files must update frontmatter links in
the same task.

## Reading order

1. Start with `AGENTS.md`.
2. For implementation work, load `.agents/skills/webapp-task-protocol/SKILL.md`
   first, then follow its skill chain.
3. For documentation or agent-rules work, read this file, then
   `.agents/common/documentation-maintenance.md`, then
   `.agents/skills/agent-rules-skill-author/SKILL.md`.
4. Read only the overlays and skill references relevant to the current task.
5. Finish implementation work with
   `.agents/skills/frontend-review-and-fix/SKILL.md`.

## Common bundle docs

- `common/approved-patterns.md` - bundle-wide reusable implementation patterns
- `common/anti-patterns.md` - bundle-wide prohibited directions
- `common/documentation-maintenance.md` - rules for changing publishable bundle
  docs

## Project overlays

- `project/stack-profile.md` - host-project framework, runtime, tooling, and
  state-management snapshot
- `project/architecture-map.md` - host-project route tree, shared code
  locations, and client/server structure
- `project/styling-profile.md` - host-project styling conventions and tokens
- `project/verification-profile.md` - host-project verification order and scope
- `project/approved-patterns.md` - host-project approved-pattern addenda and
  examples
- `project/anti-patterns.md` - host-project anti-pattern addenda and exceptions
- `project/figma-profile.md` - host-project design-to-code constraints
- `project/react/path-index.md` - host-project lookup index for component and
  client work
- `project/next/path-index.md` - host-project lookup index for App Router work

## Skill packages

- `skills/webapp-task-protocol` - classify the task and choose the skill chain
- `skills/nextjs-app-router` - App Router routes, layouts, metadata, and
  boundaries
- `skills/react-component-workflow` - component structure, props, state, and
  hooks
- `skills/redux-state-workflow` - Redux, selectors, typed store hooks, and
  shared state
- `skills/frontend-typescript-rules` - strict typing and safe refactors
- `skills/boundary-input-validation` - boundary parsing without new
  dependencies
- `skills/frontend-review-and-fix` - final review, regression checks, and
  verification
- `skills/project-onboarding-adapter` - Plan Mode-only first-time host project
  adaptation planning, root `AGENTS.md` pointer setup, `.agents/project/**`
  overlay planning, and bundle path audit
- `skills/project-context-adapter` - refresh repo overlays after structure
  drift
- `skills/agent-rules-skill-author` - maintain `.agents/` and repo-local agent
  policy, including `.agents`-first skill authoring, native Codex skill
  contract boundaries, `openai.yaml`, local scaffolding and validation
  scripts, trigger precision, source-backed workflows, progressive disclosure,
  and validation
- `skills/readme-maintainer` - audit agent documentation and keep
  `.agents/README.md` structured, accurate, and user-facing
- `skills/webdev-assistant-sync` - sync the shared bundle with the upstream
  `webdev-assistant` repository while keeping local work on `main`, using
  short-lived PR branches for publication, or pushing a fallback branch when
  `main` does not exist yet
- `skills/frontend-security-inspector` - security-focused review
- `skills/technical-seo-app` - technical SEO review and fixes
- `skills/screenshot-design-inspector` - screenshot-first design extraction
- `skills/architecture-from-spec` - architecture planning from a user
  specification

## Nested upstream repo

- `.agents/` itself is the local checkout of
  `git@github.com:ytvee-dev/webdev-assistant.git`
- `.agents/AGENTS.md` is the canonical publishable copy of the bundle policy
- the host repository root `AGENTS.md` is a stable pointer to
  `.agents/AGENTS.md`, not a synchronized mirror
- `.agents/README.md` and `.agents/.gitignore` belong to the shared bundle repo
- `.agents/project/**` stays local-only inside the nested checkout
- `.agents/.obsidian/**` stores local Obsidian vault settings and is not
  publishable
- changes inside `.agents/` do not require updating the host-root `AGENTS.md`
  unless the canonical policy path itself changes

## Navigation rules

- Prefer filesystem MCP tools for reading file contents and directory
  structure. Use shell commands for search, git state, diffs, and executable
  checks when command output itself is needed.
- Treat `.agents/common/**` as upstream-managed reusable bundle docs.
- Treat `.agents/project/**` as repo-specific facts and policy overlays.
- Treat `.agents/skills/**` as reusable workflows and reference material.
- Treat `.agents/AGENTS.md`, `.agents/SUMMARY.md`, `.agents/common/**`,
  `.agents/skills/**`, `.agents/README.md`, and `.agents/.gitignore` as the
  publishable shared-bundle surface.
- When a task changes project facts or reveals documentation drift, update the
  relevant `.agents/project/**` files in the same task.
- When a task asks the agent to adapt to a new project, initialize Codex
  project context, connect `.agents`, or create the host-root `AGENTS.md`
  pointer, use `project-onboarding-adapter`; it only works in Plan Mode.
- When a task changes publishable bundle structure, cross-links, skill names,
  or reading order, update this file in the same task.
- When a task adds, renames, or moves Markdown files, update graph frontmatter
  and Obsidian wikilinks in the same task.
- When project onboarding, project context refresh, README maintenance,
  sync-down drift repair, or skill authoring changes Markdown docs, update
  graph frontmatter and keep workflow instructions in the body.
- When a task changes user-facing agent workflow, skill lists, path policy, or
  sync/publication instructions, update `.agents/README.md` in the same task.
- When shared client state, selectors, or Redux are in scope, include
  `redux-state-workflow` alongside the React or Next.js skill chain instead of
  relying on component guidance alone.
- When a task is about syncing or publishing the bundle itself, use
  `webdev-assistant-sync`.
