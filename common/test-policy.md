---
id: 'agents.common.test-policy'
title: 'Test Change And Verification Policy'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'testing/policy'
    - 'verification/scope'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/verification-loop-rules|Verification Loop Rules]]'
    - '[[common/smart-verification-budget|Smart Verification Budget]]'
    - '[[common/anti-patterns/no-test-authoring-by-default|No Test Authoring By Default]]'
    - '[[common/anti-patterns/no-unapproved-test-infrastructure|No Unapproved Test Infrastructure]]'
depends_on:
    - '[[common/policy-precedence|Policy Precedence]]'
---

# Test Change And Verification Policy

Purpose: separate relevant existing-test verification and maintenance from unrequested test authoring or infrastructure expansion.

## Allowed Without Extra Approval

- Run the smallest relevant existing test command when it covers changed behavior or is a verified project gate.
- Fix an existing test that directly covers a confirmed behavior contract changed by the approved task.
- Maintain a local assertion, snapshot, fixture, or mock already owned by that existing test when the same confirmed contract changed.
- Repair an existing test's imports or setup when an approved behavior-preserving refactor moved its owner.

Existing-test edits must stay inside the changed behavior boundary. If a failure exposes a product defect rather than a stale expectation, fix the product code instead of weakening the test.

## Explicit Request Or Approval Required

- Create a new test file or new test case, including a local regression test.
- Install a test framework, runner, dependency, browser, or service.
- Add or change test scripts, configuration, global setup, CI jobs, or coverage gates.
- Create broad fixtures, shared mocks, snapshot baselines, visual-regression infrastructure, E2E suites, or testing architecture.
- Run unrelated full suites when they are not a verified project gate for the changed surface.
- Expand test edits beyond the changed behavior or confirmed contract.

An explicit request to add the named regression test authorizes that local test within scope. A request to fix tests authorizes relevant existing-test repair, not new infrastructure or unrelated test creation.

## Low-Risk And CSS-Only Changes

CSS-only, copy-only, and other low-risk presentation changes do not create component, unit, integration, E2E, snapshot, fixture, mock, or visual-regression tests. Use the smallest relevant source, lint, build, or rendered check instead.

## Reporting

Mention tests only when a test was run, changed, failed, blocked, explicitly requested, or represents a material verification gap requiring a decision. Do not add routine output such as `Skipped: test authoring was not requested`.

When tests matter, report the exact command or file, result, scope, and any approval needed. Do not present an unrelated green suite as proof of the changed behavior.

## Validation Gates

- Existing-test maintenance follows a confirmed changed contract.
- New tests and infrastructure have explicit current user authorization.
- Verification stays proportional and relevant.
- Final output omits non-actionable skipped-test noise.
