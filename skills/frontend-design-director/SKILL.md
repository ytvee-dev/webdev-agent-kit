---
name: frontend-design-director
description: Use for standard or deep frontend UI work that needs subject-grounded visual direction, redesign, visual polish, design critique, anti-template checks, or design handoff before implementation. Do not use for purely technical micro-fixes or isolated code edits.
id: 'agents.skills.frontend-design-director.skill'
title: 'Frontend Design Director'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-design-director'
tags:
    - 'agents/skill-package'
    - 'agents/design'
    - 'workflow/design-direction'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[common/prompt-intent-routing-rules|Prompt Intent Routing Rules]]'
    - '[[common/design-quality-rubric|Design Quality Rubric]]'
    - '[[common/anti-template-defaults|Anti-Template Defaults]]'
    - '[[common/interface-copy-rules|Interface Copy Rules]]'
    - '[[common/motion-rules|Motion Rules]]'
    - '[[skills/design-screenshot-spec/SKILL|Design Screenshot Spec]]'
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Frontend Design Director

## Purpose

Define a concrete, subject-grounded frontend design direction before implementation when a task requires visual judgment.

This skill prevents generic AI-generated UI by making deliberate choices about audience, single job, visual position, hierarchy, typography, color, layout, motion, interface copy, and anti-template risks.

It does not implement code by default. It creates a design direction contract that can be handed to `frontend-layout-implementer` and verified by `frontend-visual-qa` or `frontend-quality-reviewer`.

## When To Use

Use this skill after prompt intent routing when the task is `Standard Workflow` or `Deep Workflow` and includes visual judgment.

Use this skill when the user asks to:

- create a new UI;
- redesign an existing UI;
- improve visual quality;
- make a page more distinctive;
- create or reshape a landing page;
- create or reshape a dashboard;
- turn a vague visual request into a concrete direction;
- critique generic AI-looking UI;
- define visual acceptance criteria before implementation;
- adapt a screenshot, visual reference, or design brief into a stronger frontend direction.

## When Not To Use

Do not use this skill for:

- one small bug;
- one obvious type error;
- one direct file-scope edit;
- one isolated code refactor;
- purely technical debugging;
- backend, database, or infrastructure work;
- UI component library selection;
- testing workflows.

Do not use this skill as a required step for every frontend task. Use it only when design judgment affects the current slice.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/prompt-intent-routing-rules.md` when workflow level is unclear.
3. Read only relevant project overlays:
   - `project/stack-profile.md`;
   - `project/styling-profile.md`;
   - `project/design-reference-profile.md`;
   - `project/visual-memory.md` when present;
   - `project/active-goals.md` or the compact goal contract when present.
4. Read supplied screenshots, design references, copied inspect values, or written brief.
5. Read affected route or component files only when existing project constraints are needed.
6. Do not read all source files, all skills, all references, or `SUMMARY.md` for routing.

## Tool Contract

- May use filesystem access to read relevant project overlays and write design artifacts only when the task requires durable handoff.
- May use Browser or Playwright screenshots when a rendered UI already exists and screenshot critique is needed.
- May use MDN or official platform docs for CSS, accessibility, motion, or browser behavior details when needed.
- May use `context7` for framework-specific UI constraints when relevant.
- Must not use Figma MCP for the screenshot-only bundle workflow.
- Must not install UI libraries, animation libraries, testing libraries, packages, or MCP servers.
- Must not implement code unless the user explicitly asked for implementation and the execution plan includes a separate implementation slice.

## Workflow

1. Confirm visual task scope.
   - If the task is lightweight and purely technical, stop and route to the direct technical skill.
   - If visual direction matters, continue.

2. Ground the design.
   Define:
   - subject;
   - audience;
   - single job;
   - product context;
   - workflow level.

3. Identify existing constraints.
   - Existing typography system.
   - Existing colors and tokens.
   - Existing layout patterns.
   - Existing component conventions.
   - Accessibility and responsive constraints.
   - Visual memory or rejected directions.

4. Explore compact directions.
   Produce two or three concise direction options only when the task is ambiguous. For a clear brief, produce one direction.

5. Select or recommend a direction.
   Explain why the selected direction fits the subject, audience, and single job.

6. Define the Design Direction Contract.
   Include:
   - subject;
   - audience;
   - single job;
   - visual position;
   - design risk;
   - signature element;
   - token system;
   - layout concept;
   - typography roles;
   - motion stance;
   - interface copy voice;
   - anti-template checks;
   - acceptance criteria.

7. Run anti-template review.
   Check for:
   - generic SaaS hero;
   - fake metrics;
   - meaningless feature grids;
   - decorative badges or numbers;
   - unjustified glass, glow, gradients, or shadows;
   - typography without purpose;
   - motion used to hide weak structure.

8. Prepare implementation handoff.
   Hand off to `frontend-layout-implementer` only after the design direction is concrete enough to implement.

9. Prepare verification handoff.
   Define visual acceptance criteria that `frontend-visual-qa` or `frontend-quality-reviewer` can verify.

## Output Contract

Return or write a Design Direction Contract with:

```text
Subject
Audience
Single Job
Product Context
Visual Position
Design Risk
Signature Element
Token System
Typography Roles
Layout Concept
Motion Stance
Interface Copy Voice
Anti-Template Checks
Implementation Handoff Notes
Visual Acceptance Criteria
Next Skill Or Next Step
```

Use `templates/design-direction-contract.md` for durable handoff when needed.

## Validation Gates

Before finishing, verify:

- the task actually needed design judgment;
- the direction is grounded in the subject and audience;
- the screen has one primary job;
- at least one signature element is defined when creating or redesigning a major page;
- typography, color, layout, and motion choices have reasons;
- anti-template checks were applied;
- no UI component library skill was introduced;
- no testing workflow was introduced;
- no source code was changed by this skill unless a separate implementation slice was explicitly requested.

## Trigger Evals

Should trigger:

- "Make this dashboard look less generic before implementation."
- "Create a visual direction for this landing page."
- "Redesign this screen from the screenshot and make it distinctive."
- "Define the design contract before coding this UI."
- "Review this page for AI-template design issues."

Should not trigger:

- "Fix this TypeScript error."
- "Change this button color to #333."
- "Rename this prop in one component."
- "Run visual QA on the already implemented page."
- "Install a UI library."
- "Create tests."

## Reference Map

- `AGENTS.md` - canonical policy, routing, tool rules, and documentation rules.
- `common/prompt-intent-routing-rules.md` - workflow weight selection and escalation rules.
- `common/design-quality-rubric.md` - design review dimensions and verdicts.
- `common/anti-template-defaults.md` - suspicious generic UI defaults.
- `common/interface-copy-rules.md` - copy as part of interface design.
- `common/motion-rules.md` - motion restraint and reduced-motion rules.
- `templates/design-direction-contract.md` - durable design direction artifact.
- `templates/visual-memory.md` - local-only project visual memory template.
