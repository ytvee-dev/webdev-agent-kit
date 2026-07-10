---
id: 'agents.common.anti-patterns.no-test-authoring-by-default'
title: 'No Test Authoring By Default'
doc_type: 'anti-pattern-template'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'anti-patterns/testing'
parent:
    - '[[common/anti-patterns/README|Anti-Pattern Templates]]'
related:
    - '[[common/test-policy|Test Change And Verification Policy]]'
    - '[[common/anti-patterns/no-unapproved-test-infrastructure|No Unapproved Test Infrastructure]]'
    - '[[common/verification-loop-rules|Verification Loop Rules]]'
depends_on: []
---

# No Test Authoring By Default

## Rule

Do not create new tests by default.

This includes new component, hook, function, unit, integration, E2E, snapshot, fixture, mock, and visual-regression cases.

Run relevant existing tests. Maintain an existing test only when it directly covers a confirmed behavior contract changed by the approved task, as defined in `common/test-policy.md`.

If a new regression test would be useful but was not requested, propose its exact scope only when the missing coverage is a material verification gap.

## Avoid

- Adding a test file because code changed.
- Creating `*.test.tsx`, `*.spec.tsx`, or `__tests__/**` for a component, hook, helper, or page because implementation changed.
- Updating unrelated tests while implementing a feature or bugfix.
- Creating fixtures, mocks, visual regression suites, or end-to-end flows without approval.
- Adding test dependencies, scripts, or framework setup.

## Allowed

```text
User: Add a regression test for this bug.
Agent: Adds the smallest local regression case using existing test infrastructure.
```

```text
User: Change this confirmed validation contract and update its existing tests.
Agent: Updates only the directly affected assertions and runs the relevant test command.
```

## Bad

```ts
// A small CSS tweak creates a new test file.
describe('Background', () => {
  it('renders', () => {});
});
```

## Reporting

Do not mention skipped test authoring for a CSS-only or unrelated code change. Report tests only when they were run, changed, blocked, explicitly requested, or represent a material gap.

## Apply When

Use this whenever an agent considers creating a test or changing an existing test, test script, dependency, fixture, mock, snapshot, or test infrastructure.
