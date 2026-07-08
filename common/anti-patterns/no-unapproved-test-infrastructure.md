---
id: 'agents.common.anti-patterns.no-unapproved-test-infrastructure'
title: 'No Unapproved Test Infrastructure'
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
    - '[[common/anti-patterns/no-test-authoring-by-default|No Test Authoring By Default]]'
    - '[[common/verification-loop-rules|Verification Loop Rules]]'
depends_on: []
---

# No Unapproved Test Infrastructure

## Rule

Run existing project tests only when they are already part of the relevant verification path. Do not create or edit tests by default.

Create or update component tests, hook tests, function or unit tests, integration tests, E2E tests, snapshots, fixtures, or mocks only when the user explicitly asks for test authoring and approves the exact target scope.

Do not add a testing framework, setup layer, script, dependency, broad fixture system, end-to-end suite, or visual-regression infrastructure without explicit user approval.

## Avoid

- Adding test tooling merely because the agent prefers another framework.
- Creating a regression test when the user asked only for an implementation fix.
- Creating a component or helper test as a side effect of changing the component or helper.
- Rewriting unrelated tests while implementing a feature or bugfix.
- Treating a green unrelated test as proof that the changed behavior works.
- Skipping a relevant existing verification command because no new test was requested.

## Verification

- Run the relevant existing test only when changed behavior is already covered and the verification budget calls for it.
- Report the exact test command and result when an existing test was run.
- If a test would be useful but was not requested or would need new infrastructure, report the gap and approval needed.

## Apply When

Use this whenever an agent considers changing tests, test scripts, test dependencies, test setup, or the verification plan.
