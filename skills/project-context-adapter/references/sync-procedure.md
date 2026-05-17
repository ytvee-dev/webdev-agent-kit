---
id: 'agents.skills.project-context-adapter.references.sync-procedure'
title: 'Sync Procedure'
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

# Sync Procedure

1. Read the current `AGENTS.md`.
2. Inspect stack and tooling files.
3. Inspect route structure, shared components, styling, and validation helpers.
4. Build or refresh framework-specific path indexes so common request types map
   to concrete project paths before broad repo scanning is needed.
5. Update `.agents/project/**` with factual repo details only.
6. Keep local approved-pattern and anti-pattern files limited to host-project
   addenda; do not duplicate bundle-wide rules from `.agents/common/**`.
7. After application code changes, verify whether routes, components, helpers,
   tokens, verification commands, or indexed paths changed.
8. Keep the reusable skills untouched unless the user explicitly asked for a
   library-level skill change.
