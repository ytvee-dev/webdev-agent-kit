---
id: 'agents.common.review-severity-model'
title: 'Review Severity Model'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'workflow/review'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
depends_on: []
---

# Review Severity Model

Purpose: make frontend review findings consistent and actionable.

## Labels

- `blocking`: must fix before merge, release, or final acceptance.
- `high`: likely user-facing bug, security issue, data loss, or serious
  maintainability risk.
- `medium`: real issue with contained impact.
- `low`: minor risk or polish issue.
- `nit`: optional style or clarity improvement.
- `praise`: specific positive finding backed by evidence.

## Verdicts

- `pass`: no required fixes found.
- `pass with concerns`: required fixes are absent, but risks or optional
  improvements should be recorded.
- `fail`: at least one `blocking` or unresolved required `high` issue exists.

