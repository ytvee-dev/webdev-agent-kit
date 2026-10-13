---
id: 'agents.templates.project.claude-agent-profile'
title: 'Claude Agent Profile Template'
doc_type: 'template'
layer: 'template'
status: 'active'
publishable: true
local_only: false
tags:
    - 'client/claude-code'
parent:
    - '[[skills/project-onboarding-adapter/SKILL]]'
related:
    - '[[common/claude-agent-routing-policy]]'
depends_on: []
---

# Claude Agent Profile

Copy to host `.agents/project/claude-agent-profile.md` with `publishable: false`
and `local_only: true`. Record names and evidence only, never credential values.

## Client And Scope

- Client version, surface, platform and checked revision:
- Plugin name, version, installed root and discovery evidence:
- Host root and applicable instructions:
- Full onboarding or explicit facts-only/no-model-change/Plan Mode exclusion:
- Native delegation signature and permission evidence:
- Primary model and existing custom agents preserved:
- Account catalog, supported effort controls, modalities and checked date:
- Approved cost/latency ceiling and model-selection rationale:

## Roles

| Task role | Actual registry identifier | Inherited or approved override | Effective tools | Status | Dispatch evidence |
| --- | --- | --- | --- | --- | --- |
| Lookup | | | | activation-unverified | |
| Light worker | | | | activation-unverified | |
| Worker | | | | activation-unverified | |
| Complex work | | | | activation-unverified | |
| Light reviewer | | | | activation-unverified | |
| Reviewer | | | | activation-unverified | |
| Deep reviewer | | | | activation-unverified | |
| Architect | | | | activation-unverified | |
| Deep architect | | | | activation-unverified | |

## Freshness And Results

- Installed/discovered facts versus actual native invocation metadata:
- Tiny read-only checks run, skipped or blocked, with reason:
- Configuration/plugin/auth fingerprint without secrets:
- Missing tools, image evidence or provider access:
- Drift that makes affected bindings stale:
- Normal single-agent fallback when routing is unavailable:
- Measured coordinator, child, retry and review usage per accepted result:

No fixed savings promise. CLI inventory and written profiles do not establish
model activation or successful behavioral evaluation.
