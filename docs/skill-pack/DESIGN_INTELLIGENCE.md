# Design Intelligence Architecture

Status: draft architecture.
Scope: design judgment, anti-template defaults, visual direction, screenshot critique, visual memory, and frontend design quality gates.

## Purpose

The design intelligence layer prevents the agent from producing generic AI-generated UI. It adds deliberate visual judgment before implementation and design-aware verification after implementation.

The layer is inspired by the Anthropic `frontend-design` skill, but it is adapted for WebDev Assistant as a reusable frontend engineering skill pack layer.

## Design Role

Future skill:

```text
frontend-design-director
```

Role:

```text
Act as a design lead for frontend work. Define a subject-grounded visual direction, make deliberate choices about palette, typography, layout, structure, motion, and interface copy, and protect the implementation from templated defaults.
```

## When To Use

Use `frontend-design-director` when the user asks to:

- create new UI;
- redesign an existing UI;
- visually polish a screen;
- create a landing page;
- create a dashboard;
- make an interface more distinctive;
- improve layout, typography, spacing, or color;
- turn a vague design request into a concrete visual direction;
- detect generic AI UI.

Do not use it for purely technical bugfixes, documentation-only tasks, or behavior-preserving refactors unless the task includes visual judgment.

## Design Direction Contract

Target template:

```text
templates/design-direction-contract.md
```

Required fields:

```text
Subject
Audience
Single Job
Product Context
Visual Position
Design Risk
Signature Element
Token System
Layout Concept
Motion
Interface Copy Voice
Anti-Template Checks
Acceptance Criteria
```

### Subject

The subject is the concrete thing being designed. If the brief does not specify it, the agent must pick one concrete subject and state the choice before design work continues.

### Audience

The audience defines who the interface serves and what level of density, clarity, tone, and visual risk is appropriate.

### Single Job

Every screen must have one primary job. Visual hierarchy should make that job obvious.

### Visual Position

The visual position names the intended character of the interface.

Examples:

```text
calm
technical
editorial
dense
premium
playful
utilitarian
experimental
architectural
minimal
```

### Design Risk

Each major design direction should take one justified aesthetic risk. The risk must serve the subject or audience. It must not be arbitrary decoration.

### Signature Element

A signature element is one memorable visual or interaction element grounded in the subject.

Rules:

- one signature element per screen or page;
- grounded in product context;
- not decorative filler;
- not repeated everywhere;
- restrained by the rest of the layout.

Examples:

```text
AI update feed -> update diff lens or source credibility rail
Frontend course -> code-to-screen split panel
Personal technical blog -> architectural graphite-and-glass sketch motif
Dashboard -> status topology map rather than generic metric cards
```

## Design Principles

### Hero Is A Thesis

A hero section must express the page's central thesis.

Do not default to:

- big number with a small label;
- fake metrics;
- generic gradient blobs;
- three generic supporting stats;
- empty marketing language.

Use headline, image, interaction, demo, data, or motion only when it expresses the subject.

If the hero could fit any SaaS product, it fails the design direction check.

### Typography Carries Personality

Typography is not neutral filler. The design direction must define at least:

```text
display role
body role
utility/data role when labels, captions, metrics, tables, or code are present
```

The agent must define:

- type scale;
- weight strategy;
- line-height;
- letter spacing where relevant;
- density;
- why the type treatment fits the subject.

For existing projects, map the direction to existing typography tokens before proposing new fonts.

### Structure Is Information

Structural devices must encode meaning.

Allowed when meaningful:

- numbering for real sequence;
- dividers for real grouping;
- labels for real classification;
- badges for status or semantic difference;
- timeline for actual time/order;
- grid for comparable items.

Slop patterns:

- numbered cards without sequence;
- decorative eyebrows;
- badges that do not change user understanding;
- dividers that only decorate;
- grids that make unrelated things look equivalent;
- timeline layout without actual time or order.

### Spend Boldness In One Place

Use one bold design move and keep the rest disciplined.

Rules:

- minimal design requires precision in spacing, type, and detail;
- maximal design requires enough execution quality to support complexity;
- if every block tries to be memorable, the design fails;
- remove decoration that does not serve the brief.

### Motion Must Serve Meaning

