---
id: 'agents.common.planning-analysis-rules'
title: 'Planning Analysis Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'workflow/planning'
    - 'workflow/analysis'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/planning-rules|Planning Rules]]'
    - '[[skills/execution-plan-manager/SKILL|Execution Plan Manager]]'
depends_on: []
---

# Planning Analysis Rules

Purpose: find actionable gaps in a standard or deep execution plan before
implementation begins.

## Read-Only Boundary

Planning analysis is a repeatable, read-only pass. It may read the current user
request, confirmed goal, plan, decisions, project overlays, and the minimum
affected source context needed to test plan assumptions. It must not:

- edit the plan, goal, decisions, application code, configuration, or tests;
- install packages or tools;
- run implementation, migration, generation, or auto-fix commands;
- silently repair, reorder, expand, or approve plan scope.

Route proposed remedies back to `create` or `resume` mode. Re-running analysis
against unchanged inputs should preserve finding identity and ordering.

## Required Checks

Check for:

1. an active `AC-###` with no slice or no named verification source;
2. a slice with neither an `AC-###` nor a justified `ENABLER` dependency;
3. duplicate or contradictory criteria, slices, states, or verification claims;
4. conflicts between the current request, confirmed scope, constraints,
   decisions, and plan;
5. implicit package, tool, configuration, test, architecture, or README changes;
6. a slice that exceeds its allowed files or surfaces;
7. parallel slices that can write the same files or state;
8. unknown ownership of application state, data, API behavior, or route surface;
9. vague completion language that cannot produce pass/fail evidence.

Do not invent a finding when the available evidence is merely incomplete. Name
the exact context needed and classify the gap according to its implementation
risk.

## Finding Contract

Use stable zero-padded identifiers in deterministic source order:

```text
PA-001 | category | blocking/high/medium/low | source | evidence | recommendation
```

- `blocking`: implementation cannot safely start without a decision, approval,
  owner, or missing contract.
- `high`: likely scope violation, acceptance gap, or conflicting plan behavior.
- `medium`: material ambiguity with a safe bounded path.
- `low`: clarity or maintainability issue that does not change execution safety.

Show at most 20 finding rows. Aggregate additional findings by category and
severity without losing their count. Cite identifiers, sections, or file paths
instead of copying long plan prose.

## Handoff Gate

- Any `blocking` or `high` finding stops implementation handoff.
- `medium` and `low` findings may proceed only when the remaining risk is named
  and the plan still has an unambiguous safe slice.
- Zero findings means the analyzed plan is internally ready to hand off; it is
  not proof that implementation will satisfy the goal.
- Lightweight workflows bypass planning analysis unless they have already been
  escalated to standard or deep work.
