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
    - '[[common/css-modules-specificity-rules|CSS Modules Specificity Rules]]'
    - '[[common/form-feedback-rules|Form Feedback Rules]]'
    - '[[common/navigation-ux-rules|Navigation UX Rules]]'
    - '[[common/data-visualization-rules|Data Visualization Rules]]'
    - '[[common/icon-quality-rules|Icon Quality Rules]]'
    - '[[common/mobile-responsive-rules|Mobile Responsive Rules]]'
    - '[[skills/design-screenshot-spec/SKILL|Design Screenshot Spec]]'
    - '[[skills/frontend-design-director/SKILL|Frontend Design Director]]'
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

Implement a `Design Implementation Spec` or `Design Direction Contract` in a React or Next.js project while respecting existing CSS Modules, Redux, TanStack, Axios, architecture, styling, decomposition, and verification conventions.

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
5. Read `common/css-modules-specificity-rules.md` for CSS Modules changes.
6. Read conditional UX rules only when the touched surface needs them: forms, navigation, data visualization, icons, or mobile responsive behavior.
7. Read relevant project overlays when present: stack, architecture, styling, verification, state, data-fetching, build, and workspace profiles.
8. Read the `Design Implementation Spec`, `Design Direction Contract`, and supplied visual references.
9. Read affected source files, styles, components, routes, and configs.
10. Read `references/implementation-rules.md` when present.

Do not read `README.md` or `dist/**` during normal runtime.

## Tool Contract

- Use Project Context MCP when available; otherwise read `project/**` and source files directly.
- Use Design Spec MCP when available; otherwise use the supplied spec text or user-approved local artifact.
- Use Visual Reference MCP when available; otherwise use attached or local image files supplied by the user.
- Use `context7` for React, Next.js, Redux, TanStack, Axios, TypeScript, or build-tool docs when implementation depends on current behavior.
- Use `mdn` for current HTML, CSS, Web API, accessibility, and compatibility facts.
- Use rendered visual QA only when screenshot comparison, viewport evidence, overflow checks, or visible state verification are in scope.
- Use Visual Diff MCP when available during final visual comparison.
- Do not use Figma MCP.
- If a named MCP is unavailable, report the missing capability before using a lower-confidence fallback.

## Workflow

1. Confirm the task is within the supported target stack.
2. Detect React/Next.js routing, CSS Modules ownership, Redux ownership, TanStack usage, Axios API adapter boundaries, and verification commands.
3. Map the spec to existing project components, layout primitives, tokens, assets, styles, and UX patterns.
4. Identify missing design details before editing. Ask only when the gap changes implementation.
5. Use `frontend-architecture-planner` before editing when route, state, data, form, build, workspace, or shared component ownership is unclear or material.
6. Plan component decomposition before editing.
7. Map structure as information before adding numbers, dividers, badges, labels, grids, metrics, or decorative sections.
8. Identify conditional UX gates: forms, navigation, data visualization, icon quality, and mobile responsiveness.
9. Identify CSS Modules ownership and selector risks before styling.
10. Implement the smallest scoped change that satisfies the spec, design direction, architecture handoff, and decomposition plan.
11. Keep UI state local unless existing React, Redux, or TanStack ownership requires otherwise.
12. Keep styles in CSS Modules by default.
13. Reuse existing Axios clients and API adapters for API-facing changes.
14. Do not add dependencies, global tokens, UI libraries, or new styling systems without explicit approval.
15. Preserve accessibility, semantic structure, keyboard/focus behavior, text wrapping, responsive behavior, and stable layout dimensions.
16. Use `frontend-linter-manager` after code-changing work when a lint command exists.
17. Run relevant project verification commands from `project/verification-profile.md`.
18. Run `frontend-visual-qa` only when the change needs rendered screenshot comparison, viewport evidence, overflow verification, or visible state verification.
19. Use `frontend-quality-reviewer` before final reporting when the user asks for review, the implementation has significant surface area, or the plan requires a quality pass.

## Output Contract

Report:

- implemented spec scope;
- affected React or Next.js surface;
- decomposition applied or why the touched component remained intentionally small;
- CSS Modules, Redux, TanStack, Axios, or project primitives reused;
- form, navigation, data, icon, and responsive gates considered or skipped as not applicable;
- deviations from the design spec;
- lint and verification commands run;
- rendered visual QA result, skipped reason, or blocker.

## Validation Gates

- Implementation must follow inspected project conventions.
- The target must be within React, Next.js, CSS Modules, Redux, TanStack, or Axios scope.
- CSS Modules changes must have clear ownership and stable specificity.
- Structural devices must encode meaning instead of decoration.
- Form, navigation, data, icon, and mobile risks must be handled when present.
- No Figma MCP use is allowed.
- No new package, styling system, global token, architecture layer, or UI library may appear without approval.
- Code-changing implementation must run lint when an existing lint command is available.

## Reference Map

- `common/target-stack-policy.md`
- `common/approved-patterns.md`
- `common/anti-patterns.md`
- `common/css-modules-specificity-rules.md`
- `common/form-feedback-rules.md`
- `common/navigation-ux-rules.md`
- `common/data-visualization-rules.md`
- `common/icon-quality-rules.md`
- `common/mobile-responsive-rules.md`
- `skills/frontend-architecture-planner/SKILL.md`
- `skills/frontend-linter-manager/SKILL.md`
- `skills/frontend-quality-reviewer/SKILL.md`
- `skills/frontend-visual-qa/SKILL.md`
