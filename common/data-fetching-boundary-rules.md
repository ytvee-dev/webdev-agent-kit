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
    - '[[common/target-stack-policy|Target Stack Policy]]'
depends_on: []
---

# Data Fetching Boundary Rules

Purpose: keep frontend data access within existing TanStack and Axios boundaries.

## Rules

- Follow the existing TanStack Query, TanStack Router, Axios, and API adapter conventions when present.
- Reuse existing Axios instances and API helper layers.
- Keep request and response transformation in the current API adapter owner.
- Do not duplicate TanStack-owned remote data into Redux unless the existing project convention requires it.
- Do not create backend endpoints, schemas, migrations, database clients, or persistence layers unless the user explicitly changes scope.
- Do not put secrets in client code.
- Use official TanStack or Axios docs when current API behavior affects the change.
- Do not add data libraries without explicit approval.
