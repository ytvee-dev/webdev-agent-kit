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

The copied STEM helper initializes telemetry enabled and contains its original
snapshot repository default. Do not treat these defaults as the current user's
selection. Reconcile both settings with the confirmed learning profile before any
export or synchronization. For no Langfuse, set `telemetry.enabled` false in the
project learning configuration and disable the client tracing integration for that
project. Disabling exports alone does not stop the client's tracing hook.

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

Sources: [deployment options](https://langfuse.com/self-hosting) and
[local Docker Compose setup](https://langfuse.com/self-hosting/deployment/docker-compose).
