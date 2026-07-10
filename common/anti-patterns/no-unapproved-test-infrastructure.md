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
    - '[[common/test-policy|Test Change And Verification Policy]]'
    - '[[common/anti-patterns/no-test-authoring-by-default|No Test Authoring By Default]]'
    - '[[common/verification-loop-rules|Verification Loop Rules]]'
depends_on: []
---

# No Unapproved Test Infrastructure

## Rule

Run existing project tests when they are part of the relevant verification path.

Maintain an existing directly affected test when a confirmed behavior contract changed. Creating a new test still requires an explicit current user request.

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
- Update the smallest existing assertion, fixture, mock, snapshot, import, or setup owned by a confirmed changed contract.
- Report the exact test command and result when an existing test was run.
- Report a missing-test gap only when it is material; request approval before new tests or infrastructure.

## Apply When

Use this whenever an agent considers changing tests, test scripts, test dependencies, test setup, or the verification plan.
