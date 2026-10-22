---
id: 'agents.docs.install.claude-agents'
title: 'Claude Project Adaptation And Native Roles'
doc_type: 'guide'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags:
    - 'client/claude-code'
parent:
    - '[[docs/install/claude-code]]'
related:
    - '[[common/claude-agent-routing-policy]]'
    - '[[docs/install/vscode-claude]]'
    - '[[docs/install/upgrade]]'
depends_on: []
---

# Claude Project Adaptation And Native Roles

The current release candidate includes 23 shared skills and nine plugin agents.
Claude Code and the VS Code Claude alias use the same generated plugin.
Complete the [Claude installation](claude-code.md) or
[VS Code installation](vscode-claude.md) first.

## What Is Shared

| Capability | Claude adaptation |
| --- | --- |
| Planning, implementation, debugging, design and visual QA | Same portable skills; verify required tools in the active session |
| Project context, path indexes, goals and loop memory | Host `.agents/project/`, outside the installed plugin |
| Runtime instructions | Each skill explicitly loads plugin-local `AGENTS.md` using `${CLAUDE_SKILL_DIR}` |
| Bounded subagent work | Nine native `agents/` definitions, using actual discovered identifiers |
| Model selection | Inherit by default; approved account-specific overrides only when supported and verified |
| Review and handoffs | Shared task/report contracts and exact review helper, invoked from the plugin root |
| Updates and rollback | Native plugin manager; preserve host settings, custom agents, context and model choices |

## Adapt An Existing Project

From the host project, invoke `/webdev-agent-kit:project-onboarding-adapter` and
provide this scope:

```text
Adapt this Claude plugin to my project. Preserve CLAUDE.md, imported rules,
existing agents, models, permissions and global settings. Record verified
project facts in .agents/project/. Discover the plugin's native roles and
inspect supported model choices within my existing budget. Verify only new or
changed approved bindings with tiny read-only checks. Do not change app code.
```

To list roles without calling models, add: `Facts only; no model changes or canaries.`
Plan Mode returns a proposal without writing project context or settings.
If persistent context imports are needed, review the proposed minimal host
`CLAUDE.md` merge. Never replace existing instructions or import a missing
`.agents/AGENTS.md`; the plugin carries its own policy and skills.

## Native Roles

| Suffix | Suitable work | Tools |
| --- | --- | --- |
| `wdk-lookup` | Focused file lookups | Read, Glob, Grep |
| `wdk-worker-light` | Fully specified mechanical edits | Read, Glob, Grep, Edit, Write, Bash |
| `wdk-worker` | Routine implementation | Same worker tools |
| `wdk-complex` | Ambiguous debugging or integration | Same worker tools, within explicit scope |
| `wdk-reviewer-light` | Narrow requested review | Read, Glob, Grep |
| `wdk-reviewer` | Review changes across several components | Read, Glob, Grep |
| `wdk-reviewer-deep` | Critical security or data-loss review | Read, Glob, Grep |
| `wdk-architect` | Architecture or migration decisions | Read, Glob, Grep |
| `wdk-architect-deep` | Architecture with many interacting parts | Read, Glob, Grep |

Use the actual registry identifier, normally `webdev-agent-kit:<suffix>`.
Descriptions define when to delegate; small work stays in the main session.
Only the coordinator dispatches. Children receive explicit host/plugin roots,
criteria, owned paths, selected skills, evidence and retry budgets.

All shipped roles use `model: inherit`. Role names are not model tiers and do
not prove different reasoning settings. During onboarding, inspect the current
account catalog and native dispatch signature before selecting a cheaper or
stronger adequate model. Preserve existing model choices and cost limits.
Do not apply Codex TOML, GPT IDs or unsupported effort values to Claude.

## Verify Each Level

1. `claude plugin list` establishes enabled installation and version.
2. Use `claude plugin details webdev-agent-kit@webdev-agent-kit` if your CLI
   supports it, or inspect `/plugin` and `/agents`. Compare the list with the
   installed release. Seeing a role in the list does not prove it can run.
3. Refresh with `/reload-plugins` or a new session. Inspect actual native agent
   identifiers, effective tools and permitted dispatch options.
4. For authorized live verification, send one existing-file lookup to a newly
   selected role. Retain actual tool events, model metadata and returned file
   evidence. Do not invoke every role just to fill a table.

Keep results in `.agents/project/claude-agent-profile.md`. Missing credentials,
disabled delegation or unknown tools leave affected roles unverified and normal
single-agent work available. Keep secrets out of profiles and logs. Read-only
reviewers return findings for the coordinator and cannot use shell or edit tools.

## Update And Troubleshoot

Use [upgrade and rollback](upgrade.md); never patch a versioned plugin cache or
duplicate plugin agents into `.claude/agents`. Preserve existing custom agents
and mark affected evidence stale after plugin, account or tool changes.

- Skills missing: verify the correct enabled plugin, version and actual client.
- Roles missing: verify `agents/` in the plugin, refresh and inspect native names.
- Paths fail: use the invoked skill's base directory, not the current host folder.
- Model override rejected: keep inheritance; report the unsupported control.
- Review helper unavailable: run its absolute plugin path with host `--root` and
  host plan paths. No helper or model installation is implied by an ordinary task.

The [official plugin-development sources](https://github.com/anthropics/claude-code/tree/main/plugins/plugin-dev)
and [Claude subagent documentation](https://code.claude.com/docs/en/sub-agents)
define client mechanisms. This kit's role assignments are project policy.
