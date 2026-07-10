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
    - '[[common/test-policy|Test Change And Verification Policy]]'
    - '[[common/anti-patterns/no-test-authoring-by-default|No Test Authoring By Default]]'
    - '[[common/anti-patterns/no-unapproved-test-infrastructure|No Unapproved Test Infrastructure]]'
depends_on: []
---

# Frontend Implementation Boundaries

Use English instructions and Unix-style paths.

Use existing CSS variables only.

Create no new project tests unless the current user explicitly requests the named test scope. Maintain an existing directly affected test only when the approved task changed its confirmed behavior contract; follow `common/test-policy.md`.

Introduce no project-code loops except a named isolated utility when no practical alternative exists.

Split hard-to-read chains into named variables and helpers.

Name behavior-bearing functions.

Apply only the Open-Closed Principle from SOLID when adding variants or behavior branches.
