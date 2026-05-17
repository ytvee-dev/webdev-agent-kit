---
name: frontend-security-inspector
description: Use when the user request involves security-sensitive code,
    configuration, secrets, auth/session boundaries, public entry points, or
    unsafe data handling in React or Next.js projects.
id: 'agents.skills.frontend-security-inspector.skill'
title: 'Frontend Security Inspector'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-security-inspector'
tags:
    - 'agents/skill-package'
    - 'frontend/security'
    - 'agents/skill'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/frontend-security-inspector/assets/audit-report-template|Security Audit Report]]'
    - '[[skills/frontend-security-inspector/references/reporting-template|Reporting Template]]'
    - '[[skills/frontend-security-inspector/references/security-checklist-next|Next.js Security Checklist]]'
    - '[[skills/frontend-security-inspector/references/security-checklist-react|React Security Checklist]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Frontend Security Inspector

## Default workflow

1. Inspect the affected code and configuration.
2. Check the relevant React or Next.js security checklist.
3. Produce a structured findings report.
4. Suggest remediation tasks or implement follow-up fixes only when requested.

## Scope

- auth and session handling
- public entry points
- secrets and environment exposure
- client/server boundary mistakes
- unsafe data handling or validation gaps

## Reference map

- `references/security-checklist-next.md`
- `references/security-checklist-react.md`
- `assets/audit-report-template.md`