Motion is useful when it clarifies state, hierarchy, transition, or subject atmosphere.

Rules:

- prefer one orchestrated motion moment over scattered effects;
- respect reduced motion;
- do not add animation to hide weak layout;
- do not animate generic content just to make it feel premium;
- verify hover, focus, transition, and reduced-motion behavior when motion is used.

## Anti-Template Defaults

Target file:

```text
common/anti-template-defaults.md
```

Suspicious defaults:

- cream editorial page with serif display and terracotta accent;
- black page with acid green or vermilion accent;
- broadsheet/newsprint layout with dense columns and hairline rules;
- generic SaaS hero with gradient blobs and fake metrics;
- three-card feature grid without hierarchy;
- glass cards and glow effects without subject reason;
- fake dashboard numbers;
- random icons used as filler;
- oversized border radius everywhere;
- shadows used as a substitute for hierarchy.

These styles are not banned. They are banned only when used automatically without a subject-grounded reason.

## Interface Copy Rules

Target file:

```text
common/interface-copy-rules.md
```

Rules:

- words are design material;
- write from the user's side, not the system's internals;
- name actions by what happens;
- keep action vocabulary consistent across buttons, toasts, modals, and states;
- use active voice by default;
- prefer specific over clever;
- errors explain what happened and how to fix it;
- empty states invite the next action;
- one element, one job: label labels, example demonstrates, button acts.

## Screenshot Critique And Repair Loop

Visual work should use rendered screenshots when browser tooling is available.

Loop:

```text
1. Render current UI.
2. Capture screenshot.
3. Compare against design direction contract, design spec, or reference.
4. Classify deviations:
   - layout
   - spacing
   - typography
   - color
   - responsive
   - interaction
   - accessibility
   - copy
5. Fix one class of deviation.
6. Capture screenshot again.
7. Record evidence and remaining deviations.
8. Stop after one repair slice unless the active plan says to continue.
```

## Visual Memory

Target file:

```text
project/visual-memory.md
```

Purpose:

- avoid repeating the same visual ideas;
- remember accepted and rejected directions;
- record project-specific visual preferences;
- improve future design continuity.

Fields:

```text
Tried Directions
Strong Local Preferences
Rejected Defaults
Successful Patterns
Avoid Repeating
Last Updated
```

## CSS Specificity Gate

UI implementation must avoid CSS conflicts that make rendered output diverge from design intent.

Rules:

- spacing must have one owner;
- parent layout rhythm should come before child margin hacks;
- avoid generic section classes fighting component classes;
- avoid element selectors overriding component or utility selectors;
- avoid global styles that change unrelated screens;
- inspect computed styles when rendered output differs from authored CSS;
- do not add tokens or global classes when a local styling owner exists.

## Design Quality Rubric

Target file:

```text
common/design-quality-rubric.md
```

Rubric dimensions:

```text
Clarity
Hierarchy
Specificity
Consistency
Responsiveness
Accessibility
Copy Quality
Motion Restraint
Implementation Feasibility
Anti-Template Resistance
```

Verdict:

```text
pass
pass with concerns
fail
```

## Pipeline: New UI Or Redesign

```text
goal-planner
-> execution-plan-manager
-> frontend-design-director
-> frontend-layout-implementer
-> frontend-visual-qa
-> frontend-quality-reviewer
-> project-context-adapter when project facts changed
```

## Pipeline: Screenshot Reference

```text
design-screenshot-spec
-> frontend-design-director when design judgment is needed
-> frontend-layout-implementer
-> frontend-visual-qa
-> frontend-quality-reviewer
```

## Token Budget Rules For Design Work

The design layer must read only:

```text
AGENTS.md
project/stack-profile.md
project/styling-profile.md
project/design-reference-profile.md
project/visual-memory.md
project/active-goals.md
project/active-plan.md
affected route/component files when needed
```

Do not read:

```text
all skills
all references
all source files
SUMMARY.md for runtime routing
```

## Output Contract

`frontend-design-director` should output:

```text
Design Direction Contract
Design Risk
Signature Element
Token System
Layout Concept
Anti-Template Checks
Implementation Handoff Notes
Visual Acceptance Criteria
```

It should not implement code unless the user explicitly asks for implementation in the same task and the execution plan includes that slice.
