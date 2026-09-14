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
- Onboarding request or explicit setup authority, exclusions and spending ceiling:
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
- Client-surface dispatch mode: named-role / explicit-binding / unsupported:
- Observed tool signature and supported role/model/effort/context parameters:
- Canary run ID, observed model/effort metadata and evidence location:
- Effective permissions and instruction adherence:
- Reviewer context isolation evidence, when relevant:
- Blocked checks and accepted fallback:

A role is eligible only when its runtime evidence and current configuration
fingerprint match. Do not infer an executed model from its self-report, role
name, request arguments or file contents. Partial activation does not verify
other roles or dispatch modes. Direct-binding evidence never certifies native
role loading. A config change invalidates affected activation evidence.

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

## Native Gate And Restart Handoff

- Observed `agents.enabled` / `features.multi_agent` and effective precedence:
- Installed-schema evidence for the chosen key, or confirmed enabled default:
- Approved old/new gate values (omitted when no gate change is needed):
- `--inspect` fingerprint and date (configuration evidence only):
- Effective local configuration loading and trust/managed-policy evidence:
- Required client refresh/new-session action and exact next onboarding step:
- Per-role expected versus observed model AND effort; primary model unchanged:

Configured but untrusted, disabled by higher precedence, or without an observable
canary is not verified. Do not use a prose checklist or inspector output as a
substitute for child execution metadata. Never copy private raw session logs
or secret-bearing configuration into a publishable report.
