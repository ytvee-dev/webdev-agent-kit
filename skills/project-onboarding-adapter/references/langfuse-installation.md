---
id: 'agents.skills.project-onboarding-adapter.references.langfuse-installation'
title: 'Optional Langfuse Installation'
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

# Optional Langfuse installation

During adaptation, offer the user's requested choice separately from local
learning capture and private memory synchronization. Preserve a recorded choice;
do not ask again merely because the Kit was updated.

| Choice | Setup |
| --- | --- |
| No Langfuse | Keep local learning available; disable telemetry for this project. |
| Langfuse Cloud | Use the user's selected region, project, endpoint and credentials. |
| Local or self-hosted Langfuse | Reuse the supplied instance, or prepare an explicitly requested deployment using the official guide. |

Inspect the installed client integration before configuration. Installing this Kit
does not install the Langfuse plugin or a server. Explain what recorded content
the integration sends. Obtain the hosting choice and tracing scope before enabling
it. Never put credentials into project rules, commits or reports.

## Required Adaptation Sequence

1. Read the host learning profile and inspect the current client, integration,
   project config and credential presence without printing secrets. Preserve a
   saved choice on re-adaptation and Kit updates. An unresolved choice must be
   offered during full adaptation, not silently skipped. Ask connection versus
   decline; if connecting, resolve Cloud region or the existing HTTPS endpoint.
   A new server deployment remains separate explicit scope.
2. Explain that tracing exports session content, attachments and tool inputs and
   outputs. Connection consent covers the supported plugin and its documented
   hooks for this project, not local raw capture or private-memory synchronization.
3. Offer to reuse already available credentials. If missing, create a private
   credential template and open its absolute path in the user's editor using the
   callable client file-opening tool. A path printed in chat is not an opened
   file: if opening is unavailable, report that limitation and provide the path.
   Never request keys in chat, print their contents or overwrite an existing file.
4. Wait for the user's completion message or refusal. Blank/placeholder values
   and elapsed time are not readiness or consent. Check required values privately;
   presence and key shape do not establish authentication. Invalid credentials
   leave setup pending and tracing disabled until corrected.
5. Once approved credentials are ready, install only missing supported integration
   components, preserve other hooks/settings and enable this project's tracing.
   Native hook trust prompts remain user-controlled. Do not re-request permission
   already granted for this setup. Unsupported clients stay pending with a
   concrete limitation; never install the Codex adapter into another client.
6. Configure stable project tags with `learning_tagging.py configure --project
   ROOT`. Use `probe --project ROOT --hook VERIFIED_HOOK_PATH` only for the actual
   installed compatible hook, then `validate --project ROOT`. Ingestion requires
   both matching stable-ID evidence and `probe_status=found` for the new probe;
   existing old traces or configuration alone are insufficient. If readback
   credentials are missing, report configured but unverified, not connected.
7. Record choice, endpoint, tags, stable ID, setup status, verification evidence
   and project-only disable steps in `.agents/project/learning-profile.md`.
   Never store keys there. If restart or native approval is required, record
   pending status and the next action; resume verification afterward.

## Codex Credentials And Hooks

Use `~/.codex/langfuse.json` for a missing credential file (resolve the actual
Codex home first). Create it exclusively, with `enabled: false`, empty
`public_key` and `secret_key`, and the selected `base_url`. Leave existing values
and unrelated fields intact. Keep secrets outside the repository; if existing
project credentials are used, confirm their file is excluded from Git before
writing. Do not change an existing global tracing preference without permission.

Inspect the installed Codex version, Node runtime, `codex plugin list` and
`codex features list`. Follow the current official integration guide; its plugin
is `tracing@codex-observability-plugin` from marketplace
`langfuse/codex-observability-plugin`. If missing, use the supported
`codex plugin marketplace add` and `codex plugin add` commands after connection
consent. Missing runtime prerequisites are a disclosed blocker, not permission
for unrelated system installation.

Merge project-local `.codex/config.toml` hook/plugin enablement (`features.hooks`
and the plugin's `enabled` setting) without replacing existing TOML or trust
state. Merge `.codex/langfuse.json` with project `enabled: true` only after the
credential gate, selected endpoint and required tags. Global credentials can be
shared; project enablement and stable IDs cannot. For existing global tracing or
environment overrides, explain any conflict with project-only isolation and
resolve it with the user before claiming isolation; do not disable other projects.

Effective configuration precedence is environment, project file, global file,
then defaults. Check `TRACE_TO_LANGFUSE`, `LANGFUSE_CODEX_TAGS` and the installed
integration's supported prefixed overrides, including credential/endpoint
overrides, without displaying secrets. Resolve conflicting overrides before
declaring enablement, disablement or project tagging successful.

When a restart is required, ask the user to restart Codex and use a fresh session
with two short test turns. Do not claim hooks loaded retroactively. Align the
learning export endpoint and its named authorization environment variable with
the tracing account; writing trace keys alone does not configure API readback.

## Decline And Disable

For refusal or an explicit project disable request, preserve all keys and other
projects. Set this project's `.codex/langfuse.json` `enabled: false` and existing
learning `telemetry.enabled: false`. Preserve unrelated settings. Check overrides
that could still enable tracing; unresolved overrides mean disablement is not
verified. Keep local memory available. If memory needs initialization, use
`learning_project.py --project ROOT --local-only`; do not create or enable hooks
for a declined integration. Save the decision so subsequent adaptation does not
repeat the offer unless the user explicitly reconfigures it.

New project memory defaults to telemetry and synchronization disabled with no
repository address. Preserve explicit existing choices; reconcile unconfirmed
legacy defaults before network work. Use `learning_tagging.py status --project
ROOT` for a secret-free credential/override check, then `enable --project ROOT
--approve` or `disable --project ROOT --approve` for the user's chosen action.
Enablement validates key presence/shape and authenticates a minimal scoped API
read before configuring tags. Authentication failure disables project tracing.
This does not install the native plugin or prove ingestion; finish client setup
and the current probe readback.

For either connected option, align the client tracing endpoint and learning
`telemetry.base_url`; configure the named authorization environment variable
without printing its value. Use the copied `learning_tagging.py` setup and readback
procedure. Report installation, configuration and observed trace ingestion
separately. Missing credentials or a missing connector leave setup pending.

The copied exporter requires HTTPS. A local HTTP-only instance cannot be declared
compatible with that exporter: arrange an approved HTTPS endpoint or retain the
documented database-only fallback until transport support is implemented.

For a new local deployment, inspect Docker availability and ports first. Follow
the current official Compose guide in a separate chosen infrastructure directory,
replace example secrets and preserve data volumes. A deployment request does not
authorize deleting volumes or changing unrelated running services.

Record the choice, endpoint (without credentials), project scope, disable steps
and observed verification in host-local `project/learning-profile.md`.

Sources: [Codex integration](https://langfuse.com/integrations/developer-tools/codex),
[deployment options](https://langfuse.com/self-hosting) and
[local Docker Compose setup](https://langfuse.com/self-hosting/deployment/docker-compose).
