---
id: 'agents.skills.project-onboarding-adapter.references.codex-model-bootstrap'
title: 'Codex GPT Model Bootstrap'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/model-routing'
parent:
    - '[[skills/project-onboarding-adapter/SKILL]]'
related:
    - '[[common/codex-model-routing-policy]]'
    - '[[templates/project/model-routing-profile]]'
    - '[[common/codex-official-docs-policy]]'
depends_on: []
---

# Codex GPT Model Bootstrap

Purpose: let onboarding instructions install approved project-local GPT roles;
the optional helper only validates and writes files, never routes model calls.

## Entry And Approval

Run only when the user explicitly requests GPT model setup or approves the
proposed configuration diff. Ordinary adaptation, kit updates, Plan Mode and
non-Codex clients must not write model settings. Using GPT in Cursor is not
proof of the Codex contract. Keep the existing primary model unchanged.

Resolve the actual host root, installed Codex surface/version, authentication
mode, active configuration precedence, project trust, writable boundaries,
callable delegation and all effective agent names. Do not read credentials.
Inspect relevant configuration fields, not a secret-bearing config dump.
Use `common/codex-official-docs-policy.md` for current official contracts.
Do not install software, trust a project, enable disabled agents, modify global
settings or relax sandbox/approval controls as a setup workaround.

## Resolve Models From Evidence

Use an actually available client catalog, such as App Server `model/list` only
when that interface is accessible, or confirmed client model-picker evidence.
Never invent a callable `list_models` tool. Public documentation establishes
model capabilities, not account availability. If availability, format or
permissions cannot be established, return a proposal and the exact blocker.

Select only confirmed GPT IDs with supported reasoning efforts. Record the
observation date, client/version/auth mode, input modalities, availability
source and cost basis. Compare current official subscription credits or API
prices as appropriate; do not mix units or infer price from an ID suffix.
Use task-fit evidence and expected total cost, not just the lowest token rate.
Start with an economical model for bounded lookup/work and a more capable
approved model for complex/review work when the catalog supports that split.
The same model may serve several roles; do not claim savings without evidence.
Use higher effort only when justified and supported. No permanent production
model IDs belong in reusable instructions or templates.

## Choose One Native Format

Check the installed client's documentation/schema before writing:

- `standalone`: create `.codex/agents/wdk_*.toml` with `name`, `description`,
  `developer_instructions`, `model` and `model_reasoning_effort`.
- `registered`: merge only `[agents.wdk_*]` descriptions and `config_file`
  references into host `.codex/config.toml`; put configuration layers in
  `.codex/wdk-agents/`, outside standalone discovery. Relative paths resolve
  from the declaring config. These layers omit standalone name/description.

Do not register the same role twice or override a user/built-in/global role.
Check names inside TOMLs, not only filenames. The helper checks local collisions;
onboarding must also check the effective registry/global collisions. A format
migration requires a separate reviewed plan; do not switch formats in place.
Never change `[agents]` defaults, primary model, providers, auth, MCP, network,
trust, approval policy or concurrency settings as part of the narrow merge.
Read-only role defaults do not override stronger live parent settings: verify
the effective sandbox and enforce the no-edit instruction as well.

## Deterministic Installation

Use an existing Python 3.11+ interpreter and the shipped
`scripts/configure_gpt_agents.py` under this skill when available. Do not
install Python just for onboarding. Without it, use native file tools with
the same validation, ownership and recovery gates, or report blocked setup.

Create a local-only request JSON after confirming its facts. Required shape:

