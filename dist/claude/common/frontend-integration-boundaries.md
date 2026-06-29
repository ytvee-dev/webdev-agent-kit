---
id: 'agents.common.frontend-integration-boundaries'
title: 'Frontend Integration Boundaries'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'frontend/integration'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/data-fetching-boundary-rules|Data Fetching Boundary Rules]]'
depends_on: []
---

# Frontend Integration Boundaries

Purpose: support frontend integration with existing auth, data, and provider
layers without turning the bundle into backend or infrastructure tooling.

## Rules

- Follow existing SDKs, API clients, auth flows, and provider wrappers.
- Use official provider docs when integration behavior is current or ambiguous.
- Do not create backend schemas, migrations, RLS policies, queues, webhooks, or
  database setup unless the user explicitly changes scope.
- Do not handle secrets in client code.
- Ask for approval before changing auth persistence, session behavior, or data
  mutation flow.

