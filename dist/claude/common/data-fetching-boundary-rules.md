---
id: 'agents.common.data-fetching-boundary-rules'
title: 'Data Fetching Boundary Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'frontend/data'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/frontend-integration-boundaries|Frontend Integration Boundaries]]'
depends_on: []
---

# Data Fetching Boundary Rules

Purpose: keep frontend data access within existing project layers.

## Rules

- Follow the existing data-fetching layer, cache model, and server/client
  boundary.
- Keep data transformation close to the current owner.
- Do not create backend endpoints, schemas, migrations, database clients, or
  persistence layers unless the user explicitly changes scope.
- Do not put secrets in client code.
- Use official provider or framework docs when current API behavior affects the
  change.
- Do not add data libraries without explicit approval.

