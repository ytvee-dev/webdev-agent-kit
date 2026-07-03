---
id: 'agents.common.rule-audit-findings'
title: 'Rule Audit Findings'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'agents/audit'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/frontend-implementation-boundaries|Frontend Implementation Boundaries]]'
    - '[[common/feedback-cycle-policy|Feedback Cycle Policy]]'
depends_on: []
---

# Rule Audit Findings

This historical audit record captures rule gaps and their current resolution:

- Path style was stated only generally. The boundary rule now requires Unix-style paths in docs, examples, reports, and validation output.
- CSS token safety was present as an anti-pattern but not strict enough. The boundary rule now requires existing CSS variables only.
- Test infrastructure was previously conflated with scoped regression tests. The current anti-pattern permits relevant existing tests and approval- or convention-backed scoped tests while keeping new tooling and broad suites approval-gated.
- Code loops were previously restricted too broadly. The current anti-pattern targets render-side mutation and unclear orchestration while allowing clear local iteration.
- Feedback cycles were easy to confuse with code loops. The feedback cycle policy now separates workflow cycles from project-code iteration.
- Skill authoring validation already checked links and metadata, and the audit checklist now makes path style, English text, and contradiction checks explicit.
