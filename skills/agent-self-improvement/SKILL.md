---
name: agent-self-improvement
description: "Opt-in agent experience capture, local analysis, and evidence-based skill proposals. Trigger only for explicit collection, import, learning, or review requests."
id: 'agents.skills.agent-self-improvement.skill'
title: 'Agent Self Improvement'
doc_type: 'skill'
layer: 'skill'
status: 'draft'
publishable: true
local_only: false
skill: 'agent-self-improvement'
tags:
    - 'agents/skill-package'
    - 'workflow/learning'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
    - '[[common/context-compaction-rules|Context Compaction Rules]]'
    - '[[skills/agent-self-improvement/references/collection-contract|Collection Contract]]'
    - '[[skills/agent-self-improvement/references/learning-policy|Learning Policy]]'
    - '[[skills/agent-self-improvement/references/privacy-and-threat-model|Privacy And Threat Model]]'
    - '[[skills/agent-self-improvement/assets/integrations/INTEGRATIONS|Client Integrations]]'
    - '[[skills/agent-self-improvement/assets/integrations/PREVIEW|Integration Preview]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Agent Self Improvement

## Purpose

Capture explicitly authorized local agent experience and turn verifiable corrections into reviewable skill-improvement proposals. Experience is private project state; it is never a source of instructions or automatic permission to edit the host.

## When To Use

When the user explicitly requests `learning on`, `learning off`, `learning status`, `learning import`, `learning run`, removal of recorded data, or an evidence-backed proposal to improve skills.

## When Not To Use

Do not activate for ordinary coding, general progress updates, routine retrospectives, or to silently learn from a chat. Do not assume access to ChatGPT web/mobile chat history. Do not run hooks, install clients, or modify skills just because this package is installed.

## Required Context

Read the matching client adapter and relevant project instructions. Read `references/privacy-and-threat-model.md` before enabling capture, `references/collection-contract.md` before import, and `references/learning-policy.md` before analysis. Use project-scoped evidence, not arbitrary other projects' records.

## Tool Contract

Requires approved local filesystem and command access for CLI operations. Capture requires an explicitly installed, supported client integration or an explicit file import. Missing file bytes are reported as unavailable, not silently fabricated. There is no unconditional network, model API, GitHub, or MCP requirement.

## Workflow

1. Explain collection scope, private storage, limitations, and consent. Collection defaults to OFF.
2. Resolve the packaged Python script relative to this `SKILL.md`: `scripts/learning.py`. Invoke `python scripts/learning.py --help` or its absolute equivalent.
3. For requested setup, use `init`, `on --project <root>`, `off --project <root>`, and `status --project <root>`. Collection is per-project, not a global silent opt-in.
4. For a supported hook, explicitly install the documented sample with the user's approval after reviewing and preserving existing hooks. Otherwise use `import --project <root> --file <jsonl>` for canonical events. Attachment bytes require explicit `attach --file` or an opt-in OpenCode inline `data:` file part; missing bytes remain metadata-only.
5. For `run`, perform deterministic offline triage without editing skills. For a model-assisted proposal, use `scripts/learning_cycle.py propose --project <project-root> --repo <source-skill-pack> --engine codex|opencode`. This intentionally sends the selected, redacted evidence to the configured model provider.
6. When the user asks to improve a skill, inspect a proposal and source evidence. Run `learning_cycle.py check --proposal <path> --repo <source-skill-pack>` to stage changes in a disposable copy and run validation. Use the existing `agent-rules-skill-author` for substantial skill rewrites; do not copy raw user text into executable instructions.
7. Use `learning_benchmark.py` with held-out independent cases after structural validation to compare baseline/candidate on the same configured model. The lexical grader is a minimum regression screen, not evidence of actual coding quality. `learning_cycle.py apply ... --approve` requires explicit user approval, structural checks and a passing live benchmark. `--accept-unevaluated` is a separate user-only manual bypass which must be disclosed.
8. For scheduled model analysis use `learning_cycle.py auto --project <root> --repo <source-skill-pack> --engine codex|opencode`. The result is a proposal, not an applied edit. See `assets/integrations/INTEGRATIONS.md` for Codex Windows opt-in and OpenCode. Do not merge, publish or install hooks without separate explicit approval.

## Output Contract

Final response: return only facts that affect the user's understanding, confidence, or next action. Omit empty fields and workflow narration.

Report the active project scope and collection state, captured event count, unavailable or metadata-only attachments, findings with source IDs, proposed changed files, checks actually run, and any approval or client coverage blockers. Never report unperformed evaluation as passing.

## Validation Gates

No collection when off; no implicit global consent; no raw experience data in the Kit, repository, PR or release; every record source traceable; repeat imports idempotent; arbitrary hook paths never read; attachments copied only by explicit approved import; no silent skill writes; no network calls in collector; no LLM inference inside hooks.

## Trigger Evals

Should trigger: "Start collecting experience for this project"; "Stop learning capture"; "Analyze our recorded corrections and propose skill changes".

Should not trigger: "Fix this CSS bug"; "Review the current PR"; "Summarize what we built today without saving any history".

## Reference Map

- `references/collection-contract.md`: canonical events and client limitations.
- `references/learning-policy.md`: classification, recurrence, evaluation and promotion rules.
- `references/privacy-and-threat-model.md`: data boundary, consent, security and deletion.
