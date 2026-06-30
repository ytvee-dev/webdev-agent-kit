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
related: []
depends_on: []
---

# Frontend Implementation Boundaries

Use English instructions and Unix-style paths.

Use existing CSS variables only.

Create no new project tests.

Introduce no project-code loops except a named isolated utility when no practical alternative exists.

Split hard-to-read chains into named variables and helpers.

Name behavior-bearing functions.

Apply only the Open-Closed Principle from SOLID when adding variants or behavior branches.
