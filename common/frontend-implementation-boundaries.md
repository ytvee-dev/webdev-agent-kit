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
    - '[[common/frontend-design-system-rules|Frontend Design System Rules]]'
    - '[[common/component-substitution-rules|Component Substitution Rules]]'
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

Name behavior-bearing functions and project-owned variables by their purpose or
domain content. Do not introduce bare `Item`, `Items`, `item`, or `items` names
for project-owned components, props, variables, helpers, or callback parameters.
Use names such as `WorkspaceOption`, `selectedMembers`, `logEntry`, and
`renderInvoiceRow`. Preserve externally mandated API fields; alias them at the
local boundary when helpful instead of breaking a public contract. Do not run
an unrelated mass rename. Confirm domain terms through existing project facts.

Apply the Open-Closed Principle for variants and behavior branches, and the
Liskov substitution principle for compatible component replacements under
`common/component-substitution-rules.md`. Shared UI work also follows
`common/frontend-design-system-rules.md`. Do not impose a full SOLID redesign.
