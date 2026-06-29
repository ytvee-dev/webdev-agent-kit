---
id: 'agents.common.performance-review-rules'
title: 'Performance Review Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'workflow/performance-review'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
depends_on: []
---

# Performance Review Rules

Purpose: focus frontend performance review on evidence and user-visible risk.

## Rules

- Prioritize render-blocking work, excessive client bundles, repeated expensive
  renders, layout shift, image misuse, unnecessary network waterfalls, and
  avoidable hydration or route-load cost.
- Prefer existing project metrics, browser evidence, and framework build output
  over speculative optimization.
- Do not add caching, memoization, virtualization, build tooling, or dependencies
  without evidence and approval.
- Label speculative opportunities as optional improvements, not required fixes.

