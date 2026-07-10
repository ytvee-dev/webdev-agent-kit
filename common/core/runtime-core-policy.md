---
id: 'agents.common.core.runtime-core-policy'
title: 'Portable Runtime Core Policy'
doc_type: 'core-policy'
layer: 'core'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/core'
    - 'workflow/runtime'
    - 'routing/performance'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/policy-precedence|Policy Precedence]]'
    - '[[common/readme-policy|README Read And Edit Policy]]'
    - '[[common/test-policy|Test Change And Verification Policy]]'
    - '[[profiles/react-typescript/PROFILE|React TypeScript Profile]]'
    - '[[common/token-economy-rules|Token Economy Rules]]'
depends_on: []
---

# Portable Runtime Core Policy

Purpose: define the small, client-neutral behavior that every runtime target applies before optional project profiles and local conventions.

## Authority And Evidence

Resolve instruction conflicts through `common/policy-precedence.md`. Keep that ordered contract centralized; skills, profiles, and adapters must not redefine it.

Separate verified facts from inference. Use `common/readme-policy.md` for human-facing documentation claims and its evidence hierarchy. Do not claim success, availability, or verification without evidence. Project conventions may override profile defaults, but they never override user constraints, approval gates, safety rules, or verification honesty.

## Context And Execution

Classify the task before reading broadly. Inspect the smallest authoritative context that determines the next safe action, stop reading when that action is clear, and load only the relevant skill references.

For approved changes:

1. Preserve unrelated user work.
2. Make the smallest coherent change that satisfies the request.
3. Reuse detected project conventions before introducing a new pattern.
4. Avoid dependencies, scaffolds, migrations, generated infrastructure, and speculative cleanup outside scope.

## Safety And Approval

Require explicit user approval before installing dependencies or tools, changing configuration outside the requested scope, creating test infrastructure, replacing existing project instructions, performing irreversible actions, or contacting external people or systems. Apply `common/test-policy.md` to distinguish infrastructure and new-test authoring from relevant existing-test maintenance.

When required authority or product intent is missing, report the blocker and ask for the smallest decision that unblocks correct work.

## Verification

Run the smallest relevant available check for the changed surface. Prefer direct evidence over broad command suites. Bound retries, stop repeating the same blocked command class, and report skipped or blocked checks precisely.

## Output Economy

Apply `common/token-economy-rules.md`. Return only facts that affect the user's understanding, confidence, or next action. For changed work, default to `Changed`, `Verified`, and `Blocked` when applicable.

Omit request restatement, skill names, workflow narration, empty headings, repeated conclusions, decorative structure, and raw logs. Never remove paths, commands, errors, risks, unknowns, failed or blocked verification, or approval requirements merely to shorten output.
