---
id: 'agents.common.claude-agent-routing-policy'
title: 'Claude Native Agent Routing'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/model-routing'
parent:
    - '[[adapters/claude-code]]'
related:
    - '[[common/subagent-handoff-rules]]'
    - '[[common/independent-review-rules]]'
    - '[[skills/project-onboarding-adapter/references/claude-agent-bootstrap]]'
    - '[[templates/project/claude-agent-profile]]'
    - '[[agents/claude-code/wdk-lookup]]'
    - '[[agents/claude-code/wdk-worker-light]]'
    - '[[agents/claude-code/wdk-worker]]'
    - '[[agents/claude-code/wdk-complex]]'
    - '[[agents/claude-code/wdk-reviewer-light]]'
    - '[[agents/claude-code/wdk-reviewer]]'
    - '[[agents/claude-code/wdk-reviewer-deep]]'
    - '[[agents/claude-code/wdk-architect]]'
    - '[[agents/claude-code/wdk-architect-deep]]'
depends_on: []
---

# Claude Native Agent Routing

Apply only in Claude Code with discovered plugin agents, permitted native
delegation and current evidence in host `.agents/project/claude-agent-profile.md`.
Otherwise retain normal single-agent execution. Do not run the Codex TOML helper.

## Select The Next Executor

Keep trivial tasks and deterministic commands inline. Select a role for the next
bounded action, not an entire skill or workflow:

| Role suffix | Work | Boundary |
| --- | --- | --- |
| `wdk-lookup` | Bounded facts and locations | Read-only |
| `wdk-worker-light` | Fully specified mechanical changes | Owned files only |
| `wdk-worker` | Ordinary implementation | Approved slice |
| `wdk-complex` | Ambiguous debugging and integration | No scope expansion |
| `wdk-reviewer-light` | Narrow requested review | Read-only, independent |
| `wdk-reviewer` | Cross-boundary correctness review | Read-only, independent |
| `wdk-reviewer-deep` | Critical security or data-loss review | Read-only, justified budget |
| `wdk-architect` | Consequential architecture and migration | Read-only, user owns decisions |
| `wdk-architect-deep` | Exceptionally coupled architecture | Read-only, explicit deeper budget |

Resolve the actual namespaced identifier from the client's registry, normally
`webdev-agent-kit:<suffix>`. Never assume a role name changes the active model.
Shipped agents use `model: inherit`; installation does not select another model.
During approved onboarding, record the account's available models, capabilities,
supported effort controls and cost ceiling. Use a cheaper adequate model for
bounded work only through an actually supported dispatch override. Stronger
models require capability evidence and budget; there is no silent expensive
fallback. Do not translate GPT effort values or model IDs into Claude settings.

## Dispatch And Evidence

Use `common/subagent-handoff-rules.md`. Pass a self-contained packet with absolute
plugin/host roots, selected skill, owned files, criteria, evidence and retry
budget. Plugin agents do not inherit the coordinator's full conversation.
The coordinator alone delegates; use sequential dispatch by default. Parallel
work requires independent scope and task authorization, with no overlapping
writers. Never ask a child to install tools, publish or change permissions.

Read-only roles have no Bash, Edit, Write or delegation tools. A worker's tools
do not authorize new tests, dependency changes or broader edits. Visual tasks
need actual image evidence and a capable permitted executor; use the primary
session when the selected role cannot inspect it.

Separate installation, discovery, configured model, observed dispatch and
verified behavior. A local model override needs actual invocation metadata;
configuration or self-report alone does not prove activation. Respect Plan Mode,
explicit no-model-change scope and disabled delegation. Preserve existing local
agents, primary model, permissions and global settings. Authentication and tool
failures are not reasoning failures and do not reset retry budgets.

Use fresh-context review when required by `common/independent-review-rules.md`.
An implementer cannot certify its own work; label unavailable independent review
honestly. Compare total coordinator/child/retry cost per accepted outcome, not
token price alone. Refresh stale bindings only through approved onboarding.
