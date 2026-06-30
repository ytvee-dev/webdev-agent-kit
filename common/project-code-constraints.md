---
id: 'agents.common.project-code-constraints'
title: 'Project Code Constraints'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'frontend/code-quality'
    - 'frontend/readability'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/approved-patterns|Approved Patterns]]'
    - '[[common/anti-patterns|Common Anti-Patterns]]'
    - '[[common/documentation-maintenance|Documentation Maintenance]]'
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
    - '[[skills/frontend-refactor-surgeon/SKILL|Frontend Refactor Surgeon]]'
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
depends_on: []
---

# Project Code Constraints

Purpose: define non-negotiable code and documentation constraints that apply before any frontend implementation, bugfix, refactor, review, or skill-authoring work.

## Documentation Language And Paths

- Write every reusable instruction, policy, skill, reference, template note, and project overlay in English.
- Use Unix-style paths only: `path/name/file.md`.
- Do not write Windows-style paths such as `path\\name\\file.md` in Markdown links, references, examples, commands, validation output, or final reports.
- Convert user-provided Windows-style paths to Unix-style paths before writing docs or comments.

## CSS Variables And Tokens

- Never invent CSS variables, design tokens, theme names, breakpoint names, spacing variables, typography variables, or color variables.
- Before using a CSS variable, prove it exists in the current project source, project overlays, copied inspect values, or the user-provided spec.
- If the needed value has no existing variable, use the closest existing project-native primitive or ask the user. Do not create a global token or theme variable without explicit approval.
- New CSS custom properties are allowed only when the edited file already owns a local component-scoped variable pattern and the new variable is local to that file or component.
- Do not hardcode broad reusable colors, spacing, typography, z-index, radius, or shadow values when an existing token or local owner exists.

## Tests

- Do not create new tests in host projects.
- Do not add test files, test snapshots, visual regression tests, unit tests, component tests, end-to-end tests, test scripts, test setup, test dependencies, or test framework config.
- Do not modify existing tests unless the user explicitly asks to edit a specific existing test file.
- Existing tests in a project do not authorize writing new tests.

## Iteration And Readability

- Do not introduce loops in host project code.
- Forbidden loop forms include `for`, `for...of`, `for...in`, `while`, `do...while`, `forEach`, reducers used as loops, manual accumulator mutation, and hidden render arrays.
- Do not hide iteration inside unreadable array chains.
- Break transformation chains into named intermediate variables and named helper functions when an existing chain must be preserved.
- Do not write long chained expressions that combine nullish fallback, mapping, filtering, sorting, slicing, and returning in one statement.
- Do not use anonymous functions to hide behavior. Name components, handlers, predicates, mappers, formatters, selectors, and helpers.
- A loop exception is allowed only inside a small isolated utility when there is no practical non-loop alternative. The exception must be named, local, documented in the final report, and must not appear inside components, routes, state slices, effects, render logic, or business orchestration.

## Readable Chain Shape

Do not write this shape:

```ts
return (notification.content.actions ?? [])
    .map(getAcceptDeclineActionMapper(notification.id))
    .filter(isNotificationCardAction)
    .slice(0, MAX_NOTIFICATION_ACTIONS);
```

Use named steps instead:

```ts
const notificationActions = notification.content.actions ?? [];
const acceptDeclineActionMapper = getAcceptDeclineActionMapper(notification.id);
const mappedActions = notificationActions.map(acceptDeclineActionMapper);
const cardActions = mappedActions.filter(isNotificationCardAction);
const visibleActions = cardActions.slice(0, MAX_NOTIFICATION_ACTIONS);

return visibleActions;
```

If the project task also forbids array iteration for the touched surface, move the transformation into an existing utility or ask before adding a new utility.

## Open-Closed Principle

- Apply the Open-Closed Principle from SOLID when adding variants, statuses, actions, UI states, or behavior branches.
- Prefer extending a typed lookup table, strategy map, adapter map, or configuration object over editing a long conditional chain.
- Do not use this rule to introduce unnecessary architecture layers. Keep the extension point local and project-native.
- Do not apply other SOLID principles as additional requirements unless the user explicitly asks for them.

## Validation Gates

- No new or modified documentation may contain Windows-style paths.
- No changed CSS may reference a non-existent variable or invented token.
- No new tests or test setup may be created.
- No project code may introduce loops except for the explicit isolated utility exception.
- No anonymous function may hide meaningful behavior.
- No hard-to-read chain may remain in touched code when it can be split into named steps.
- New variants or branches must be checked against the Open-Closed Principle before final reporting.
