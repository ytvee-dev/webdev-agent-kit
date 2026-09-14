---
id: "agents.docs.architecture.superpowers-adoption"
title: "Superpowers-Informed Execution Improvements"
doc_type: "guide"
layer: "docs"
status: "active"
publishable: true
local_only: false
tags: []
parent:
  - "[[AGENTS]]"
related: []
depends_on: []
---

# Superpowers-Informed Execution Improvements

## Audit Scope And Differences

Compared WebDev `d01a66da060f739f36cd39cf8ff06da96141abc8` (1.0.0) with
Superpowers `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` (6.3.0), inspecting runtime
instructions, helpers, evaluation machinery, docs and relevant issues.
WebDev already has GPT role bootstrap, criterion/slice traceability, independent
review, bounded retries and a live-eval runner. This release improves their
handoffs and activation, rather than adding duplicate orchestrators.

WebDev's strengths remain frontend-specific boundaries and proportional work.
Superpowers provides concrete task/report/diff handoffs and scoped repair loops.
Its mandatory review/TDD workflow is not imported as a blanket frontend policy.

## Adopted With Adaptation

| Source idea | WebDev implementation |
| --- | --- |
| Self-contained task briefs and file-based reports | Existing plan slices export exact constraints/interfaces, owned paths and remaining retries; stable AC/S identities remain authoritative |
| Whole-task review diff, not only last commit | New dependency-free packager records full commit range or scoped staged/unstaged/untracked state; no forced commit |
| Scoped re-review | Existing reviewer judges open findings and repair-induced risk; explicit dependency exception prevents narrow blind spots |
| Isolated per-plan artifacts and recovery | Additive local run namespaces, while canonical plans retain completion/evidence pointers |
| Cost-shaped dispatch | Batch same-shape mechanical work only when useful; keep trivial work inline and preserve approved roles/retry caps |
| Behavioral evidence instead of slogans | Extend the existing live scenarios; separate schema, executable-helper, synthetic-runner and actual model evidence |

New reusable wording and the Python helper are kit-specific implementations, not
an installation or wholesale copy of the upstream skills.

## Issues That Changed The Design

[WebDev #71](https://github.com/ytvee-dev/webdev-agent-kit/issues/71) reports roles
configured but inactive. The old installer rejected `agents.enabled = false`
but did not reject `features.multi_agent = false`. A regression test reproduced
that omission. The new request optionally enables one explicitly approved local
key and validates all unrelated parsed values; it never edits global trust.
Onboarding now avoids requiring delegation before it can configure delegation.

[Superpowers #1075](https://github.com/obra/superpowers/issues/1075) reports
ambiguous completion after plan execution. WebDev therefore keeps canonical
completion and evidence pointers, instead of copying unconditional scratch cleanup.
[Superpowers #2046](https://github.com/obra/superpowers/issues/2046) reports an
import failure presented as behavioral test evidence. WebDev explicitly separates
structural failure from an executed assertion rejecting a wrong outcome.
These are reported failure modes, not a claim that every upstream version fails.

## Deliberately Not Adopted

No mandatory agents/review/design approval for every small edit; no global
TDD override; no default increase to five repair rounds; no escalation merely
because a command failed; no automatic trust restoration; no marking required
criteria verified when retries end. No savings percentage is claimed.

## Sources And Compatibility

Primary references inspected on 2026-09-14:

- [Pinned SDD workflow and prompts](https://github.com/obra/superpowers/tree/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/subagent-driven-development)
- [Pinned test quality rules](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/test-driven-development/writing-good-tests.md)
- [Pinned skill testing methodology](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/writing-skills/SKILL.md)
- [Official Codex subagents](https://developers.openai.com/codex/subagents)
- [Official configuration reference](https://developers.openai.com/codex/config-reference)
- [Official configuration precedence and trust](https://developers.openai.com/codex/config-basic)

Current official docs enable subagents by default and describe both native
configuration and role-specific model/effort fields. Installed-version schema,
account availability and effective policy still govern a host installation.
Project configuration can be ignored when untrusted. A role's read-only default
does not replace verification of inherited permissions. These facts require
runtime evidence; the local helper cannot certify them.

See the [release checklist](../release/1.1.0-checklist.md) and
[live evaluation guide](behavior-evaluation.md) for verification boundaries.
