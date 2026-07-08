---
id: 'agents.common.frontend-implementation-boundaries'
title: 'Frontend Implementation Boundaries'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/anti-patterns/no-test-authoring-by-default|No Test Authoring By Default]]'
    - '[[common/anti-patterns/no-unapproved-test-infrastructure|No Unapproved Test Infrastructure]]'
depends_on: []
---

# Frontend Implementation Boundaries

Use English instructions and Unix-style paths.

Use existing CSS variables only.

Create no new project tests.

Do not create or edit component tests, hook tests, function or unit tests, integration tests, E2E tests, snapshots, fixtures, or mocks unless the user explicitly asks for test authoring and approves the exact target scope.

Introduce no project-code loops except a named isolated utility when no practical alternative exists.

Split hard-to-read chains into named variables and helpers.

Name behavior-bearing functions.

Apply only the Open-Closed Principle from SOLID when adding variants or behavior branches.
