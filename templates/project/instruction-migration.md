---
id: 'agents.templates.project.instruction-migration'
title: 'Instruction Migration Template'
doc_type: 'template'
layer: 'template'
status: 'active'
publishable: true
local_only: false
tags: []
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/host-instruction-migration-rules]]'
depends_on: []
---

# Instruction Migration Template

Copy to local `project/instruction-migration.md` using `publishable: false` and
`local_only: true`. Fill it only for a requested migration.

- original entrypoint and digest:
- verbatim backup path:
- explicit migration authorization or pending replacement decision:
- kit version and canonical target:
- proposed minimal pointer:
- local host-instructions path:

| Original rule/section and scope | Destination | Relative-link adjustment | Preservation evidence |
| --- | --- | --- | --- |

## Validation

- All original rules mapped:
- Conflicts or unknowns:
- Pointer destination exists:
- Core loads local host instructions:
- Links resolve from their new locations:
- Original backup matches its digest:
- Unrelated files preserved:
- Repeat migration changes nothing:
- Rollback path:

Do not replace the entrypoint while any instruction is unmapped. A backup alone
does not count as runtime reachability.
