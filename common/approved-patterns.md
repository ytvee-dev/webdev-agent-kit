---
id: 'agents.common.approved-patterns'
title: 'Approved Patterns'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'docs/policy'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[SUMMARY|Agent Documentation Summary]]'
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
depends_on: []
---

# Approved Patterns

Purpose: define reusable patterns for screenshot-to-frontend implementation.

## Source-First Design Intake

- Treat user-supplied screenshots, copied inspect panels, exported assets, and
  written notes as the design source.
- Separate high-confidence copied values from screenshot-inferred values.
- Convert visual input into a `Design Implementation Spec` before editing code.
- Keep unknown states, breakpoints, assets, and token values explicit.

## Project-Native Implementation

- Detect the actual frontend stack before choosing framework patterns.
- Select official documentation for the detected stack before encoding
  stack-specific rules: MDN for web platform behavior and `context7` for
  current framework, library, CLI, and tooling docs.
- Cache MCP and documentation capability facts in `project/mcp-profile.md`
  during onboarding or context refresh.
- Reuse existing components, routes, styling systems, tokens, breakpoints, and
  verification commands.
- Keep styles local to the edited surface unless the project already owns a
  shared primitive for the pattern.
- Use the nearest established styling owner: CSS Modules, global CSS,
  styled-components, design-system components, plain CSS, framework scoped
  styles, or another project-native mechanism.

## Responsive Layout

- Implement desktop, tablet, and mobile behavior from the spec when supplied.
- Preserve text wrapping, tap targets, focus states, and stable dimensions
  across supported viewport widths.
- Prefer semantic layout structure over pixel-only duplication.

## Verification

- Use browser-rendered evidence for visual work.
- Compare implementation screenshots against the spec and visual references.
- Report material visual deviations instead of hiding them.
