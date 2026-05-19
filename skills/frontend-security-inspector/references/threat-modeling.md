---
id: 'agents.skills.frontend-security-inspector.references.threat-modeling'
title: 'Threat Modeling'
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
    - '[[skills/frontend-security-inspector/references/reporting-template|Reporting Template]]'
depends_on:
    - '[[skills/frontend-security-inspector/SKILL|Frontend Security Inspector]]'
---

# Threat Modeling

Use this reference when the user explicitly asks for a threat model, abuse-path
analysis, trust-boundary review, or AppSec-oriented architecture review.

## Workflow

1. Define scope: in-scope paths, excluded paths, runtime versus CI/dev/test, and
   assumptions.
2. Extract the system model from repo evidence: frameworks, routes, public entry
   points, server actions, route handlers, integrations, data stores, auth, and
   deployment clues.
3. Enumerate assets: credentials, session state, PII, user content, tenant data,
   payment or account state, build artifacts, logs, and availability-critical
   components.
4. Enumerate trust boundaries: browser to app, app to API, server to database,
   third-party integrations, webhooks, uploads, storage, and admin surfaces.
5. Identify attacker capabilities and non-capabilities based on exposure and
   repo evidence.
6. List concrete abuse paths tied to assets, entry points, and trust boundaries.
7. Prioritize with qualitative likelihood and impact, then note assumptions that
   would change the ranking.
8. Recommend mitigations tied to concrete components, boundaries, or paths.
9. Provide follow-up verification and manual review focus paths.

## Assumption check-in

Before finalizing a threat model, ask only for missing context that materially
changes risk ranking:

- intended deployment model and internet exposure;
- authentication and authorization expectations;
- data sensitivity, tenant model, and high-value assets;
- known out-of-scope paths or non-production surfaces.

If the user cannot answer, proceed with explicit assumptions and label
conditional conclusions.

## Output shape

- Executive summary with top risk themes.
- Scope and assumptions.
- System model with primary components and trust boundaries.
- Assets and security objectives.
- Attacker model.
- Prioritized threats and abuse paths.
- Existing mitigations, gaps, and recommendations.
- Manual review focus paths.
- Quality check covering entry points, boundaries, assumptions, and residual
  risks.
