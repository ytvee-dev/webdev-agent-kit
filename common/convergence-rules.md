---
id: 'agents.common.convergence-rules'
title: 'Convergence Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'workflow/planning'
    - 'workflow/convergence'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/policy-precedence|Policy Precedence]]'
    - '[[common/planning-rules|Planning Rules]]'
    - '[[common/independent-review-rules|Independent Review Rules]]'
    - '[[skills/execution-plan-manager/SKILL|Execution Plan Manager]]'
depends_on: []
---

# Convergence Rules

Purpose: compare completed implementation and evidence with the confirmed intent,
then expose the smallest remaining work without rewriting history.

## Authority And Preconditions

Apply `common/policy-precedence.md`. A goal, specification, or execution plan is
useful intent evidence, but is never the sole authority over the current direct
user request, confirmed approvals, host instructions, or verified facts.

Convergence requires an implementation result plus a confirmed goal or acceptance
criteria. If the current user request changed the goal, scope, or constraints,
reconcile that intent in `create` or `resume` mode before convergence. Do not
silently judge new intent against a stale plan.

Load only the active acceptance criteria, constraints, relevant decisions,
planned surfaces, changed surfaces, and verification evidence. Do not re-read the
entire project or historical plan unless a concrete conflict requires it.

## Comparison Contract

Compare the implementation and evidence with each active criterion and classify
only actionable gaps:

```text
F-001 | missing/partial/contradicts/unrequested | critical/high/medium/low | source | evidence | remaining work
```

- `missing`: required behavior or evidence is absent.
- `partial`: the criterion is started but not fully satisfied.
- `contradicts`: implemented behavior conflicts with confirmed intent or a
  higher-authority constraint.
- `unrequested`: implementation exceeds confirmed scope or approval.

Assign stable zero-padded `F-###` identifiers in acceptance-criterion order,
then changed-surface order for unrequested work. Preserve identifiers when the
same finding is revisited. Severity reflects impact on accepted behavior:

- `critical`: unsafe, destructive, security-sensitive, or release-blocking gap;
- `high`: an active criterion fails or scope materially conflicts;
- `medium`: behavior is usable but incomplete or evidence is materially weak;
- `low`: bounded cleanup or clarity gap with no material behavior failure.

Every finding must cite a criterion, constraint, decision, diff surface, or
verification result. Do not create work from taste, speculative architecture, or
generic best practice.

## Write Boundary

Convergence never changes application source, configuration, dependencies,
tests, generated assets, or verification results.

For response-only plans, report findings and remaining work only. Do not create
a durable file.

For a durable plan with actionable findings, append exactly one new section to
the end of `project/active-plan.md`:

```text
## Convergence Pass N

Finding: F-### ...
Added Slice: S-### [AC-###] ...
Verification: ...
```

- Append; never rewrite, renumber, delete, reorder, or mark over prior slices.
- Choose `N` after the highest existing convergence pass.
- Allocate new `S-###` identifiers after the highest existing slice identifier.
- Link `missing`, `partial`, and `contradicts` work to the affected `AC-###`.
- For `unrequested`, add `S-### [F-###]` citing the conflicting scope constraint
  and requiring a justify-or-remove decision. Never delete the work or assume
  approval during convergence.
- Preserve all prior decisions, states, evidence, and deviations byte-for-byte.

If no actionable finding exists, leave the durable plan byte-for-byte unchanged.
Do not add an empty pass, success marker, timestamp, formatting cleanup, or
rewritten status.

## Completion Boundary

Convergence reports whether confirmed intent and implementation align. It does
not implement fixes, grant approvals, replace verification, or replace the
independent review required by `common/independent-review-rules.md`.
