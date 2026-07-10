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
4. Inspect current `tool-capabilities-manifest.json` declarations when MCP,
   native-tool, or documentation capability facts may have changed.
5. Build or refresh framework-specific path indexes so common request types map
   to concrete project paths before broad repo scanning is needed.
6. Update `.agents/project/**` with factual repo details only.
7. Keep `project/mcp-profile.md` aligned with required, conditional, optional,
   and blocked capabilities plus availability evidence for active providers.
8. Keep `project/design-reference-profile.md` focused on screenshot, exported
   asset, copied inspect, and design-reference boundaries; do not imply live
   design-tool access.
9. Keep local approved-pattern and anti-pattern files limited to host-project
   addenda; do not duplicate bundle-wide rules from `.agents/common/**`.
10. After application code changes, verify whether routes, components, helpers,
   tokens, verification commands, MCP facts, documentation choices, or indexed
   paths changed.
11. Keep the reusable skills untouched unless the user explicitly asked for a
   library-level skill change.
