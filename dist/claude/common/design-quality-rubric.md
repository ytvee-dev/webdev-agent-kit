---
id: 'agents.common.design-quality-rubric'
title: 'Design Quality Rubric'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'docs/design'
    - 'quality/design'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/frontend-design-director/SKILL|Frontend Design Director]]'
    - '[[common/anti-template-defaults|Anti-Template Defaults]]'
    - '[[common/interface-copy-rules|Interface Copy Rules]]'
    - '[[common/motion-rules|Motion Rules]]'
depends_on: []
---

# Design Quality Rubric

Purpose: evaluate whether a frontend design direction or rendered UI is clear, specific, implementable, and resistant to generic AI defaults.

## Verdicts

Use one verdict:

```text
pass
pass with concerns
fail
```

## Dimensions

### Clarity

- The screen has one primary job.
- The hierarchy makes the primary job obvious.
- The user can tell what to do next.

### Hierarchy

- Layout, spacing, typography, and emphasis agree.
- Important elements are not visually equal to secondary elements.
- Groups are visually meaningful.

### Specificity

- The design is tied to the subject, product, and audience.
- The hero or lead section expresses the page thesis.
- The signature element is meaningful, not decorative filler.

### Consistency

- Typography, spacing, color, radius, depth, and interaction patterns follow a system.
- Existing project tokens and conventions are reused when available.
- New tokens are justified and minimal.

### Responsiveness

- The layout has an explicit desktop, tablet, and mobile behavior when relevant.
- Text wrapping, overflow, and density are considered.
- The mobile model is not an afterthought.

### Accessibility

- Semantic structure is plausible.
- Focus states and keyboard paths are considered for interactive elements.
- Contrast and reduced motion are considered.

### Copy Quality

- Interface copy helps the user understand or act.
- Labels classify real meaning.
- Buttons name actions by outcome.
- Errors and empty states guide the next step.

### Motion Restraint

- Motion clarifies state, hierarchy, transition, or subject atmosphere.
- Motion is not used to hide weak layout.
- Reduced motion behavior is respected.

### Implementation Feasibility

- The design can be implemented with the current stack and project constraints.
- It does not require unapproved packages, UI libraries, animation libraries, or architecture changes.
- It has clear handoff notes.

### Anti-Template Resistance

- The design does not rely on generic SaaS defaults.
- Decorative numbers, badges, gradients, glass, glow, and fake metrics are justified or removed.
- The UI would not fit any unrelated product with only text swapped.

## Hero Rule

A hero section must express the page's central thesis.

Do not default to:

- fake metrics;
- gradient blobs;
- generic three-card support blocks;
- vague marketing slogans;
- decorative badges;
- meaningless screenshots.

If the hero could fit any SaaS product, it fails the design direction check.

## Restraint Rule

Spend boldness in one place.

- Minimal design requires precision.
- Maximal design requires high execution quality.
- If every block tries to be memorable, the design fails.
- Remove decoration that does not serve the brief.

## Review Output

When using this rubric, return:

```text
Verdict
Strongest Design Decisions
Concerns
Blocking Issues
Optional Improvements
Evidence
Next Step
```
