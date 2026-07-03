---
id: 'agents.common.form-feedback-rules'
title: 'Form Feedback Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'frontend/forms'
    - 'quality/ux'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/interface-copy-rules|Interface Copy Rules]]'
    - '[[common/ui-ux-priority-checklist|UI UX Priority Checklist]]'
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
depends_on: []
---

# Form Feedback Rules

Purpose: keep form UI understandable, recoverable, accessible, and implementable with project-native frontend patterns.

Use when implementing, reviewing, debugging, or visually verifying inputs, filters, search fields, auth forms, checkout steps, settings forms, upload flows, destructive confirmations, or multi-step flows.

## Core Rules

- Use persistent labels for inputs. Do not rely on placeholder-only labels.
- Place field-level errors close to the related field.
- Use helper text when the user needs format, scope, or consequence guidance.
- Validate after the user has had a reasonable chance to finish input, such as on blur or submit, unless the existing project convention differs.
- After submit errors, make the first invalid field easy to find; use focus management when the project already supports it.
- Async submission should communicate loading, success, and failure states when the action is not instant.
- Prevent duplicate destructive or expensive submissions while an action is pending.
- Destructive or irreversible actions need confirmation, undo, or a clearly separated danger path.
- Long or high-risk forms should preserve user work when the existing architecture supports draft, autosave, or route state.
- Use semantic input types and autocomplete attributes when they are appropriate and project conventions allow them.

## Empty, Loading, Error, And Success States

### Empty

An empty state should answer:

```text
What is missing?
Why does it matter?
What can the user do next?
```

### Loading

Loading state should clarify that work is happening. Do not add motion or personality when a disabled label, spinner, skeleton, or progress state is enough.

### Error

An error should answer:

```text
What happened?
Which field or action caused it when known?
What can the user do now?
```

### Success

Success feedback should confirm completion without stealing attention from the next task.

## Accessibility Rules

- Error messages must be reachable by assistive technology when the project has a pattern for `aria-describedby`, `aria-live`, or alert semantics.
- Do not use color alone for validation state.
- Disabled controls must be semantically disabled, not only visually muted.
- Required fields must be understandable without relying on color or vague punctuation alone.
- Toasts should not steal focus unless the existing project pattern intentionally does so for critical alerts.

## Implementation Boundaries

- Reuse existing form primitives, validation helpers, API adapters, Redux or local state ownership, and CSS Modules conventions.
- Do not introduce form libraries, validation libraries, toast systems, test frameworks, or new state layers without explicit user approval.
- Do not move domain processing into Redux to make a form easier to wire.

## Validation Gate

Before final reporting, verify that the form has clear labels, relevant states, recovery copy, focus or location behavior for errors, and no placeholder-only critical labels unless the existing project explicitly uses that pattern.
