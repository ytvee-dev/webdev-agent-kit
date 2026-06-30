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

The audit found these rule gaps:

- Path style was stated only generally. The boundary rule now requires Unix-style paths in docs, examples, reports, and validation output.
- CSS token safety was present as an anti-pattern but not strict enough. The boundary rule now requires existing CSS variables only.
- Test creation was forbidden, but existing tests could still mislead agents. The boundary rule now says existing tests do not authorize new tests.
- Code loops were limited mostly to component bodies. The loop anti-pattern now applies across host project code.
- Feedback cycles were easy to confuse with code loops. The feedback cycle policy now separates workflow cycles from project-code iteration.
- Skill authoring validation already checked links and metadata, and the audit checklist now makes path style, English text, and contradiction checks explicit.
