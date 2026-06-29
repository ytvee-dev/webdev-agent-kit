---
id: 'agents.skills.project-context-adapter.references.extraction-checklist'
title: 'Extraction Checklist'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'project-context-adapter'
tags:
    - 'agents/skill-package'
    - 'agents/project-context'
    - 'agents/reference'
parent:
    - '[[skills/project-context-adapter/SKILL|Project Context Adapter]]'
related:
    []
depends_on:
    - '[[skills/project-context-adapter/SKILL|Project Context Adapter]]'
---

# Extraction Checklist

- Framework and router model
- React version and rendering model
- Non-React frontend framework, static frontend model, or custom build model
- Project type: `frontend-only` or `fullstack`
- Styling system and token sources
- Validation libraries
- Verification commands
- Official documentation sources selected for the detected stack
- MCP dependency scan from `skills/*/agents/openai.yaml`
- Required, available, missing, optional, approved, installed, skipped, or
  blocked MCP capabilities
- Shared architecture patterns
- Local anti-patterns
- Screenshot, exported asset, copied inspect, and design-reference constraints
- Current code paths and modules after recent code changes
- Framework-specific lookup indexes for:
  - styles and themes
  - components
  - business logic
  - SEO
  - utilities
  - server components
  - client components
  - routing, layouts, and metadata
  - content and data
  - analytics and integrations
