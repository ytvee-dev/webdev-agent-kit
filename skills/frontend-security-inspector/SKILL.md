---
name: frontend-security-inspector
description: Use when the user explicitly asks for a security audit, secure coding guidance, threat model, vulnerability review, or when React/Next.js work touches secrets, auth/session boundaries, public entry points, client/server data exposure, unsafe rendering, redirects, storage, or untrusted input. Do not use for ordinary code review without security risk.
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
    - '[[skills/frontend-security-inspector/references/reporting-template|Reporting Template]]'
    - '[[skills/frontend-security-inspector/references/security-checklist-next|Next.js Security Checklist]]'
    - '[[skills/frontend-security-inspector/references/security-checklist-react|React Security Checklist]]'
    - '[[skills/frontend-security-inspector/references/threat-modeling|Threat Modeling]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Frontend Security Inspector

## Modes

- Secure-by-default editing: apply the React or Next.js checklist while making
  security-sensitive changes.
- Passive finding: flag high-impact issues in touched or nearby code when the
  current task exposes a clear security risk.
- Explicit audit: inspect the requested scope and produce a structured findings
  report.
- Threat model: enumerate assets, trust boundaries, entry points, attacker
  capabilities, abuse paths, mitigations, and open assumptions.

## Default workflow

1. Inspect the affected code, configuration, routes, and boundary files.
2. Choose the mode from the user request and discovered risk surface.
3. Read the relevant React, Next.js, reporting, or threat-modeling reference.
4. Ground every finding in evidence from file paths, code, config, or an
   explicit uncertainty note.
5. Produce a structured report for audits and threat models.
6. Suggest remediation tasks or implement fixes only when requested.

## Scope

- auth and session handling
- public entry points
- secrets and environment exposure
- client/server boundary mistakes
- unsafe data handling or validation gaps
- XSS sinks, unsafe HTML, direct DOM injection, dynamic code execution
- redirects, third-party scripts, browser storage, CORS, headers, and cookies

## Core rules

- Never output, log, or commit secret values. Redact any discovered secret and
  report only its location and exposure path.
- Treat TypeScript types as non-security boundaries. Runtime validation is
  required for untrusted input.
- Treat URL data, route params, request bodies, headers, cookies, browser
  storage, postMessage payloads, third-party script data, remote API responses,
  and persisted user content as untrusted unless proven otherwise.
- Do not recommend weakening protections, widening CORS, disabling CSRF,
  turning off CSP, skipping authorization, or storing secrets in the browser as
  a fix.
- Report uncertainty plainly when a control may exist outside app code, such as
  CDN headers, WAF rules, reverse proxy limits, or managed-platform settings.
- Do not use security ownership-map or git-history analytics workflows from
  this skill; they require a different tooling model and are out of scope.

## Reference map

- `references/security-checklist-next.md`
- `references/security-checklist-react.md`
- `references/reporting-template.md`
- `references/threat-modeling.md`
