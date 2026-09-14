---
id: 'agents.common.codex-model-routing-policy'
title: 'Codex GPT Model Routing'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/model-routing'
parent:
    - '[[AGENTS]]'
related:
    - '[[common/subagent-handoff-rules]]'
    - '[[common/bounded-retry-rules]]'
    - '[[common/independent-review-rules]]'
    - '[[skills/project-onboarding-adapter/references/codex-model-bootstrap]]'
    - '[[templates/project/model-routing-profile]]'
depends_on: []
---

# Codex GPT Model Routing

Purpose: choose a real native executor for the next action, not pretend that
instructions can change the model of a running response.

## Activation

Apply only in Codex with callable native delegation and approved, runtime-verified
roles in local `project/model-routing-profile.md`. Check that its client, auth
mode, configuration fingerprint and role evidence still match the current
session. Missing, stale, disabled or unavailable routing leaves the existing
single-agent workflow intact; report limits only when they affect the task.
Never create configuration during ordinary work. Configuration syntax alone,
a model self-report, a skill name and `agents/openai.yaml` are not runtime proof.

## Executor Selection

Classify the next action using existing workflow rules before broad context
loading. Keep trivial work inline when coordination would cost more than it
saves. Use tools directly for deterministic commands. Do not bind an entire
skill or workflow level permanently to a model.

| Executor | Suitable action | Boundary |
| --- | --- | --- |
| `wdk_lookup` | Bounded read-heavy evidence gathering | No edits or fixers |
| `wdk_worker` | Explicit low-risk implementation slice | Assigned files only |
| `wdk_complex` | Ambiguous cause or cross-boundary reasoning | No scope expansion |
| `wdk_reviewer` | Material-risk independent review | No implementation |

Choose the least costly verified adequate role, considering uncertainty,
consequences, tool access, input modalities, context size and verification.
Image work requires confirmed image support and real visual evidence tools;
a text-only model cannot substitute for screenshot analysis. Retain the
user's primary model and approved cost ceiling. No silent expensive fallback.

## Delegation Contract

Use the actual native delegation tool and the configured role name. A custom
role's fixed model and effort are not overridden by prose; escalation selects
a different approved role. Pass only the selected skill, goal and acceptance
criteria, owned paths, constraints, decisive evidence, required tools, checks,
and remaining attempt budget. Do not forward the full parent transcript.

Use `common/subagent-handoff-rules.md` for self-contained task/report packets
and batching independent same-shape mechanical edits.

Only the coordinator delegates. Default to sequential work; use at most two
concurrent children only for independent, explicitly bounded assignments, and
honor stricter client limits. Never allow overlapping writers. Reuse returned
evidence instead of redoing delegated exploration; verify integration once.

## Escalation And Review

Escalate on a concrete capability mismatch or new evidence, not merely failure.
Permission, authentication and environment errors are blockers, not reasons to
buy more reasoning. Use `common/bounded-retry-rules.md`: model changes do not
reset the shared retry budget. No recursive delegation or endless repair loop.

Independent review follows `common/independent-review-rules.md`, not every
Standard or Deep task. Launch a non-inheriting fresh context using supported
client controls; pass criteria, diff, decisions and verification evidence.
Without real isolation label the pass self-review. After material repairs,
review the repaired diff independently before claiming independent confidence.

## Cost Evidence

Compare total coordinator, child, cached-input, retry, review and integration
usage per accepted outcome. Distinguish subscription credits from API money.
Do not promise a savings percentage without comparable task results. Refresh
model choices only through approved onboarding, not per task or kit update.
