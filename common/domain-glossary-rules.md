---
id: "agents.common.domain-glossary-rules"
title: "Domain Glossary Rules"
doc_type: "common-rule"
layer: "common"
status: "active"
publishable: true
local_only: false
tags: []
parent:
  - "[[AGENTS|Canonical Agent Policy]]"
related:
  - "[[templates/project/domain-glossary]]"
  - "[[skills/project-context-adapter/SKILL]]"
depends_on: []
---

# Domain Glossary Rules

Use a domain glossary when product terms are ambiguous, repeatedly drift, or
carry distinctions that affect UI, types, or data ownership. Read only the
relevant domain. Do not require a glossary for simple projects.

Reuse an existing authoritative glossary. Otherwise create local-only
`project/domain-glossary.md` from `templates/project/domain-glossary.md` only
when there are confirmed terms to record. Keep definitions short, distinguish
UI labels from code identifiers, and cite a verified source or user decision.
List ambiguous aliases with their meaning; do not globally ban ordinary words.

A conflicting user term needs clarification only if it changes behavior.
Uncertain meanings stay unconfirmed. Never infer product semantics solely from
a convenient variable name or rename existing code as part of glossary refresh.
Load this context for affected planning, implementation, copy, and review work;
keep generic instructions and full specifications elsewhere.

Use the existing `project/decision-log.md` for consequential choices, reasons,
and rejected alternatives. Link existing ADRs instead of duplicating them.
A glossary refresh does not authorize edits to host documentation or source.
