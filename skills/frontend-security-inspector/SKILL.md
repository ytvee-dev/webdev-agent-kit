---
name: frontend-security-inspector
description: Use when the user request involves security-sensitive code,
    configuration, secrets, auth/session boundaries, public entry points, or
    unsafe data handling in React or Next.js projects.
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
