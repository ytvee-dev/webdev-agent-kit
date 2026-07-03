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
    - '[[common/verification-loop-rules|Verification Loop Rules]]'
depends_on: []
---

# No Unapproved Test Infrastructure

## Rule

Use existing project tests and testing conventions when they are the smallest reliable evidence for changed behavior.

Create or update a scoped regression test only when the user requests it, acceptance criteria require it, or the existing project convention makes it part of the approved task. Keep the test limited to changed behavior.

Do not add a testing framework, setup layer, script, dependency, broad fixture system, end-to-end suite, or visual-regression infrastructure without explicit user approval.

## Avoid

- Adding test tooling merely because the agent prefers another framework.
- Rewriting unrelated tests while implementing a feature or bugfix.
- Treating a green unrelated test as proof that the changed behavior works.
- Skipping a relevant existing test because the task did not create a new test.

## Verification

- Run the relevant existing test when changed behavior is already covered.
- Report the exact test command and result.
- If a required regression test is out of scope or needs new infrastructure, report the gap and approval needed.

## Apply When

Use this whenever an agent considers changing tests, test scripts, test dependencies, test setup, or the verification plan.

