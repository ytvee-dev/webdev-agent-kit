---
id: 'agents.skills.frontend-design-intelligence.references.product-pattern-matrix'
title: 'Product Pattern Matrix'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-design-intelligence'
tags:
    - 'agents/skill-package'
    - 'agents/reference'
    - 'workflow/design-intelligence'
parent:
    - '[[skills/frontend-design-intelligence/SKILL|Frontend Design Intelligence]]'
related:
    - '[[skills/frontend-design-intelligence/references/design-dials|Design Dials]]'
    - '[[skills/frontend-design-intelligence/references/product-anti-patterns|Product Anti-Patterns]]'
    - '[[common/anti-template-defaults|Anti-Template Defaults]]'
depends_on:
    - '[[skills/frontend-design-intelligence/SKILL|Frontend Design Intelligence]]'
---

# Product Pattern Matrix

Purpose: provide starting hypotheses for product-grounded UI direction. These are not templates. The brief, project conventions, screenshots, and user constraints always win.

## How To Use

For the closest product category, extract:

```text
likely page pattern
useful subject materials
primary UX risks
visual traps to avoid
```

Then adapt the result to the actual audience and single job.

## Categories

### SaaS Or B2B Product

- Likely pattern: hero thesis, product proof, workflow, integration or trust section, CTA.
- Useful materials: real workflow objects, permissions, collaboration states, audit trails, product screenshots, setup friction.
- UX risks: vague ROI, fake metrics, overstuffed feature grids, unclear primary action.
- Avoid: generic gradient hero, meaningless badges, decorative dashboard cards.

### AI Tool Or Automation Product

- Likely pattern: problem framing, live example or before-after, control surface, trust and limits, CTA.
- Useful materials: prompts, inputs, outputs, review checkpoints, logs, confidence, human approval states.
- UX risks: magical claims, invisible failure modes, unclear user control, generic purple branding.
- Avoid: treating AI as decoration instead of showing the actual user workflow.

### Developer Tool

- Likely pattern: immediate value, code or workflow example, installation path, docs proof, integration surface.
- Useful materials: terminal, diff, API call, config, editor state, logs, status checks.
- UX risks: marketing fluff, unreadable code samples, unclear compatibility, missing error states.
- Avoid: fake terminal output and decorative code blocks that do not explain the product.

### Dashboard Or Analytics

- Likely pattern: summary, exception or trend, drill-down path, table or chart detail, filters.
- Useful materials: real data hierarchy, thresholds, alerts, time windows, comparison modes.
- UX risks: data density without hierarchy, fake numbers, charts without a question, mobile overflow.
- Avoid: dashboard layout for non-analytical content.

### Ecommerce Or Marketplace

- Likely pattern: product discovery, trust, comparison, detail, cart or conversion path.
- Useful materials: product imagery, price, availability, variants, reviews, shipping, return policy.
- UX risks: weak product hierarchy, hidden total cost, unclear availability, inaccessible filters.
- Avoid: decoration that competes with product decision making.

### Education Or Learning Product

- Likely pattern: learner goal, path or curriculum, progress, practice, feedback, next lesson.
- Useful materials: lesson cards, examples, checkpoints, achievements, mistakes, teacher notes.
- UX risks: gamification without learning purpose, unclear next step, inaccessible dense content.
- Avoid: playful visuals that reduce comprehension.

### Content, Blog, Or Editorial Site

- Likely pattern: thesis, latest or featured content, topic paths, author credibility, subscription or follow path.
- Useful materials: article hierarchy, tags, dates, reading time, author notes, related essays.
- UX risks: decorative editorial layouts that hurt reading, weak information scent, generic newsletter blocks.
- Avoid: magazine styling when the content structure does not need it.

### Portfolio Or Studio

- Likely pattern: point of view, selected work, process evidence, proof, contact path.
- Useful materials: case-study artifacts, sketches, prototypes, before-after, project constraints.
- UX risks: style over evidence, confusing navigation, weak project summaries.
- Avoid: trend aesthetics that could belong to any portfolio.

### Service Or Booking Business

- Likely pattern: service promise, eligibility or fit, proof, process, booking action, contact.
- Useful materials: appointment slots, location, staff, pricing, trust markers, FAQs.
- UX risks: unclear next step, missing trust, hidden constraints, weak mobile booking flow.
- Avoid: beauty shots without task clarity.

### Finance Or High-Trust Product

- Likely pattern: trust thesis, safety controls, clear numbers, comparison, compliance or support, action.
- Useful materials: balances, limits, permissions, verification, audit state, risk labels.
- UX risks: low contrast, ambiguous status, overplayful visuals, unclear consequences.
- Avoid: speculative performance claims and decorative volatility.

## Validation Gate

The selected pattern must answer why this structure fits this product and user job. If the page could work for an unrelated product by only swapping copy, revise the pattern.
