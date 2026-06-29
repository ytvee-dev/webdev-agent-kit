---
name: frontend-visual-qa
description: Use after frontend visual implementation to verify rendered UI against a Design Implementation Spec and supplied screenshots. Run browser or Playwright checks, capture desktop and mobile evidence, compare visual references, and report deviations. Do not use Figma MCP or treat static checks as visual QA.
---

# Frontend Visual QA

## Purpose

Verify a rendered frontend implementation against the `Design Implementation
Spec` and supplied visual references using browser evidence, viewport checks,
and visual diff review.

## When To Use

- After `frontend-layout-implementer` changes rendered UI.
- When the user asks to check visual fidelity, responsive behavior, screenshots,
  browser rendering, console errors, or layout overflow.
- When visual acceptance requires comparing implementation screenshots against
  supplied references.

## When Not To Use

- Documentation-only, skill-only, backend-only, or static code review tasks.
- Design intake before implementation. Use `design-screenshot-spec`.
- Live Figma inspection or Figma MCP workflows.

## Required Context

1. Read `AGENTS.md`.
2. Confirm the classified task is `visual-qa`, frontend verification, or a
   post-implementation rendered UI check.
3. Read `common/approved-patterns.md`.
4. Read `common/anti-patterns.md`.
5. Read `project/verification-profile.md` when present.
6. Read the `Design Implementation Spec`, visual references, changed files,
   and relevant routes or pages.
7. Read `references/visual-qa-checklist.md`.

## Tool Contract

- Use Playwright MCP directly when it is available and callable in the current
  session. Open the local app, inspect console/runtime errors, interact with
  controls, resize viewports, and capture screenshots without asking the user
  for separate confirmation.
- Use Browser MCP as a lower-confidence rendered QA fallback only when
  Playwright MCP is unavailable. Do not install missing MCP servers as part of
  the fallback.
- Use Visual Diff MCP when available to compare implementation screenshots with
  supplied references.
- Use Visual Reference MCP when available to access supplied images.
- Use `mdn` only when web platform behavior affects the QA finding.
- Do not use Figma MCP.
- If Playwright MCP, browser tooling, or visual diff tooling is unavailable,
  report the blocker and complete only the checks that can be run honestly.

## Workflow

1. Identify target routes, pages, components, states, and viewports from the
   spec.
2. Start or reuse the local app with the project's normal development or preview
   command when needed.
3. Open the rendered target in Browser or Playwright MCP.
4. Check console and runtime errors.
5. Verify desktop, tablet, and mobile viewport fit when in scope.
6. Capture implementation screenshots.
7. Compare screenshots against visual references with Visual Diff MCP when
   available; otherwise perform manual comparison using the checklist.
8. Exercise relevant hover, focus, selected, disabled, loading, empty, error,
   and interaction states when provided by the spec.
9. Fix scoped implementation issues only when the user asked for fixes or the
   task is part of implementation; otherwise report findings.
10. Hand off material quality, architecture, TypeScript, security, or
    performance concerns to `frontend-quality-reviewer` instead of treating
    visual QA as a broad code review.

## Output Contract

Report:

- routes or pages verified;
- viewports checked;
- interactions or states checked;
- console/runtime findings;
- visual diff result or manual comparison summary;
- fixed issues or remaining deviations;
- blockers and unavailable tools.

## Validation Gates

- A visual QA pass must include rendered browser evidence unless blocked.
- When Playwright MCP is callable, proposing Playwright checks or reporting a
  handoff is not a completed visual QA pass; run the rendered checks.
- Static typecheck, lint, or build alone is not visual QA.
- Rendered verification is QA evidence, not a testing workflow.
- Material visual mismatches must be reported with the affected viewport or
  state.
- No Figma MCP use is allowed.

## Trigger Evals

Should trigger:

- "Verify the implemented screen against the screenshots with Playwright."
- "Run visual QA on desktop and mobile."
- "Compare the rendered page to the design references and report deviations."

Should not trigger:

- "Write the implementation spec from screenshots."
- "Implement this spec now."
- "Inspect the Figma node directly."

## Reference Map

- `references/visual-qa-checklist.md`
