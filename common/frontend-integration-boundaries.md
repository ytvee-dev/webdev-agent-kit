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
    - '[[common/target-stack-policy|Target Stack Policy]]'
depends_on: []
---

# Frontend Integration Boundaries

Purpose: support frontend integration through existing React, Next.js, Redux, TanStack, and Axios boundaries without becoming backend or infrastructure tooling.

## Rules

- Follow existing Axios clients, TanStack query/router conventions, Redux slices, React providers, and Next.js server/client boundaries.
- Use official target-stack docs when integration behavior is current or ambiguous.
- Keep Redux out of server communication and domain processing.
- Do not create backend schemas, migrations, RLS policies, queues, webhooks, or database setup unless the user explicitly changes scope.
- Do not handle secrets in client code.
- Ask for approval before changing auth persistence, session behavior, or data mutation flow.
