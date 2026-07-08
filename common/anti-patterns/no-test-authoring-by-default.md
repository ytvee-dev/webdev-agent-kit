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
    - '[[common/anti-patterns/no-unapproved-test-infrastructure|No Unapproved Test Infrastructure]]'
    - '[[common/verification-loop-rules|Verification Loop Rules]]'
depends_on: []
---

# No Test Authoring By Default

## Rule

Do not create or modify tests by default.

This includes component tests, hook tests, function or unit tests, integration tests, snapshots, fixtures, mocks, visual regression suites, and end-to-end flows.

Run existing verification commands when relevant, but create or change tests only when the user explicitly asks for test authoring and approves the exact target scope.

If a test would be useful but was not requested, report the verification gap and ask for approval instead of writing the test.

## Avoid

- Adding a test file because code changed.
- Creating `*.test.tsx`, `*.spec.tsx`, or `__tests__/**` for a component, hook, helper, or page because implementation changed.
- Updating unrelated tests while implementing a feature or bugfix.
- Creating fixtures, mocks, visual regression suites, or end-to-end flows without approval.
- Adding test dependencies, scripts, or framework setup.

## Allowed

```text
User: Add a regression test for this bug.
Agent: Proposes the exact test scope and changes only after approval.
```

## Bad

```ts
// A small CSS tweak creates a new test file.
describe('Background', () => {
  it('renders', () => {});
});
```

## Good

```text
Changed: one CSS module.
Verified: changed-file formatting.
Skipped: component and function test authoring was not requested.
```

## Apply When

Use this whenever an agent considers creating or editing tests, test scripts, test dependencies, fixtures, mocks, snapshots, or test infrastructure.
