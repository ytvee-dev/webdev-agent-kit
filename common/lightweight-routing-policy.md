---
id: 'agents.common.lightweight-routing-policy'
title: 'Lightweight Routing Policy'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'routing/performance'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/prompt-intent-routing-rules|Prompt Intent Routing Rules]]'
    - '[[skills/project-context-adapter/SKILL|Project Context Adapter]]'
    - '[[skills/mcp-toolchain-manager/SKILL|MCP Toolchain Manager]]'
depends_on: []
---

# Lightweight Routing Policy

Purpose: keep simple lookup, explanation, and narrow inspection tasks fast without weakening safety for code-changing work.

## Fast Path Triggers

Use the fast path when the user asks to:

- find where something is implemented;
- inspect how a function, selector, component, style, route, or config works;
- explain a small code fragment;
- locate related files;
- answer a narrow project question;
- check whether a specific pattern exists.

## Fast Path Context Budget

For a fast path task:

1. Read `AGENTS.md` only when routing is unclear or the task may change files.
2. Search narrowly first.
3. Read only the top relevant files or snippets.
4. Do not read all skills, all common rules, all references, all project overlays, `README.md`, or `dist/**`.
5. Do not invoke planning, architecture, onboarding, MCP audit, visual QA, quality review, or documentation-maintenance workflows.
6. Do not run validation commands unless files were changed or the user asked for verification.
7. Answer with findings and cite the exact files or paths inspected.

## Escalation

Escalate out of the fast path only when targeted inspection shows that:

- a code change is required;
- the root cause is unclear after the first narrow search;
- more than one implementation slice is needed;
- architecture, state ownership, routing, data flow, tooling, or generated assets are affected;
- the user asks for audit, refactor, implementation, PR, onboarding, or broad review.

When escalation is needed, state the reason briefly and then load the smallest relevant skill set.

## Prohibited Fast Path Work

During fast path tasks, do not:

- create plans or checkpoint files;
- update `project/**` overlays;
- inspect MCP installation state;
- start local servers;
- use Browser or Playwright;
- perform broad repository scans;
- audit rules or skills;
- change files.

## Validation Gates

- The first answer must be possible after narrow search and targeted reads.
- A fast path task must not load heavy skills unless escalation is explicitly justified.
- If the user asks only a question, answer the question before proposing implementation.
