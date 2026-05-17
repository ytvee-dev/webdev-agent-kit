---
name: webapp-task-protocol
description: Use to classify React and Next.js application tasks, detect project
    type, choose the right skill chain from the user prompt and repo context,
    and enforce inspect -> plan -> implement -> verify.
---

# Webapp Task Protocol

## When to use

- New feature work
- Refactors
- Bug fixes
- Code review or follow-up fixes
- SEO or security audits
- Design implementation tasks that may start from a Figma URL

## Required context order

1. Read `AGENTS.md`.
2. Read framework indexes and overlay files based on task type:
    - Always: `.agents/project/stack-profile.md`
    - Implementation or refactor work: `.agents/common/approved-patterns.md`
    - Implementation or refactor work with local addenda: `.agents/project/approved-patterns.md`
    - Routing / layout / metadata / server-client work: `.agents/project/next/path-index.md`
    - Component / hooks / client UI work: `.agents/project/react/path-index.md`
    - Routing / architecture overview: `.agents/project/architecture-map.md`
    - Styling or design-driven work: `.agents/project/styling-profile.md`
    - Figma URL present: `.agents/project/figma-profile.md`
    - Any implementation work: `.agents/common/anti-patterns.md`
    - Local implementation exceptions or addenda: `.agents/project/anti-patterns.md`
3. Read the affected source files and configuration files.
4. Then choose the skill chain.

## Skill selection rules

- Select skills from the user prompt and repo context. The user does not need
  to name a skill explicitly.
- Prefer MCP tools and project indexes before broad repo scanning when the
  required tool or context is available.
- Prefer filesystem MCP tools for reading file contents and directory structure
  when available. Use shell commands for targeted search, git state, diffs, and
  verification output.
- Use this lookup fallback order: framework index -> targeted repo search ->
  user clarification.
- Run an initial scan on the first substantive request and a delta scan on later
  tasks focused on the affected area and documentation drift risk.
- Search for an existing implementation before inventing a new abstraction,
  component, hook, selector, or store layer.
- If the task changes project facts or `.agents/` structure, route the follow-up
  documentation update in the same task.

## Routing workflow

1. Classify the task: `feature`, `refactor`, `bugfix`, `review`, or `audit`.
2. Detect the framework boundary:
    - Next.js routing/layout/metadata/server-client work -> `nextjs-app-router`
    - React component/state/hooks work -> `react-component-workflow`
    - Redux, selectors, or shared client-state work -> `redux-state-workflow`
3. Detect the project type:
    - `frontend-only`
    - `fullstack`
4. Add cross-cutting skills as needed:
    - `frontend-typescript-rules`
    - `boundary-input-validation`
5. End implementation work with `frontend-review-and-fix`.
6. If implementation changes project structure, routes, components, helpers,
   styling tokens, or verification commands, use `project-context-adapter` to
   refresh `.agents/project/**` before finishing.

## Prompt-specific skills

- Use `technical-seo-app` for SEO requests.
- Use `frontend-security-inspector` for security-audit requests.
- Use `project-context-adapter` when repo overlay docs need refresh or
  project-specific indexing updates.
- Use `agent-rules-skill-author` when the request is about agent rules, skills,
  or `AGENTS.md` policy.
- Use `webdev-assistant-sync` when the request is about syncing or publishing
  the shared agent bundle through `git@github.com:ytvee-dev/webdev-assistant.git`.
- Use `screenshot-design-inspector` when Figma access is unavailable and the
  user provides or can provide screenshots.
- Use `architecture-from-spec` when the user provides a new-project or
  large-refactor specification and wants architecture guidance.

## Figma trigger

If the prompt includes a Figma URL, node, or explicit design implementation
request:

1. Use the built-in Figma capabilities first.
2. Read `.agents/project/figma-profile.md`.
3. If Figma access fails, ask the user for screenshots and switch to
   `screenshot-design-inspector`.
4. Continue implementation with the appropriate domain skill.

## Reference map

- `references/classification-rules.md`
- `references/task-routing.md`
