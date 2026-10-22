---
id: 'agents.docs.install.gpt-model-routing'
title: 'Codex Onboarding Model Routing'
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

# Codex Onboarding Model Routing

Codex can delegate part of a task to a subagent with its own role and model.
During full project adaptation, the Kit sets up missing local roles and checks
that they work. It preserves existing working settings and your main session's
model. No separate routing service or API key is required.

This setup applies to supported Codex clients, including compatible IDE
extensions. It does not configure GPT models inside other products. A Kit
update, Plan Mode or a request to update project facts only leaves model settings
unchanged. If settings conflict, the agent asks how to resolve them.

## Enable During Onboarding

After normal installation, send:

```text
Onboard this project with WebDev Agent Kit.
```

This request includes local role setup and small read-only checks. The agent
shows what it will change and proceeds without a second setup confirmation.
To skip this, say: "Update only project facts; do not change model configuration."

Each role needs a model and a supported reasoning effort. The agent checks the
models available in your client and account before choosing them. Subscription
and API accounts can offer different models.

The four original roles cover lookup, implementation, complex work and review.
New setup normally also adds a role for mechanical edits and one for architecture.
The bundled routing matrix suggests model families and effort levels for each
job; the agent must match them to your account's available models. Additional
review or architecture roles are optional. See the
[workload and effort matrix](../../skills/project-onboarding-adapter/references/model-workload-matrix.md).
Skills describe how to do a task; roles determine who does it. Small tasks stay
with the main agent. Delegated tasks keep their scope and retry limits even if
a stronger model is selected.

## Files And Safety

The native format is checked against your installed client. Standalone roles
live in `.codex/agents/`; registered configuration layers live in
`.codex/wdk-agents/` with a narrow `.codex/config.toml` registration block.
Do not configure the same role in both formats. Existing global/user roles,
main-model defaults, approvals and MCP are preserved. Name conflicts stop setup.
Only an onboarding-scoped enablement field may be changed alongside the roles:
`agents.enabled` or `features.multi_agent`, selected from the installed schema.
Current Codex documentation enables subagents by default, so a missing flag is
not itself a defect. Another false gate, higher-precedence denial, untrusted
project or ambiguous TOML layout needs explicit reconciliation, not a workaround.

Local `.agents/project/` stores the setup request, a readable summary of role
settings, file hashes used to detect changes, and recovery records for rollback. Keep these and `.codex/`
out of public commits and release archives. Journals can contain original
configuration bytes; do not share them. Symlinks and Windows reparse points,
including junctions in managed paths or the host root, are refused. On POSIX, journals use 0600 inside a
0700 directory. On Windows, native Windows PowerShell protects and verifies a
current-user-only inheritable ACL before the journal is written; if unavailable
or denied, setup stops without configuration writes. It does not change parent
or global ACLs. Existing Python 3.11+ can run the
included deterministic helper; no package installation is required.

For exact request fields, dry-run/apply/rollback commands and collision rules,
see the [bootstrap reference](../../skills/project-onboarding-adapter/references/codex-model-bootstrap.md).
Do not run placeholder model IDs. After interruptions, inspect the journal
and state; do not delete a setup lock while another installer may still run.

## Check how your client starts subagents

Some Codex clients start a subagent by role name. Others accept a model and
reasoning effort directly. Adaptation records the supported mode as `named-role`,
`explicit-binding`, or `unsupported`.

A direct call must include the role's instructions, model and effort. An
independent reviewer starts without the implementation conversation. A successful
direct call does not prove that role files loaded, and a CLI result does not
prove the same setup works in the desktop app.

## Verify Activation, Not Just Files

A written TOML means configured, not verified. Use this read-only local check:

```sh
python .agents/skills/project-onboarding-adapter/scripts/configure_gpt_agents.py \
  --root . --inspect
```

It reports configured roles, enablement settings and a configuration fingerprint
used to detect later changes. It does not start a subagent.
Role files can be prepared before delegation is available. To test them, the
client must actually support starting subagents. Save the next onboarding step before a
client restart. Project trust and managed policy remain controlled by the human
and the client, not by kit instructions. The agent should refresh the
client as documented, run the onboarding-scoped small read-only checks, and inspect actual
model/effort and permissions from runtime metadata. A model's identity claim
is not proof. Reviewer independence additionally requires fresh context.

When the client, credentials or observable runtime metadata are unavailable,
setup remains activation-unverified and the ordinary single-agent workflow
continues. The agent must not silently switch to a more expensive model. Real savings must be
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
| Local native gate explicitly false | During full onboarding, show and apply the narrow supported enablement; preserve higher-precedence restrictions |
| Both known gates false or effective policy denies children | Reconcile effective configuration; never guess which flag wins |
| Project is not trusted | Human uses the client's supported trust controls; the kit does not edit global trust |
| Roles written but not discovered | Refresh/new session, confirm role format and effective registration |
| Inspector succeeds but runtime metadata is missing | Leave activation-unverified; use the main agent |
| Actual child model or effort differs | Block that role, inspect loading/precedence, repeat the small check after correction |
| Existing user role or inline TOML conflicts | Stop before writes and review a manual scoped merge |

See the [1.1.0 validation scope](../release/1.1.0-checklist.md) for automated
coverage and the authenticated per-role acceptance procedure. The
[1.0.0 checklist](../release/1.0.0-checklist.md) remains historical.
