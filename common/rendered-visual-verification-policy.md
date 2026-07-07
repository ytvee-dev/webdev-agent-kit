---
id: 'agents.common.rendered-visual-verification-policy'
title: 'Rendered Visual Verification Policy'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'frontend/verification'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/smart-verification-budget|Smart Verification Budget]]'
    - '[[common/diff-impact-verification-rules|Diff Impact Verification Rules]]'
    - '[[common/mcp-availability-detection-rules|MCP Availability Detection Rules]]'
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
    - '[[skills/mcp-toolchain-manager/SKILL|MCP Toolchain Manager]]'
depends_on: []
---

# Rendered Visual Verification Policy

Purpose: keep rendered automation narrow, capability-aware, and tied to visual QA.

## Allowed Use

Use Browser or Playwright only when rendered evidence is required:

- compare an implemented page with supplied screenshots or visual references;
- capture desktop, tablet, or mobile screenshots for visual QA;
- check responsive layout, wrapping, overflow, clipping, occlusion, or viewport fit;
- check visible interaction states such as hover, focus, active, selected, disabled, loading, empty, or error;
- confirm console or runtime errors that affect the rendered UI during visual QA;
- collect screenshot evidence for a reported visual regression;
- verify a repeated visual correction after the previous source-only or static verification was insufficient.

## Not Allowed Use

Do not use Browser or Playwright for tasks that should be answered from static files, supplied inspect values, or documentation:

- reading font family, font size, font weight, line height, colors, spacing, CSS variables, or tokens when those values are present in source or copied notes;
- checking typography through computed styles only;
- routine lint, typecheck, build, refactor, or code review tasks;
- project onboarding, stack detection, or MCP detection;
- replacing a missing configured Browser or Playwright MCP with a local Playwright dependency;
- low-risk CSS-only color, background, border color, or decorative mask changes when no layout or repeated-failure risk is present.

Typography work starts from the Design Implementation Spec, copied inspect values, CSS files, tokens, and component styles. Browser evidence may be used only when typography is part of a broader visual mismatch that cannot be evaluated from source alone.

## Availability Boundary

Read `common/mcp-availability-detection-rules.md` before checking Browser or Playwright availability.

A running local app, open port, lockfile entry, and installed Playwright dependency do not mean Browser or Playwright MCP is available.

If the MCP or host browser capability required for rendered visual QA is missing, report the missing capability and blocked checks. Do not claim tool-based visual QA from a local Playwright dependency unless the user explicitly approved that fallback for the current task.

## Impact Boundary

Read `common/diff-impact-verification-rules.md` before deciding route and viewport scope.

Rendered QA must be limited to directly affected routes, components, states, and viewports. Do not discover and test unrelated pages merely because the local app has them.

## Cost Boundary

Read `common/smart-verification-budget.md` for lightweight and CSS-only changes.

Tool availability does not make rendered QA mandatory. A browser check must have a named visual acceptance criterion, directly affected surface, repeated-failure signal, or explicit user request.
