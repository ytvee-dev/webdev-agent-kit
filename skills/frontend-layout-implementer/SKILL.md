---
name: frontend-layout-implementer
description: Use when implementing a Design Implementation Spec or screenshot-derived visual spec in a React or Next.js project using existing CSS Modules, Redux, TanStack, and Axios conventions. Do not use for unrelated frontend stacks, Figma MCP, new styling systems, or implementation before design intent is specified.
id: 'agents.skills.frontend-layout-implementer.skill'
title: 'Frontend Layout Implementer'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-layout-implementer'
tags:
    - 'agents/skill-package'
    - 'frontend/implementation'
    - 'frontend/layout'
parent: []
related:
    - '[[common/target-stack-policy|Target Stack Policy]]'
    - '[[common/approved-patterns|Approved Patterns]]'
    - '[[common/anti-patterns|Common Anti-Patterns]]'
    - '[[skills/design-screenshot-spec/SKILL|Design Screenshot Spec]]'
    - '[[skills/frontend-architecture-planner/SKILL|Frontend Architecture Planner]]'
    - '[[skills/frontend-linter-manager/SKILL|Frontend Linter Manager]]'
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
    - '[[skills/project-context-adapter/SKILL|Project Context Adapter]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Frontend Layout Implementer

## Purpose

Implement a `Design Implementation Spec` in a React or Next.js project while respecting existing CSS Modules, Redux, TanStack, Axios, architecture, styling, decomposition, and verification conventions.

## When To Use

- The user asks to build a screen, section, component, or static page from a `Design Implementation Spec`.
- The user supplies screenshot-derived design material and asks for code in the current supported frontend project.
- The implementation target is within React, Next.js, CSS Modules, Redux, TanStack, or Axios scope.

## When Not To Use

- The design intent has not been converted into a spec and the source is only screenshots. Use `design-screenshot-spec` first.
- The user asks for live Figma inspection, Figma MCP, canvas edits, or Figma whiteboard workflows.
- The project is outside the supported target stack unless the user explicitly changes scope.
- The task is unrelated to frontend rendering or layout.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/target-stack-policy.md`.
3. Confirm the classified task is `frontend-layout`, `feature/development`, `bugfix`, `refactor`, or `optimization` for a rendered React or Next.js surface.
4. Read `common/approved-patterns.md` and relevant anti-pattern rules.
5. Read relevant project overlays when present: stack, architecture, styling, verification, state, data-fetching, build, and workspace profiles.
6. Read the `Design Implementation Spec` and supplied visual references.
7. Read affected source files, styles, components, routes, and configs.
8. Read `references/implementation-rules.md` when present.

Do not read `README.md` or `dist/**` during normal runtime.

## Tool Contract

- Use Project Context MCP when available; otherwise read `project/**` and source files directly.
- Use Design Spec MCP when available; otherwise use the supplied spec text or user-approved local artifact.
- Use Visual Reference MCP when available; otherwise use attached or local image files supplied by the user.
- Use `context7` for React, Next.js, Redux, TanStack, Axios, TypeScript, or build-tool docs when implementation depends on current behavior.
- Use `mdn` for current HTML, CSS, Web API, accessibility, and compatibility facts.
- Use available Playwright MCP for rendered verification after implementation without asking the user for separate confirmation when the local app can be used.
- Use Visual Diff MCP when available during final visual comparison.
- Do not use Figma MCP.
- If a named MCP is unavailable, report the missing capability before using a lower-confidence fallback.

## Workflow

1. Confirm the task is within the supported target stack.
2. Detect React/Next.js routing, CSS Modules ownership, Redux ownership, TanStack usage, Axios API adapter boundaries, and verification commands.
3. Map the spec to existing project components, layout primitives, tokens, assets, and styles.
4. Identify missing design details before editing. Ask only when the gap changes implementation.
5. Use `frontend-architecture-planner` before editing when route, state, data, form, build, workspace, or shared component ownership is unclear or material.
6. Plan component decomposition before editing. Separate route or page shell, feature sections, small presentational components, list or item components, and named helpers, selectors, adapters, or approved hooks when needed.
7. Implement the smallest scoped change that satisfies the spec, design direction, architecture handoff, and decomposition plan.
8. Do not create or expand components that mix routing, data access, state orchestration, transformations, form logic, repeated markup, large JSX, and side effects in one file.
9. Do not hide missing decomposition behind `renderXxx`, `xxxRender`, nested array pipelines, component-body JSX preparation, oversized custom hooks, or unnecessary `useCallback`.
10. Keep UI state local unless existing React, Redux, or TanStack ownership requires otherwise.
11. Keep styles in CSS Modules by default.
12. Reuse existing Axios clients and API adapters for API-facing changes.
13. Do not add dependencies, global tokens, UI libraries, or new styling systems without explicit approval.
14. Preserve accessibility, semantic structure, keyboard/focus behavior, text wrapping, and responsive behavior.
15. Use `frontend-linter-manager` after code-changing work when a lint command exists.
16. Run relevant project verification commands from `project/verification-profile.md`.
17. Run `frontend-visual-qa` after scoped rendered frontend changes when browser tooling and a local app are available.
18. Use `frontend-quality-reviewer` before final reporting when the user asks for review, the implementation has significant surface area, or the plan requires a quality pass.

## Output Contract

Report:

- implemented spec scope;
- affected React or Next.js surface;
- decomposition applied or why the touched component remained intentionally small;
- CSS Modules, Redux, TanStack, Axios, or project primitives reused;
- deviations from the design spec;
- lint and verification commands run;
- rendered visual QA result or blocker.

## Validation Gates

- Implementation must follow inspected project conventions.
- The target must be within React, Next.js, CSS Modules, Redux, TanStack, or Axios scope.
- Changed UI must respect component decomposition rules regardless of framework or library.
- No Figma MCP use is allowed.
- No new package, styling system, global token, architecture layer, or UI library may appear without approval.
- Rendered frontend changes must include browser visual QA unless a documented blocker applies.
- Code-changing implementation must run lint when an existing lint command is available.

## Trigger Evals

Should trigger:

- "Implement this Design Implementation Spec in the React app."
- "Build this screenshot-derived screen in the Next.js project."
- "Code this layout from the spec and match the supplied references."

Should not trigger:

- "Create a spec from these screenshots."
- "Use Figma MCP to inspect this node."
- "Run only visual QA on an already implemented screen."
- "Adapt this to an unrelated frontend framework."

## Reference Map

- `common/target-stack-policy.md`
- `common/approved-patterns.md`
- `common/anti-patterns.md`
- `skills/frontend-architecture-planner/SKILL.md`
- `skills/frontend-linter-manager/SKILL.md`
- `skills/frontend-quality-reviewer/SKILL.md`
- `skills/frontend-visual-qa/SKILL.md`
