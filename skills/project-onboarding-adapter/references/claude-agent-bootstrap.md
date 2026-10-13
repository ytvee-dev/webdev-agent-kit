---
id: 'agents.skills.project-onboarding-adapter.references.claude-agent-bootstrap'
title: 'Claude Plugin Adaptation And Agent Discovery'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'project-onboarding-adapter'
tags:
    - 'client/claude-code'
parent:
    - '[[skills/project-onboarding-adapter/SKILL]]'
related:
    - '[[common/claude-agent-routing-policy]]'
    - '[[templates/project/claude-agent-profile]]'
depends_on: []
---

# Claude Plugin Adaptation And Agent Discovery

Use only for full Claude Code onboarding or explicit Claude role reconfiguration.
Updates and context refresh preserve existing choices; facts-only or Plan Mode
requests do not change native configuration or run model probes.

## Locate And Preserve

1. Locate the installed plugin using the invoked skill's client-supplied base
   directory. `${CLAUDE_SKILL_DIR}/../..` is the plugin root for shipped skills.
   Read its `AGENTS.md` and sole `adapters/claude-code.md`; do not assume the plugin
   is inside the host project or use a stale marketplace source path.
2. Inspect applicable host `CLAUDE.md`, imported rules, settings and existing
   `.claude/agents` before proposing changes. Keep all existing rules. Native
   plugin installation does not require a host `.agents/AGENTS.md` pointer.
3. Record project facts, paths, verification commands, design evidence and tool
   capabilities under host `.agents/project/`. Never write into the installed
   cache. If persistent access to those facts is requested, propose a minimal
   host `CLAUDE.md` reference to the relevant populated overlays; do not hardcode
   a versioned plugin-cache path or replace existing instructions.

## Discover And Bind

1. Check the plugin inventory with `claude plugin list` or `/plugin`, and native
   agents with `/agents` in the current session. Use `/reload-plugins` or a fresh
   session when installation changed. Preserve disabled-plugin and managed
   permission decisions rather than enabling them silently.
2. Match the nine role suffixes in `common/claude-agent-routing-policy.md` to the
   actual namespaced registry. Detect collisions and existing custom roles.
   Reuse working roles; do not copy plugin agents into `.claude/agents` or create
   competing global agents. Missing registry access means discovery-unverified.
3. Shipped roles inherit the main model. For economical dispatch, inspect the
   current account model catalog and the actual native tool signature. Record
   adequate small, balanced and stronger choices with modalities, supported
   effort and cost constraints. Use only supported model/effort overrides; never
   hardcode dated IDs or assume the GPT workload matrix applies. If overrides
   are unavailable, preserve inheritance and state that cost routing is unverified.
4. Save evidence in `templates/project/claude-agent-profile.md`, copied to host
   `.agents/project/claude-agent-profile.md` with local-only metadata. Keep provider
   secrets out of profiles, task packets and logs. Do not rewrite settings,
   permissions, primary models or existing native agent files.

## Verify Within Scope

1. A full execution-mode onboarding request allows tiny read-only checks of new
   or changed approved bindings when credentials, native delegation and budget
   are available. Send the host/plugin roots and one existing file to the
   relevant role. Inspect actual agent identifier, model, effective tools and
   returned file evidence; self-reported identity is insufficient. Do not invoke
   all nine agents merely to fill a table or repeat unchanged checks.
2. Mark each role installed, discovered, activation-unverified, verified, blocked
   or stale. Installation and CLI validation are not model execution. Missing
   authentication or permission leaves normal single-agent work available.
3. Route bounded work and reviews through the verified profile. Preserve the
    shared retry budget, coordinator-only dispatch, exact review scope and
    independent-review boundaries. Recheck only affected bindings after version,
    auth, tool or configuration drift.

## Official Mechanisms

Use current Claude Code [subagents](https://code.claude.com/docs/en/sub-agents),
[plugins](https://code.claude.com/docs/en/plugins),
[skills](https://code.claude.com/docs/en/skills) and
[model configuration](https://code.claude.com/docs/en/model-config) documentation.
The official `anthropics/claude-code` plugin-development examples also document
native `agents/`, `model: inherit` and tool allowlists. The role taxonomy and
dispatch recommendations are Kit design choices, not provider quality guarantees.
