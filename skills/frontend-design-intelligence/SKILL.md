---
name: frontend-design-intelligence
description: Use for standard or deep UI work when product category, page pattern, design dials, domain-specific UX risks, or design anti-patterns need grounding before a Design Direction Contract. Produces a compact brief only; does not implement code or install tools.
id: 'agents.skills.frontend-design-intelligence.skill'
title: 'Frontend Design Intelligence'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-design-intelligence'
tags:
    - 'agents/skill-package'
    - 'agents/design'
    - 'workflow/design-intelligence'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/frontend-design-director/SKILL|Frontend Design Director]]'
    - '[[common/design-quality-rubric|Design Quality Rubric]]'
    - '[[common/anti-template-defaults|Anti-Template Defaults]]'
    - '[[common/ui-ux-priority-checklist|UI UX Priority Checklist]]'
    - '[[skills/frontend-design-intelligence/references/product-pattern-matrix|Product Pattern Matrix]]'
    - '[[skills/frontend-design-intelligence/references/design-dials|Design Dials]]'
    - '[[skills/frontend-design-intelligence/references/product-anti-patterns|Product Anti-Patterns]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Frontend Design Intelligence

## Purpose

Create a compact design intelligence brief before visual direction when a UI task needs product-category grounding, page-pattern choice, density decisions, or domain-specific anti-pattern checks.

This skill adapts design-system reasoning into the WebDev Assistant model without becoming a UI framework, CLI generator, or package installer.

## When To Use

Use after prompt intent routing when the task is `Standard Workflow` or `Deep Workflow` and one or more are true:

- product type, page type, audience, or user job is vague;
- the user asks for visual style, landing structure, dashboard structure, or distinctive UI direction;
- the page needs visual variance, motion, or density decisions;
- `frontend-design-director` needs better grounding before writing a Design Direction Contract.

## When Not To Use

Do not use for Fast Lookup, tiny edits, purely technical bugfixes, code implementation, live Figma inspection, package installation, or new styling systems.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/prompt-intent-routing-rules.md` when workflow level is unclear.
3. Read relevant project overlays when present.
4. Read only relevant references from this skill:
   - `references/product-pattern-matrix.md`;
   - `references/design-dials.md`;
   - `references/product-anti-patterns.md`.
5. Read supplied screenshots, briefs, inspect notes, or existing route files only when they materially affect the brief.

## Tool Contract

- May read project overlays and relevant source files.
- Must not run design generators or external CLIs.
- Must not create or edit app source code.
- Must not create a global design system unless explicitly requested, and then only inside `.agents/project/**`.
- Must not use Figma MCP.

## Workflow

1. Identify product category, audience, page type, and single job.
2. If required facts are missing, infer the smallest useful assumption and label it.
3. Select a likely page pattern from the user job, not from a generic style catalog.
4. Set design dials: visual variance, motion intensity, and information density.
5. Identify domain UX risks.
6. Identify product-specific anti-patterns and generic template risks.
7. Produce a compact Design Intelligence Brief.
8. Hand off to `frontend-design-director` when visual direction is needed.

## Output Contract

```text
Product Category
Audience
Page Type
Single Job
Recommended Page Pattern
Design Dials
Domain UX Risks
Product-Specific Anti-Patterns
Useful Subject Materials
Design Direction Handoff
```

## Validation Gates

- The brief must not prescribe a UI library, styling system, package, or animation dependency.
- The recommendation must be a starting hypothesis, not a rigid template.
- The page pattern must connect to the user job.
- Design dials must explain restraint or intensity.
- Durable records belong in local project overlays, not reusable bundle docs.

## Reference Map

- `references/product-pattern-matrix.md`
- `references/design-dials.md`
- `references/product-anti-patterns.md`
- `skills/frontend-design-director/SKILL.md`
- `common/design-quality-rubric.md`
- `common/anti-template-defaults.md`
- `common/ui-ux-priority-checklist.md`
