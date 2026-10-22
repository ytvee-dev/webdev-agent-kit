---
id: 'agents.skills.project-onboarding-adapter.references.installation-diagnostics'
title: 'Installation And Subagent Diagnostics'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'project-onboarding-adapter'
tags:
    - 'agents/reference'
parent:
    - '[[skills/project-onboarding-adapter/SKILL]]'
related: []
depends_on: []
---

# Installation And Subagent Diagnostics

Use for "check WebDev setup", "why are subagents not running?", or an explicit
installation health check. This read-only branch ends with a report; it does not
continue into onboarding, model configuration, upgrades or instruction changes.

## Inspect

1. Resolve host, client surface, installed bundle/plugin path and version from
   available manifests and installation records. Report missing provenance.
2. Inspect the current native tool/agent registry and only the relevant local
   profiles: `project/client-profile.md`, `project/model-routing-profile.md`,
   or `project/claude-agent-profile.md` under the host's `.agents` directory.
   Read scoped non-secret config only when relevant; never dump credentials.
3. For Codex use `common/codex-model-routing-policy.md`; for Claude use
   `common/claude-agent-routing-policy.md`. For other clients inspect actual
   capabilities without assuming either client's role setup applies.
4. Compare configured role, discovered identifier, permitted dispatch parameters,
   recorded runtime evidence and current client/auth/config fingerprint. Unknown
   or changed fingerprints make past evidence stale. A primary model's self-report
   or a role definition is not proof a child ran with that model or effort.
5. Explain the concrete reason for single-agent work: trivial task, no callable
   delegation, explicit restriction, undiscovered role, stale profile or absent
   runtime evidence. Separate supported behavior from an observed failure.

## Evidence States

Report each relevant role with these separate fields:

| Field | Meaning |
| --- | --- |
| Configured | Definition or binding exists, with source path |
| Discovered | Current client registry exposes the real identifier |
| Dispatch permitted | Current tools and authority allow this invocation |
| Runtime verified | Observed invocation evidence matches this environment |
| Blocker / next step | Exact missing fact or separately scoped repair |

Use yes, no or unknown for each field; mark stale runtime evidence explicitly.
Report model/effort only if supplied by trusted invocation metadata. Never
collapse "configured" into "working" or promise identical support in all clients.

## Optional Invocation Check

An ordinary diagnostic request does not launch agents or spend additional model
budget. If the user explicitly requests a live subagent check and current policy
permits it, run one bounded read-only task per requested role with the existing
verified dispatch contract. Pass a neutral task and no private transcript. Record
invocation metadata, result and limitations. A successful answer proves that
invocation worked; it proves model/effort only when trusted metadata exposes them.
Do not test write capabilities by editing user files. Never change configuration,
permissions, concurrency or models to make the check pass.

## Return

Give the installed version/client, compact role evidence table, current reason
for single-agent execution and smallest next action. Do not create profiles,
rewrite pointers, enable delegation, report bugs or sync memory as a side effect.
Route an explicitly requested repair through normal approved onboarding. Route
an explicitly requested Kit issue through `webdev-feedback` with sanitized facts.
