---
id: 'agents.templates.project.model-routing-profile'
title: 'GPT Model Routing Profile Template'
doc_type: 'template'
layer: 'template'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/model-routing'
parent:
    - '[[skills/project-onboarding-adapter/SKILL]]'
related:
    - '[[common/codex-model-routing-policy]]'
    - '[[skills/project-onboarding-adapter/references/codex-model-bootstrap]]'
depends_on: []
---

# GPT Model Routing Profile

Copy to host `project/model-routing-profile.md` only for approved setup.
The copy must use `publishable: false` and `local_only: true`. Do not record
credentials, complete config contents or unverified availability as fact.

## Environment And Approval

- State: proposed / configured / activation-unverified / verified / blocked.
- User-approved configuration scope and spending ceiling:
- Client, surface, version, authentication mode and host root:
- Native format and supporting official schema/docs observation:
- Callable delegation, effective agent names and collision check:
- Trust, approvals, tool and effective sandbox constraints:
- Availability source/date and supported efforts/modalities:
- Cost basis, units, source/date and task-fit evidence:
- Request path and hash; state file hash and managed configuration fingerprint:
- Last checked source revision; refresh conditions:

## Role Bindings And Activation

For each of `wdk_lookup`, `wdk_worker`, `wdk_complex`, `wdk_reviewer`, record:

- Configuration path, model ID, effort and selection rationale:
- Input modalities and required tool capabilities:
- Configuration status separately from runtime status:
- Canary run ID, observed model/effort metadata and evidence location:
- Effective permissions and instruction adherence:
- Reviewer context isolation evidence, when relevant:
- Blocked checks and accepted fallback:

A role is eligible only when its runtime evidence and current configuration
fingerprint match. Do not infer an executed model from its self-report, role
name, request arguments or file contents. Partial activation does not verify
other roles. A config change invalidates affected activation evidence.

## Ownership And Recovery

- Managed role/block hashes: `project/model-routing-state.json`.
- Last transaction ID and restricted backup location:
- Local ignore status for request/profile/state/backups and `.codex/`:
- Preserved user settings and unresolved conflicts:
- Recovery validation:

## Outcome Cost Evidence

Record only measured comparable task results: acceptance outcome, primary and
child models, total tokens/credits or API cost with units, retries, review,
latency, regressions and remaining limitations. No fixed savings promise.
