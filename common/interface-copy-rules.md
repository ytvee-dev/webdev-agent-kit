---
id: 'agents.common.interface-copy-rules'
title: 'Interface Copy Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'docs/design'
    - 'quality/copy'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/frontend-design-director/SKILL|Frontend Design Director]]'
    - '[[common/design-quality-rubric|Design Quality Rubric]]'
depends_on: []
---

# Interface Copy Rules

Purpose: treat words as part of interface design, not as filler text.

## Core Rules

- Words are design material.
- Write from the user's side, not the system's internals.
- Name actions by what happens.
- Keep action vocabulary consistent across buttons, toasts, modals, and states.
- Use active voice by default.
- Prefer specific over clever.
- Do not use fake marketing copy to fill layout gaps.
- Do not invent dashboard numbers or outcomes to make UI look complete.

## One Element, One Job

- A label labels.
- A button acts.
- A caption clarifies.
- An example demonstrates.
- A badge communicates status or category.
- An empty state invites the next action.
- An error explains what happened and how to fix it.

## Action Copy

Good action copy names the result:

```text
Save draft
Invite teammate
Export report
Review changes
Connect account
```

Avoid vague actions unless the project convention requires them:

```text
Submit
Click here
Continue
Proceed
Get started
```

## State Copy

### Empty States

Empty states should answer:

```text
What is missing?
Why does it matter?
What can the user do next?
```

### Errors

Errors should answer:

```text
What happened?
What caused it if known?
What can the user do now?
```

### Loading

Loading copy should set expectation only when needed. Do not add personality to every loading state.

## Consistency Check

Before handoff, verify:

- buttons, labels, modals, and toasts use the same vocabulary;
- critical actions are not hidden behind clever wording;
- copy reflects the product context;
- empty and error states help the user recover;
- no lorem-like text remains in the design contract.
