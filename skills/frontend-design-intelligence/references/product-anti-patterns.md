---
id: 'agents.skills.frontend-design-intelligence.references.product-anti-patterns'
title: 'Product Anti-Patterns'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-design-intelligence'
tags:
    - 'agents/skill-package'
    - 'agents/reference'
    - 'quality/anti-slop'
parent:
    - '[[skills/frontend-design-intelligence/SKILL|Frontend Design Intelligence]]'
related:
    - '[[common/anti-template-defaults|Anti-Template Defaults]]'
    - '[[common/design-quality-rubric|Design Quality Rubric]]'
    - '[[skills/frontend-design-intelligence/references/product-pattern-matrix|Product Pattern Matrix]]'
depends_on:
    - '[[skills/frontend-design-intelligence/SKILL|Frontend Design Intelligence]]'
---

# Product Anti-Patterns

Purpose: identify product-specific design shortcuts before they become implementation defaults.

These patterns are suspicious, not universally banned. Keep them only when the brief or project evidence justifies them.

## General

- Fake metrics that make the interface look complete.
- Decorative badges that do not change understanding.
- Numbered cards without sequence or priority.
- Equal feature cards for content that has real hierarchy.
- Gradients, glass, glow, or shadows without a subject reason.
- Marketing claims that could fit any product.
- Screenshots or charts that do not support the page thesis.

## Product-Specific Risks

### SaaS And B2B

- Generic hero with vague dashboard and three feature cards.
- Trust markers without actual trust content.
- CTA labels that do not say what happens next.
- Feature grids that hide the real workflow.

### AI And Automation

- Purple gradient as the whole visual idea.
- Magic claims without showing user control, review, and failure paths.
- Generated-looking chat bubbles with no real product state.
- No indication of confidence, source, approval, or reversibility when those matter.

### Developer Tools

- Fake terminal output.
- Code samples too small to read or unrelated to the user task.
- Hiding installation, configuration, errors, or compatibility behind marketing copy.
- Overdesigned visuals that make the tool feel less credible.

### Dashboards And Analytics

- Charts without a data question.
- KPI cards with no unit, time window, or comparison context.
- Dense dashboards where every element has equal emphasis.
- Color-only status or chart meaning.
- No empty, loading, or error state for data surfaces.

### Ecommerce And Marketplace

- Visual polish that competes with product comparison.
- Hidden availability, shipping, total cost, or return information.
- Filters that look decorative rather than actionable.
- Reviews or trust marks with no source or context.

### Education And Content

- Gamified visuals that do not support learning.
- Article layouts that reduce readability for the sake of style.
- Tag clouds, badges, or topic grids with no information scent.
- Progress indicators that do not map to a real learner path.

## Replacement Rule

Do not only delete an anti-pattern. Replace it with actual workflow, real data hierarchy, user decision path, meaningful state, product-specific artifacts, or one restrained signature element.
