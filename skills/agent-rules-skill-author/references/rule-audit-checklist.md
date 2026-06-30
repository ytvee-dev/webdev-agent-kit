---
id: 'agents.skills.agent-rules-skill-author.references.rule-audit-checklist'
title: 'Rule Audit Checklist'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'agent-rules-skill-author'
tags:
    - 'agents/skill-package'
    - 'agents/reference'
parent:
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
related: []
depends_on:
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
---

# Rule Audit Checklist

Check Unix-style paths, English instruction text, link integrity, skill metadata alignment, and rule contradictions before final reporting.

New exceptions must be narrower than their parent rule.

`SKILL.md`, `agents/openai.yaml`, references, and `AGENTS.md` must agree on routing and tool scope.

Project-specific facts stay in `project/**`.

Report blocked validation honestly.
