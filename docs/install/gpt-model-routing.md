---
id: 'agents.docs.install.gpt-model-routing'
title: 'Optional GPT Model Routing'
doc_type: 'user-guide'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/model-routing'
parent:
    - '[[docs/install/codex]]'
related:
    - '[[skills/project-onboarding-adapter/references/codex-model-bootstrap]]'
    - '[[common/codex-model-routing-policy]]'
    - '[[templates/project/model-routing-profile]]'
    - '[[docs/release/1.0.0-checklist]]'
depends_on: []
---

# Optional GPT Model Routing

Version 1.1.0 extends the 1.0.0 opt-in GPT role setup with approved native
activation and read-only configuration diagnostics. It supports a local Codex
project bundle, including compatible Codex IDE surfaces, not GPT models running
inside unrelated clients. It never replaces the main session's model or requires
an external router/API key. Normal onboarding now identifies missing routing
setup and offers its scope; it still does not change models without approval.

## Enable During Onboarding

After normal installation, send:

```text
Adapt this kit to the project and configure economical GPT subagents in the
project-local .codex directory. Preserve my main model, global configuration,
MCP and security settings. Confirm model availability and show the narrow
configuration plan before writing, including the native subagent enablement
key if needed. After I approve that diff, apply it, refresh the client and
smoke-test all four roles. Do not change project trust or bypass managed policy.
```

The agent selects models from your actual client catalog and records the cost
basis and supported inputs/efforts. The reusable kit deliberately contains no
fixed production model IDs. Subscription and API authentication can expose
different catalogs; published model documentation alone is insufficient.

Four roles cover bounded lookup, explicit implementation, complex reasoning
and independent review. Skills still describe how to work. Instructions select
a real role per action; trivial work remains inline, parallelism is bounded,
and stronger models do not reset the existing retry budget.

## Files And Safety

The native format is checked against your installed client. Standalone roles
live in `.codex/agents/`; registered configuration layers live in
`.codex/wdk-agents/` with a narrow `.codex/config.toml` registration block.
Do not configure the same role in both formats. Existing global/user roles,
main-model defaults, approvals and MCP are preserved. Name conflicts stop setup.
Only a separately approved enablement field may be changed alongside the roles:
`agents.enabled` or `features.multi_agent`, selected from the installed schema.
Current Codex documentation enables subagents by default, so a missing flag is
not itself a defect. Another false gate, higher-precedence denial, untrusted
project or ambiguous TOML layout needs explicit reconciliation, not a workaround.

Local `.agents/project/` contains the request, human model-routing profile,
managed hashes and restricted recovery journals. Keep these and `.codex/`
out of public commits and release archives. Journals can contain original
configuration bytes; do not share them. Existing Python 3.11+ can run the
included deterministic helper; no package installation is required.

For exact request fields, dry-run/apply/rollback commands and collision rules,
see the [bootstrap reference](../../skills/project-onboarding-adapter/references/codex-model-bootstrap.md).
Do not run placeholder model IDs. After interruptions, inspect the journal
and state; do not delete a setup lock while another installer may still run.

## Verify Activation, Not Just Files

A written TOML means configured, not verified. Use this read-only local check:

```sh
python .agents/skills/project-onboarding-adapter/scripts/configure_gpt_agents.py \
  --root . --inspect
```

It reports configured roles, local gates and a fingerprint, never live success.
Native delegation need not exist before the configuration phase; it must exist
after activation to perform canaries. Save the next onboarding step before a
client restart. Project trust and managed policy remain controlled by the human
and the client, not by kit instructions. The agent should refresh the
client as documented, run tiny approved read-only canaries, and inspect actual
model/effort and permissions from runtime metadata. A model's identity claim
is not proof. Reviewer independence additionally requires fresh context.

When the client, credentials or observable runtime metadata are unavailable,
setup remains activation-unverified and the ordinary single-agent workflow
continues. No invisible expensive fallback is allowed. Real savings must be
measured across comparable accepted tasks, including coordinator and review
cost, rather than promised from token rates alone.

## Updates And Recovery

Kit upgrades preserve installed role bindings. Client/auth/config changes mark
activation evidence stale; request revalidation or reconfiguration explicitly.
Repeated same-input setup is a no-op. Approved rollback restores only managed
transaction files and refuses later edits. Format migration needs a separate
reviewed plan rather than silently registering duplicate agents.

## Configured But Inactive

| Observation | Action |
| --- | --- |
| Local native gate explicitly false | Preview a narrow schema-confirmed enablement change; apply only after its approval |
| Both known gates false or effective policy denies children | Reconcile effective configuration; never guess which flag wins |
| Project is not trusted | Human uses the client's supported trust controls; the kit does not edit global trust |
| Roles written but not discovered | Refresh/new session, confirm role format and effective registration |
| Inspector succeeds but runtime metadata is missing | Leave activation-unverified; use the main agent |
| Actual child model or effort differs | Block that role, inspect loading/precedence, repeat the canary after correction |
| Existing user role or inline TOML conflicts | Stop before writes and review a manual scoped merge |

See the [1.1.0 validation scope](../release/1.1.0-checklist.md) for automated
coverage and the authenticated four-role acceptance procedure. The
[1.0.0 checklist](../release/1.0.0-checklist.md) remains historical.
