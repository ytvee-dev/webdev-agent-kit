---
name: frontend-visual-qa
description: Use after frontend visual implementation only when rendered visual evidence is required: screenshot comparison, responsive layout, overflow, visible interaction states, or visual regression evidence. Use Browser or Playwright MCP only for those rendered visual QA tasks. Do not use it for static style lookup, font checks by computed styles, routine code review, lint, typecheck, build, onboarding, or MCP detection.
id: 'agents.skills.frontend-visual-qa.skill'
title: 'Frontend Visual QA'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-visual-qa'
tags:
    - 'agents/skill-package'
    - 'frontend/verification'
    - 'frontend/visual-qa'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[common/rendered-visual-verification-policy|Rendered Visual Verification Policy]]'
    - '[[skills/frontend-visual-qa/references/visual-qa-checklist|Visual QA Checklist]]'
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Frontend Visual QA

## Purpose

Verify a rendered frontend implementation against a `Design Implementation Spec` and supplied visual references when the task needs browser-rendered visual evidence.

This skill is not a general style-inspection tool. It exists for screenshot comparison, responsive rendering, visual regression evidence, and visible state verification.

## When To Use

- After implementation when visual acceptance requires comparing the rendered page with supplied screenshots or visual references.
- When the user asks to run visual QA, capture desktop/mobile screenshots, or compare rendered output to a design reference.
- When the issue is visibly rendered: responsive layout, wrapping, overflow, clipping, occlusion, viewport fit, visible interaction states, or screenshot-backed visual regression.
- When console or runtime errors must be checked because they affect the rendered UI during visual QA.

## When Not To Use

- Documentation-only, skill-only, backend-only, or static code review tasks.
- Design intake before implementation. Use `design-screenshot-spec`.
- Live Figma inspection or Figma MCP workflows.
- Font-family, font-size, font-weight, line-height, color, spacing, CSS variable, or token checks when values can be read from source files, copied inspect values, or the Design Implementation Spec.
- Computed-style checks whose only purpose is to read typography or token values.
- Routine lint, typecheck, build, refactor, onboarding, stack detection, or MCP detection.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/rendered-visual-verification-policy.md`.
3. Confirm the classified task is `visual-qa` and specifically needs rendered visual evidence.
4. Read `common/approved-patterns.md`.
5. Read `common/anti-patterns.md`.
6. Read `project/verification-profile.md` when present.
7. Read the `Design Implementation Spec`, visual references, changed files, and relevant routes or pages.
8. Read `references/visual-qa-checklist.md`.

## Tool Contract

- Use Browser or Playwright MCP only for rendered visual QA tasks allowed by `common/rendered-visual-verification-policy.md`.
- Browser or Playwright MCP availability means the tool is callable in the current agent session. A running local server or an installed Playwright dependency does not count as MCP availability.
- Do not replace a missing configured Browser or Playwright MCP with local Playwright package usage unless the user explicitly approved that fallback for the current task.
- Use Visual Diff MCP when available to compare implementation screenshots with supplied references.
- Use Visual Reference MCP when available to access supplied images.
- Use `mdn` only when web platform behavior affects a visual QA finding.
- Do not use Figma MCP.
- If Browser or Playwright MCP is unavailable, report which rendered checks are blocked and complete only the non-rendered checks that can be run honestly.

## Workflow

1. Identify target routes, pages, components, states, and viewports from the spec.
2. Confirm the task is in the allowed rendered visual QA spectrum.
3. For typography, spacing, color, and token questions, inspect the spec, copied values, CSS, tokens, and component styles first. Do not open Browser or Playwright just to read computed styles.
4. Start or reuse the local app with the project's normal development or preview command only when rendered visual evidence is in scope.
5. Open the rendered target in Browser or Playwright MCP only when that MCP tool is available and the task is in scope.
6. Check console and runtime errors only when they affect the rendered visual QA scope.
7. Verify desktop, tablet, and mobile viewport fit when in scope.
8. Capture implementation screenshots when visual comparison or evidence is in scope.
9. Compare screenshots against visual references with Visual Diff MCP when available; otherwise perform manual comparison using the checklist.
10. Exercise relevant hover, focus, selected, disabled, loading, empty, error, and interaction states only when provided by the spec or visible acceptance criteria.
11. Fix scoped implementation issues only when the user asked for fixes or the task is part of implementation; otherwise report findings.
12. Hand off material quality, architecture, TypeScript, security, or performance concerns to `frontend-quality-reviewer` instead of treating visual QA as a broad code review.

## Output Contract

Report:

- rendered visual QA scope;
- routes or pages verified;
- viewports checked;
- interactions or states checked;
- console/runtime findings when in scope;
- visual diff result or manual comparison summary;
- static style checks used instead of browser tooling, when applicable;
- fixed issues or remaining deviations;
- blockers and unavailable tools.

## Validation Gates

- Browser or Playwright must be used only for rendered visual QA tasks named in `common/rendered-visual-verification-policy.md`.
- A local Playwright package, lockfile entry, or running local server must not be reported as Browser or Playwright MCP availability.
- Font and token checks must prefer source files, copied inspect values, and specs over computed styles.
- A visual QA pass must include rendered browser evidence unless blocked.
- Static typecheck, lint, or build alone is not visual QA.
- Rendered verification is QA evidence, not a testing workflow.
- Material visual mismatches must be reported with the affected viewport or state.
- No Figma MCP use is allowed.

## Trigger Evals

Should trigger:

- "Verify the implemented screen against the screenshots with Playwright."
- "Run visual QA on desktop and mobile."
- "Compare the rendered page to the design references and report deviations."
- "Capture screenshots and check whether the mobile layout overflows."

Should not trigger:

- "Check which font-size token this heading uses."
- "Read computed styles for typography."
- "Write the implementation spec from screenshots."
- "Implement this spec now."
- "Inspect the Figma node directly."

## Reference Map

- `common/rendered-visual-verification-policy.md`
- `references/visual-qa-checklist.md`
