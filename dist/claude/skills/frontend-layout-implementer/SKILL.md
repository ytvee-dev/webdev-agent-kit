---
name: frontend-layout-implementer
description: Use when implementing a Design Implementation Spec or supplied screenshot-derived visual spec in the current frontend project. Adapt to the actual stack, use project context, current framework docs, MDN, and available visual reference tooling. Do not use Figma MCP, create new styling systems, or implement before design intent is specified.
---

# Frontend Layout Implementer

## Purpose

Implement a `Design Implementation Spec` in the current frontend project while
respecting the actual stack, architecture, styling system, and verification
commands.

## When To Use

- The user asks to build a screen, section, component, or static page from a
  `Design Implementation Spec`.
- The user supplies screenshot-derived design material and asks for code in the
  current frontend project.
- The implementation target may be React, Next.js, Vite, static HTML/CSS, Vue,
  Svelte, or another frontend stack.

## When Not To Use

- The design intent has not been converted into a spec and the source is only
  screenshots. Use `design-screenshot-spec` first.
- The user asks for live Figma inspection, Figma MCP, canvas edits, or Figma
  whiteboard workflows.
- The task is unrelated to frontend rendering or layout.

## Required Context

1. Read `AGENTS.md`.
2. Confirm the classified task is `frontend-layout`, `feature/development`,
   `bugfix`, `refactor`, or `optimization` for a rendered frontend surface.
3. Read `common/approved-patterns.md`.
4. Read `common/anti-patterns.md`.
5. Read `project/stack-profile.md`, `project/architecture-map.md`,
   `project/styling-profile.md`, and `project/verification-profile.md` when
   present.
6. Read relevant path indexes under `project/**` when present.
7. Read the `Design Implementation Spec` and supplied visual references.
8. Read affected source files, styles, components, routes, and configs.
9. Read `references/implementation-rules.md`.

## Tool Contract

- Use Project Context MCP when available; otherwise read `project/**` and
  source files directly.
- Use Design Spec MCP when available; otherwise use the supplied spec text or
  user-approved local artifact.
- Use Visual Reference MCP when available; otherwise use attached or local
  image files supplied by the user.
- Use `context7` for current framework, library, or build-tool docs when the
  implementation depends on API or framework behavior.
- Use `mdn` for current HTML, CSS, Web API, accessibility, and compatibility
  facts.
- Use available Playwright MCP for rendered verification after implementation
  without asking the user for separate confirmation. Browser MCP is an allowed
  lower-confidence fallback only when Playwright MCP is unavailable.
- Use Visual Diff MCP when available during final visual comparison.
- Do not use Figma MCP.
- If a named MCP is unavailable, report the missing capability before using a
  fallback that may reduce confidence.

## Workflow

1. Classify the task as `frontend-only` unless the inspected project proves
   server-owned domain logic is being changed.
2. Detect the actual frontend stack, router, styling system, state layer, and
   verification commands.
3. Map the spec to existing project components, layout primitives, tokens,
   assets, and styles.
4. Identify missing design details before editing. Ask only when the gap changes
   implementation.
5. Use `frontend-architecture-planner` before editing when route, state, data,
   form, build, workspace, or shared component ownership is unclear or material
   to the implementation.
6. Implement the smallest scoped change that satisfies the spec, design
   direction, and architecture handoff.
7. Keep state local unless the existing project architecture requires shared
   ownership.
8. Do not add dependencies, global tokens, or new styling systems without
   explicit approval.
9. Preserve accessibility, semantic structure, keyboard/focus behavior, text
   wrapping, and responsive behavior.
10. Use `frontend-linter-manager` after code-changing work when a lint command
    exists.
11. Run relevant project verification commands from `project/verification-profile.md`.
12. Run `frontend-visual-qa` after scoped rendered frontend changes, using
    available Playwright MCP automatically when the local app can be started or
    reused.
13. Use `frontend-quality-reviewer` before final reporting when the user asks
    for review, the implementation has significant surface area, or the plan
    requires a quality pass.
14. Skip browser visual QA only for documentation-only or static-only tasks,
    changes with no rendered surface, blocked local app startup, unavailable
    Playwright/browser tooling, or an explicit user request to skip browser
    checks.

## Output Contract

Report:

- implemented spec scope;
- affected frontend surface;
- project primitives, tokens, or styling owners reused;
- deviations from the design spec;
- verification commands run;
- rendered visual QA result or blocker.

## Validation Gates

- Implementation must follow inspected project conventions.
- No Figma MCP use is allowed.
- No new package, styling system, global token, or architecture layer may appear
  without approval.
- Rendered frontend changes must include browser visual QA unless one of the
  documented workflow blockers applies.
- Code-changing implementation must run lint when an existing lint command is
  available.
- Significant implementation must run or explicitly defer
  `frontend-quality-reviewer` when review is requested or appropriate.

## Trigger Evals

Should trigger:

- "Implement this Design Implementation Spec in the app."
- "Build this screenshot-derived screen in the current frontend project."
- "Code this layout from the spec and match the supplied references."

Should not trigger:

- "Create a spec from these screenshots."
- "Use Figma MCP to inspect this node."
- "Run only visual QA on an already implemented screen."

## Reference Map

- `references/implementation-rules.md`
- `skills/frontend-architecture-planner/SKILL.md`
- `skills/frontend-linter-manager/SKILL.md`
- `skills/frontend-quality-reviewer/SKILL.md`
- `skills/frontend-visual-qa/SKILL.md`
