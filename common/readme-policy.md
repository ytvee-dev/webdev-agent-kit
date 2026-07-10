---
id: 'agents.common.readme-policy'
title: 'README Read And Edit Policy'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'docs/readme'
    - 'evidence/authority'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/policy-precedence|Policy Precedence]]'
    - '[[common/host-project-documentation-boundary|Host Project Documentation Boundary]]'
    - '[[common/documentation-maintenance|Documentation Maintenance]]'
depends_on: []
---

# README Read And Edit Policy

Purpose: allow useful targeted README context without treating human-facing documentation as technical proof or silently editing it.

## Read Boundary

`README.md` may be read when relevant after the task is classified, including when the user asks about README content, project intent, setup or run guidance, onboarding, an audit, or documentation drift.

Do not read README by default for routing, skill selection, source inventory, or every code change. Read only the sections needed for the current question.

If the user asks to read or explain README, inspect it directly; do not require the user to paste an excerpt that is already available in the repository.

## Evidence Hierarchy

README is not sufficient technical proof. Resolve runtime and implementation facts through the highest available evidence:

1. Real run or test result.
2. Source code, configuration, or CI.
3. Package scripts or lockfile.
4. README.
5. Assumption.

Use README to locate claims and expected workflows, then confirm technical details with higher evidence. If README conflicts with code, configuration, CI, package scripts, a lockfile, or a real result, trust the higher source and report the drift.

README does not define runtime policy, instruction precedence, skill routing, package inventory, target layout, or validator truth.

## Edit Authorization

Reading does not authorize editing. An existing `README.md` must not be edited unless the user's current request explicitly asks to change that README. A broad request to fix code, update anything outdated, adapt the project, clean documentation, or keep files in sync is not sufficient authorization.

When a README change seems useful but was not requested, leave the file unchanged and report one concise proposed update. Creating a new README, rewriting it, or synchronizing it automatically also requires an explicit user request.

When README editing is explicitly requested, keep the change human-facing and verify every technical claim against higher evidence before writing it.

## Validation Gates

- Targeted README reading has a stated reason.
- Technical claims cite or use higher evidence when available.
- README/code drift is reported rather than silently normalized.
- No README file is created or changed without an explicit current user request.
