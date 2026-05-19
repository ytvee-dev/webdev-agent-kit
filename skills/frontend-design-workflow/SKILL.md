---
name: frontend-design-workflow
description: Use when React or Next.js work is primarily visual design, design-to-code implementation, Figma or screenshot translation, responsive polish, typography, color, motion, canvas/generative UI, or making an interface feel intentionally designed. Do not use for pure routing, metadata, security, or non-visual refactors.
id: 'agents.skills.frontend-design-workflow.skill'
title: 'Frontend Design Workflow'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-design-workflow'
tags:
    - 'agents/skill-package'
    - 'frontend/design'
    - 'frontend/react'
    - 'agents/skill'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/frontend-design-workflow/references/design-implementation|Design Implementation]]'
    - '[[skills/frontend-design-workflow/references/generative-ui|Generative UI]]'
    - '[[skills/screenshot-design-inspector/SKILL|Screenshot Design Inspector]]'
    - '[[skills/react-component-workflow/SKILL|React Component Workflow]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Frontend Design Workflow

## When to use

- Implement a visual design from Figma, screenshots, written design direction,
  or an existing UI that needs polish.
- Improve typography, color, hierarchy, spacing, responsiveness, motion, or
  interaction states.
- Build a React UI whose primary challenge is visual quality rather than data
  flow.
- Create canvas, generative, or web-art UI only when the user explicitly asks
  for that kind of experience.

## Required context

Before editing:

1. Read `AGENTS.md`.
2. Read `.agents/project/styling-profile.md` for the styling system, tokens,
   breakpoints, and CSS conventions.
3. Read `.agents/project/figma-profile.md` when the work starts from Figma.
4. Read `.agents/project/react/path-index.md` or
   `.agents/project/next/path-index.md` based on the affected UI surface.
5. Read the existing component and nearby styles before designing new UI.
6. Add `react-component-workflow` for component architecture and hooks.
7. Add `nextjs-app-router` when the visual work changes route structure,
   layouts, metadata, or server/client boundaries.

## Core rules

- Define the audience, purpose, and visual intent before changing styles.
- Follow the repo's existing styling system first: CSS Modules, tokens,
  variables, breakpoints, typography primitives, and component patterns.
- Do not introduce Tailwind, shadcn/ui, a new token system, external fonts, or a
  new design system unless the user explicitly approves that architecture
  change.
- Prefer distinctive, context-specific visual decisions over generic centered
  layouts, one-note palettes, excessive rounded cards, or decorative gradients.
- Keep hierarchy legible: typography, spacing, density, and controls must match
  the user's workflow and the local product context.
- Make responsive behavior explicit. Check stacking, overflow, text wrapping,
  tap targets, and long labels.
- Use motion only when it clarifies state, transition, or interaction. Keep it
  compatible with accessibility and repo conventions.
- Preserve accessibility: labels, focus states, keyboard interaction, contrast,
  alt text, and reduced-motion expectations.
- If Figma access fails, ask for screenshots and use
  `screenshot-design-inspector`.
- For canvas, generative, or algorithmic UI, do not add p5.js, Three.js, a
  bundling scaffold, or an artifact toolchain unless the user explicitly wants
  that approach and the repo already supports it or approves the dependency.

## Reference map

- `references/design-implementation.md`
- `references/generative-ui.md`
