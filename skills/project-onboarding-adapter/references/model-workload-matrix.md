---
id: 'agents.skills.project-onboarding-adapter.references.model-workload-matrix'
title: 'Task, Model And Reasoning Selection'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/model-routing'
parent:
    - '[[skills/project-onboarding-adapter/SKILL]]'
related:
    - '[[common/codex-model-routing-policy]]'
    - '[[skills/frontend-architecture-planner/SKILL]]'
    - '[[templates/project/model-routing-profile]]'
depends_on: []
---

# Task, Model And Reasoning Selection

Use during model onboarding/reconfiguration, or when a nontrivial task needs
executor selection. Apply to the next bounded action, not the whole skill.
Model capability and reasoning effort are separate decisions. A cheap model at
maximum effort is not assumed equivalent to a stronger model at medium effort.

Sections: starting matrix; effort and escalation; WebDev examples and near
misses; evidence and cost.

## Starting Matrix

These are starting recommendations, not hardcoded production bindings. Resolve
exact IDs, supported efforts, modalities and cost from the current account
catalog and official sources; store the resulting bindings locally. The named
families describe the September 2026 catalog and must be revalidated when stale.

| Action and risk | Starting family / effort | Role |
| --- | --- | --- |
| Tiny lookup, typo, deterministic command | Primary/tools inline; no child overhead | Inline |
| Bounded extraction or fact gathering | Luna / low | `wdk_lookup` |
| Fully specified repeated edit, no behavioral decisions | Luna / medium | `wdk_worker_light` |
| Ordinary component/page implementation within established boundaries | Terra / medium | `wdk_worker` |
| Ambiguous multi-file bug, integration or behavior-preserving refactor | Sol / high; medium for a bounded, well-understood slice | `wdk_complex` |
| Substantial correctness review across boundaries | Sol / high | `wdk_reviewer` |
| New architecture, competing ownership/state/routing boundaries, consequential migration design | Astra / high | `wdk_architect` |
| Exceptionally coupled architecture with irreversible consequences and a justified larger budget | Astra / xhigh | `wdk_architect_deep` |
| Explicitly requested narrow, low-risk independent review | Terra / high | `wdk_reviewer_light` |
| Critical architecture, security or data-loss review | Astra / high | `wdk_reviewer_deep` |

Full onboarding normally covers the four base roles plus `wdk_worker_light` and
`wdk_architect` when supported and within the user's limits. This makes all four
capability tiers reachable without requiring their use on every task. Add the
three specialized variants only for demonstrated workload needs, not merely
because the catalog offers them. Never silently replace existing working
bindings; compare the coverage, retain them, and record a gap or perform an
explicitly requested reconfiguration. If a family is unavailable, use a proven
adequate alternative within the cost ceiling or report the capability gap.

## Effort And Escalation

- `low`: simple evidence extraction with little reasoning. The colloquial
  "light" describes workload; it is not an API effort value.
- `medium`: normal bounded implementation or a well-defined reasoning slice.
- `high`: interacting constraints, unclear causes, assumptions and edge cases.
- `xhigh`: exceptional coupling or critical decisions where added reasoning has
  a concrete purpose. Do not require a cheaper failed attempt first when risk
  is already known.
- `max` / `ultra`: only supported values, explicit deep-reasoning need and an
  approved cost/latency budget; never universal defaults or automatic retries.
  Check execution semantics too: if an effort enables automatic delegation,
  do not use it where it would violate coordinator-only or concurrency limits.

Select a verified fixed binding that matches both decisions. Native role
parameters cannot be changed by prose. If the desired model/effort pair is not
configured and verified, retain a suitable existing executor or report the gap;
do not rewrite native files during ordinary work. Onboarding may configure a
justified optional role at another supported effort. Do not auto-upgrade all
roles or launch a canary for every possible model/effort combination.

Escalate directly for known capability/risk mismatch; escalate after new
evidence exposes one. A permissions, missing-file, authentication or tool error
is not a reasoning failure. Correct the evidence or stop, rather than cycling
through expensive models. Preserve the shared attempt budget. After the hard
decision, return the approved implementation slices to the cheaper adequate
executor. More capable models do not get extra product or mutation authority.

## WebDev Examples And Near Misses

- `frontend-architecture-planner`: use Astra for a genuinely new ownership or
  migration decision; locating an existing component or applying an established
  folder rule remains inline/Terra. The word "architecture" alone is not a tier.
- `goal-planner`, `execution-plan-manager`, `greenfield-project-builder`: use
  Sol for difficult decomposition, Astra for consequential architectural
  tradeoffs, then Terra for agreed slices. Product intent still comes from the user.
- Design intake: Luna may collect metadata, but exact visual inspection needs
  image support and real Figma/browser/screenshot evidence. Use Terra for a
  bounded known component; Sol for ambiguous interactions across states; Astra
  only when the design exposes consequential system boundaries. Never invent
  product behavior or delegate away missing visual evidence.
- Debugging/refactoring: Terra for a localized known fix, Sol for a causal
  investigation across modules, Astra for a demonstrated architectural cause.
- Lint, context refresh, upgrades and packaging: deterministic tools or bounded
  Luna/Terra work; collisions and environment errors do not justify Astra.
- Independent review is risk-based and fresh-context, not mandatory on every
  task. A review role cannot implement its own fixes or certify its own work.

## Evidence And Cost

Official sources: [models](https://learn.chatgpt.com/docs/models),
[subagent effort guidance](https://learn.chatgpt.com/docs/agent-configuration/subagents),
[pricing](https://learn.chatgpt.com/docs/pricing). The task/role assignments above
are Kit design judgments informed by these sources, not an OpenAI guarantee.
Measure accepted outcomes, including coordinator context, cache, retries,
review and latency. Record units and date locally; subscription credits are not
API dollars. Keep canaries tiny and re-run only changed/new bindings or drift.
Passing a dispatch canary proves routing, not comparative architectural quality.
