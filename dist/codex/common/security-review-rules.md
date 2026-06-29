---
id: 'agents.common.security-review-rules'
title: 'Security Review Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'workflow/security-review'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
depends_on: []
---

# Security Review Rules

Purpose: keep frontend security review evidence-backed and scope-correct.

## Rules

- Treat secrets in client code, unsafe HTML injection, auth/session changes,
  insecure redirects, exposed tokens, and unvalidated external input as
  high-priority review areas.
- Use local project evidence and official framework, platform, or provider docs
  for security claims when behavior is current or ambiguous.
- Do not claim a vulnerability without a concrete path, file, or behavior.
- Do not implement broad security rewrites from review findings without a
  separate approved fix task.

