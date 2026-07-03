---
id: 'agents.skills.frontend-design-director.references.design-direction-contract'
title: 'Design Direction Contract Reference'
doc_type: 'reference'
layer: 'skill-reference'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/design'
    - 'workflow/design-direction'
parent:
    - '[[skills/frontend-design-director/SKILL|Frontend Design Director]]'
related:
    - '[[templates/design-direction-contract|Design Direction Contract Template]]'
    - '[[common/design-quality-rubric|Design Quality Rubric]]'
depends_on: []
---

# Design Direction Contract Reference

A Design Direction Contract is the handoff artifact between visual judgment and frontend implementation.

It must be concrete enough that another agent can implement the UI without inventing a generic design system.

## Required Fields

```text
Subject
Audience
Single Job
Product Context
Lead / Hero Thesis
Design Dials
Visual Position
Design Risk
Signature Element
Token System
Typography Roles
Structure As Information
Layout Concept
Motion Stance
Interface Copy Voice
Anti-Template Checks
Implementation Handoff Notes
Visual Acceptance Criteria
```

## Subject

Name the concrete thing being designed. Avoid vague subjects such as `dashboard`, `app`, or `landing page` without domain context.

## Audience

Name who the interface serves and what density, tone, and complexity they can tolerate.

## Single Job

State the one main job the screen must perform. Every major layout decision should support this job.

## Lead / Hero Thesis

State what the first screen must prove, which subject-specific material opens the page, and why the lead cannot be reused for an unrelated product by swapping copy.

## Design Dials

Record visual variance, motion intensity, and information density on a 1-10 scale with a reason and responsive implication. Treat the values as directional constraints, not style presets.

## Visual Position

Use a short phrase that defines the interface character, such as:

```text
calm technical
editorial and precise
dense professional tool
premium but restrained
playful educational
minimal architectural
```

## Design Risk

Define one justified visual risk. The risk must support the subject or audience.

## Signature Element

Define one memorable element tied to the subject. It may be visual, structural, or interaction-based. It must not become decoration repeated everywhere.

## Token System

Define a compact token system that can map to existing project tokens when possible:

```text
4-6 colors
2-3 typography roles
spacing rhythm
border and radius stance
shadow or depth stance
```

## Typography Roles

Define display, body, and utility or data roles plus scale, weight rhythm, line height, letter spacing, and where typography carries personality.

## Structure As Information

Explain what numbering, dividers, badges, labels, grids, and metrics communicate. Remove structural devices that do not encode sequence, grouping, classification, status, comparison, or another real relationship.

## Layout Concept

Explain hierarchy and composition. Use a small ASCII wireframe when it helps implementation.

## Motion Stance

State whether motion is needed. If yes, name the one motion idea and its purpose. Always respect reduced motion.

## Interface Copy Voice

Define how labels, actions, empty states, and errors should speak to the user.

## Anti-Template Checks

Name the generic defaults this design must avoid.

## Visual Acceptance Criteria

Use concrete visual criteria that can be checked by screenshot or rendered UI review.
