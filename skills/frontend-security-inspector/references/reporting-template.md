---
id: 'agents.skills.frontend-security-inspector.references.reporting-template'
title: 'Reporting Template'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-security-inspector'
tags:
    - 'agents/skill-package'
    - 'frontend/security'
    - 'agents/reference'
parent:
    - '[[skills/frontend-security-inspector/SKILL|Frontend Security Inspector]]'
related:
    []
depends_on:
    - '[[skills/frontend-security-inspector/SKILL|Frontend Security Inspector]]'
---

# Reporting Template

Use this format for explicit security audits and vulnerability reviews.

## Finding fields

- Rule or risk ID
- Severity: Critical, High, Medium, Low
- Affected area
- Location: file path, symbol, route, or config key
- Evidence: concise code or config evidence, with secrets redacted
- Impact: what can go wrong and who can exploit it
- Recommended remediation
- Mitigation or defense-in-depth option when the direct fix is not immediate
- False-positive notes or external controls to verify
- Follow-up verification

## Report shape

1. Start with findings ordered by severity.
2. Include only evidence-backed findings. Do not pad the report with generic
   best-practice advice.
3. Separate confirmed findings from assumptions or controls not visible in app
   code.
4. Keep remediation concrete and scoped to the affected path.
5. For "no findings" results, say that clearly and list residual risk or
   checks that were not run.
