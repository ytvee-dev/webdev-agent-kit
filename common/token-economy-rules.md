---
id: 'agents.common.token-economy-rules'
title: 'Token Economy Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'routing/performance'
    - 'workflow/context'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/lightweight-routing-policy|Lightweight Routing Policy]]'
    - '[[common/prompt-intent-routing-rules|Prompt Intent Routing Rules]]'
    - '[[common/context-compaction-rules|Context Compaction Rules]]'
    - '[[common/verification-loop-rules|Verification Loop Rules]]'
depends_on: []
---

# Token Economy Rules

Purpose: reduce context, thinking, and output token waste without reducing reasoning quality, verification, safety, or functional accuracy.

## Core Principle

Optimize tokens by removing unnecessary context and unnecessary words, not by skipping judgment.

Reduce:

```text
unneeded file reads
broad scans before targeted search
heavy skills for narrow tasks
tool-call narration
pleasantries and filler
repeated conclusions
raw logs when one decisive line is enough
```

Preserve:

```text
acceptance criteria
user constraints
code semantics
exact commands
exact file paths
exact errors
API names
security warnings
irreversible-action confirmations
verification evidence
known unknowns and blockers
```

## Thinking And Context Economy

Thinking tokens shrink when the agent gives itself less irrelevant material to process.

Before loading more context:

1. Classify the workflow level.
2. Search narrowly when the target is unknown.
3. Read the smallest authoritative file or snippet that can answer the next decision.
4. Load a skill only when its trigger matches the current task.
5. Load references only when the selected skill says they are in scope.
6. Stop reading when the next safe action is already determined.

Do not reduce thinking by skipping root-cause analysis, accessibility checks, security checks, TypeScript reasoning, architecture boundaries, or verification that the selected workflow requires.

## Output Economy

Default final reports are compact, fact-only, and evidence-first. Return only facts that affect the user's understanding, confidence, or next action.

For tasks that changed or validated something, use this default shape:

```text
Changed: files or surfaces
Verified: command/check and result
Blocked: missing tool/context, if any
```

Omit `Changed` when nothing changed and omit `Blocked` when nothing is blocked. Add one decision or next action only when the user must act. Verification must remain visible whenever it was run, failed, or was required but blocked.

For lookup-only answers, prefer:

```text
Finding
Evidence path or line
Answer
```

Avoid:

```text
"Sure", "of course", "happy to"
long process narration
same conclusion in multiple sections
decorative tables
full logs when a short excerpt is decisive
large before/after dumps unless requested
repeating or paraphrasing the user request
naming selected skills or internal workflow steps
empty headings and fields
```

Use tables only when comparison is the clearest compact form. Do not hide important caveats just to stay short.

## Default Word Budgets

- `Fast Lookup`: at most 120 words unless exact source material requires more.
- `Lightweight Workflow`: at most 180 words.
- `Standard Workflow`: at most 240 words for the final handoff.
- `Deep Workflow`: at most 320 words for the final handoff.

Named artifacts requested by the user, such as plans, specs, reviews, or contracts, may be longer. Their final handoff still follows the compact fact-only shape.

Word limits never authorize hiding a blocker, failed verification, approval requirement, security issue, destructive-action warning, or uncertainty. Remove boilerplate before compressing evidence.

## Compression Boundaries

Never compress or rewrite these unless the user explicitly asks for transformation and the target format permits it:

```text
code blocks
inline code
commands
file paths
URLs
schema names
environment variables
version numbers
public API names
error strings
license or legal text
```

When compressing memory or project notes, keep headings, frontmatter, links, code blocks, inline code, paths, commands, dates, numbers, and verified facts intact.

Do not compress source code, config, lockfiles, generated files, secrets, credentials, `.env` files, or production data.

## Tool And MCP Output Economy

If a host supports MCP or tool-description compression, it may compress safe prose fields such as tool descriptions, prompt descriptions, and resource descriptions.

It must not compress:

```text
tool names
argument names
JSON schemas
request payloads
tool-call results
data returned by application tools
errors that need exact matching
```

Compressing tool-call results is high risk because downstream parsing and evidence can break.

## Quality Gates

Token economy is valid only when:

- the selected workflow still has enough evidence to make the decision;
- verification required by the task still runs or is honestly reported as blocked;
- compressed output remains unambiguous;
- safety, security, accessibility, and irreversible-action warnings remain clear;
- another agent can resume from the final report or compact summary without re-reading irrelevant material.

If compactness conflicts with correctness, correctness wins.