```json
{
  "schema_version": 1,
  "client": "codex",
  "client_version": "CONFIRMED_CLIENT_VERSION",
  "auth_mode": "chatgpt",
  "format": "standalone",
  "observed_at": "CONFIRMED_OBSERVATION_DATE",
  "availability_evidence": "CONFIRMED_CLIENT_CATALOG_SOURCE",
  "cost_basis": "CONFIRMED_COST_UNITS_SOURCE_DATE_AND_TASK_FIT",
  "models": {
    "REPLACE_WITH_AVAILABLE_GPT_ECONOMY_ID": {"efforts": ["low", "medium"], "modalities": ["text"]},
    "REPLACE_WITH_AVAILABLE_GPT_CAPABLE_ID": {"efforts": ["medium", "high"], "modalities": ["text", "image"]}
  },
  "roles": {
    "wdk_lookup": {"model": "REPLACE_WITH_AVAILABLE_GPT_ECONOMY_ID", "effort": "low", "reason": "Bounded lookup"},
    "wdk_worker": {"model": "REPLACE_WITH_AVAILABLE_GPT_ECONOMY_ID", "effort": "medium", "reason": "Explicit slice"},
    "wdk_complex": {"model": "REPLACE_WITH_AVAILABLE_GPT_CAPABLE_ID", "effort": "medium", "reason": "Ambiguous cause"},
    "wdk_reviewer": {"model": "REPLACE_WITH_AVAILABLE_GPT_CAPABLE_ID", "effort": "high", "reason": "Material-risk review"}
  }
}
```

The example contains placeholders, not actual available models. Replace every
placeholder from evidence; never execute the example verbatim. The helper
validates consistency, not the truth of supplied account/cost assertions.
Keep request, profile, state and backups local and out of published archives.

From the host root, inspect the dry-run first:

```sh
python .agents/skills/project-onboarding-adapter/scripts/configure_gpt_agents.py \
  --root . --request .agents/project/model-routing-request.json
```

After explicit permission, add `--apply --approve`. The flag is not itself
proof of user consent. Plan Mode never runs the write command.

The helper refuses unowned files, user drift, malformed TOML, links, name
collisions and disabled agents. It preserves unrelated configuration bytes
and validates parsed values after the narrow merge. Same-input reruns are
no-ops. It stores role/block hashes in `project/model-routing-state.json` and
restricted local transaction journals in `project/model-routing-backups/`,
never in an auto-discovery directory. It uses per-file atomic replacement,
not a multi-file atomic transaction; do not run concurrent setup commands.
Normal write failure attempts rollback; a crash leaves the journal for recovery.
Review the result and hashes after interruption. For approved recovery:

```sh
python .agents/skills/project-onboarding-adapter/scripts/configure_gpt_agents.py \
  --root . --rollback TRANSACTION_ID --approve
```

Rollback refuses to overwrite later user edits, including unrelated edits to
a backed-up config. Stop and reconcile such conflicts manually with approval.
Do not remove a stale setup lock without confirming that no installer is active.
Journals can contain original config bytes: protect them locally, never publish
them or accept a journal from an untrusted source.

## Activation And Smoke Checks

Write `project/model-routing-profile.md` from its template. Preserve separate
states: `proposed`, `configured`, `activation-unverified`, `verified`, `blocked`.
The helper reports only configuration state; it cannot verify a model runtime.
A written TOML does not change the model of the already running response.
Use the documented client refresh/new-session path when necessary.

With approved smoke-run scope, launch each configured role on a tiny read-only
fixture, including workers, without implementation work. Bootstrap canaries
are the explicit exception to the normal verified-role routing gate. Confirm
role discovery, actual model/effort from runtime metadata, inherited tools and
permissions, and fresh-context capability for the reviewer. The model's own
identity claim, a `--model` label or TOML contents are not execution evidence.
Record per-role run identifiers, observed metadata, effective permissions and
the configuration fingerprint. Only verified roles become eligible for normal
routing. If metadata or an authenticated client is absent, leave activation
unverified and use the existing single-agent workflow; do not fabricate success.

Recheck only on client/auth/config drift, unavailable-model errors or an explicit
request. Kit upgrades preserve host roles and profiles; they do not pick new
models. Cost and quality comparisons require comparable accepted-outcome runs.
