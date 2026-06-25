---
id: 'agents.common.anti-patterns'
title: 'Common Anti-Patterns'
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
    - '[[skills/design-screenshot-spec/SKILL|Design Screenshot Spec]]'
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
depends_on: []
---

# Common Anti-Patterns

Purpose: define prohibited directions for this screenshot-to-frontend bundle.

- Using Figma MCP, live Figma inspection, Figma canvas editing, Figma file
  creation, Figma whiteboard, design-system generation, or Code Connect workflows.
- Treating a Figma URL, file key, node id, or Figma whiteboard reference as
  sufficient source material.
- Implementing code before producing or receiving a `Design Implementation
  Spec`.
- Guessing hidden component states, assets, token names, breakpoints, or
  interactions when the source material does not provide them.
- Installing packages before checking whether project-native tools already
  solve the problem.
- Adding packages, new styling systems, global tokens, theme layers, or
  generated scaffolds without explicit user approval.
- Installing missing MCP servers without explicit user approval and a verified
  official install source.
- Installing broad, unofficial, design-tool, Figma, whiteboard, or live-design
  MCP servers as fallbacks.
- Creating app source files, framework configs, package manifests, routes,
  components, styles, tests, or build scripts during new-project onboarding.
- Replacing the project's frontend architecture with a preferred framework
  pattern that the project does not use.
- Hardcoding broad reusable colors, spacing, typography, or config when an
  existing token or local owner exists.
- Refactoring unrelated code while implementing a visual spec.
- Using a dev server as a substitute for documented verification.
- Skipping rendered browser verification for visual implementation work.
- Interacting with production systems, production data, or live production
  environments.
- Publishing or copying `project/**` facts into reusable bundle docs.
