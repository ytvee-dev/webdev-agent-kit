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
    - '[[common/smart-verification-budget|Smart Verification Budget]]'
    - '[[common/diff-impact-verification-rules|Diff Impact Verification Rules]]'
    - '[[common/mcp-availability-detection-rules|MCP Availability Detection Rules]]'
    - '[[skills/project-context-adapter/SKILL|Project Context Adapter]]'
    - '[[skills/mcp-toolchain-manager/SKILL|MCP Toolchain Manager]]'
depends_on: []
---

# Lightweight Routing Policy

Purpose: keep simple lookup, explanation, narrow inspection tasks, and small local fixes fast without weakening safety for code-changing work.

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

## Micro UI Fix Fast Lane

Use this lane for isolated frontend presentation fixes that can be completed as a `Lightweight Workflow`.

Typical examples:

- render existing text differently in one component;
- use an already-installed markdown renderer for one chat message surface;
- adjust small CSS spacing, wrapping, compact heading, or list styles;
- change a local background, decorative mask, or color value;
- fix one component branch or one local visual state;
- change a local class name or component prop mapping without touching public APIs.

Hard limits:

- target one or two files by default, unless the user explicitly named a few equivalent local surfaces;
- do not add packages;
- do not change API, stores, routing, data flow, build tooling, or architecture layers;
- do not create a goal contract, execution plan, loop contract, project memory update, MCP audit, or independent review by default;
- do not start a dev server by default;
- do not run full-repository lint or format before changed-file checks;
- do not inspect MCP installation state by default.

## Micro UI Fix Context Budget

For a micro UI fix, default to this maximum context before patching:

1. One routing or lightweight policy file only when routing is unclear.
2. The owner component or renderer.
3. The adjacent style file when styling is affected.
4. `package.json` only when dependency presence matters.
5. Config files only after a command fails or when the command target is unknown.
6. `node_modules` only when TypeScript import or exported type shape cannot be inferred from package usage, project examples, or package metadata.

Do not read broad project overlays, all skill files, all common rules, full README, generated `dist/**`, or unrelated source trees for a micro UI fix.

## Lightweight Verification Ladder

For a micro UI fix or other lightweight code-changing task, read `common/smart-verification-budget.md` and use the smallest honest level.

Default ladder:

1. Changed-file formatting.
   - Use `prettier --check` or `prettier --write` only on changed files when Prettier exists.
2. Changed-file lint.
   - Use ESLint only on changed TypeScript or JSX files when possible.
   - Do not lint CSS files when the project lint config ignores CSS.
3. Type or build check.
   - Run the smallest existing typecheck or build command when imports, JSX, TypeScript, dependency usage, or bundling behavior changed.
4. Full repository checks.
   - Run only when changed-file checks pass and the repository is known clean, or when the user explicitly asks for full verification.
5. Rendered QA.
   - Run only when the user explicitly requests browser evidence, the route is accessible without new setup, and Browser or Playwright navigation tools are available.

Stop after sufficient evidence. Do not switch to broader commands merely to create a more impressive report.

## CSS-Only Fast Lane

For CSS-only color, background, decorative mask, border color, or non-layout visual token changes:

1. Read `common/diff-impact-verification-rules.md`.
2. Check changed CSS files with the smallest formatter or static check when available.
3. Do not run full-repository ESLint by default.
4. Do not run TypeScript by default.
5. Do not start a dev server by default.
6. Do not inspect Playwright packages, browser automation packages, or MCP installation state.
7. Do not test unrelated routes.
8. Escalate only when the user asks for rendered evidence, the same issue repeats, or the diff affects layout, responsive behavior, overflow, focus, contrast, or other material visual risk.

## Micro UI Fix Stop Condition

Stop a micro UI fix after all applicable conditions are met:

- the root cause is tied to the inspected owner file;
- the patch stays inside the hard limits;
- changed-file checks pass or unsupported checks are honestly reported;
- type/build verification passes when imports, JSX, or TypeScript changed;
- heavier rendered QA is either unnecessary, explicitly skipped with reason, or blocked by unavailable route/session/tooling.

The final report should include changed files, root cause, verification, skipped heavier checks, and remaining risk. Do not start a local server after source checks and build pass unless rendered evidence is explicitly requested or high-risk.

## Escalation

Escalate out of the fast path only when targeted inspection shows that:

- a code change is required;
- the root cause is unclear after the first narrow search;
- more than one implementation slice is needed;
- architecture, state ownership, routing, data flow, tooling, or generated assets are affected;
- the user asks for audit, refactor, implementation, PR, onboarding, or broad review.

Escalate a micro UI fix out of Lightweight Workflow only when targeted evidence shows that it violates the micro UI hard limits.

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

During micro UI fixes, do not:

- invoke separate planning, architecture, visual QA, quality review, onboarding, or MCP-toolchain skills by default;
- start local servers after source/build checks pass unless rendered evidence is explicitly required;
- run full-repository checks before changed-file checks;
- expand the patch into unrelated owners to make the UI more generally reusable;
- inspect local browser automation packages as a proxy for MCP availability.

## Validation Gates

- The first answer must be possible after narrow search and targeted reads.
- A fast path task must not load heavy skills unless escalation is explicitly justified.
- A micro UI fix must remain lightweight unless it violates the hard limits.
- CSS-only low-risk changes must not become browser or full-repository verification by default.
- If the user asks only a question, answer the question before proposing implementation.
