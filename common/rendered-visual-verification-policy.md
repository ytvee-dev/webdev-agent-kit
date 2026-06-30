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
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
    - '[[skills/mcp-toolchain-manager/SKILL|MCP Toolchain Manager]]'
depends_on: []
---

# Rendered Visual Verification Policy

Purpose: keep rendered automation narrow and tied to visual QA.

## Allowed Use

Use Browser or Playwright MCP only when rendered evidence is required:

- compare an implemented page with supplied screenshots or visual references;
- capture desktop, tablet, or mobile screenshots for visual QA;
- check responsive layout, wrapping, overflow, clipping, occlusion, or viewport fit;
- check visible interaction states such as hover, focus, active, selected, disabled, loading, empty, or error;
- confirm console or runtime errors that affect the rendered UI during visual QA;
- collect screenshot evidence for a reported visual regression.

## Not Allowed Use

Do not use Browser or Playwright MCP for tasks that should be answered from static files, supplied inspect values, or documentation:

- reading font family, font size, font weight, line height, colors, spacing, CSS variables, or tokens when those values are present in source or copied notes;
- checking typography through computed styles only;
- routine lint, typecheck, build, refactor, or code review tasks;
- project onboarding, stack detection, or MCP detection;
- replacing a missing configured Browser or Playwright MCP with a local Playwright dependency.

Typography work starts from the Design Implementation Spec, copied inspect values, CSS files, tokens, and component styles. Browser evidence may be used only when typography is part of a broader visual mismatch that cannot be evaluated from source alone.

## Availability Boundary

A running local app and an installed Playwright dependency do not mean Browser or Playwright MCP is available.

If the MCP tool required for rendered visual QA is missing, report the missing capability and the blocked checks. Do not claim tool-based visual QA from a local Playwright dependency unless the user explicitly approved that fallback for the current task.
