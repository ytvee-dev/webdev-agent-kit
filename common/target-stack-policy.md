---
id: 'agents.common.target-stack-policy'
title: 'Target Stack Policy'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'frontend/stack'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related: []
depends_on: []
---

# Target Stack Policy

WebDev Assistant targets React, Next.js, CSS Modules, Redux, TanStack, and Axios.

Use local project conventions first. Use official documentation for the detected target-stack library when current behavior matters.
