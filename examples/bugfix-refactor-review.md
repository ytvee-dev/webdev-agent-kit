---
id: 'agents.examples.bugfix-refactor-review'
title: 'Bugfix Refactor Review Example'
doc_type: 'example'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/example'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/frontend-bugfix-debugger/SKILL|Frontend Bugfix Debugger]]'
    - '[[skills/frontend-refactor-surgeon/SKILL|Frontend Refactor Surgeon]]'
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
depends_on: []
---

# Bugfix Refactor Review Example

Bugfix prompt:

```text
The dashboard route renders blank on mobile. Reproduce it and fix the smallest
cause.
```

Refactor prompt:

```text
Refactor this settings panel into smaller components without changing behavior.
```

Review prompt:

```text
Review this frontend change for correctness, TypeScript safety, accessibility,
performance, and verification gaps.
```

What to expect:

- A review returns findings; it does not start an unrequested rewrite.
- A refactor preserves behavior unless you approve a change.
- The agent uses relevant existing checks. New tests need a separate request.
