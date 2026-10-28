---
id: 'agents.skills.agent-self-improvement.references.collection-contract'
title: 'Experience Collection Contract'
doc_type: 'skill-reference'
layer: 'skill'
status: 'draft'
publishable: true
local_only: false
skill: 'agent-self-improvement'
tags:
    - 'agents/learning'
parent:
    - '[[skills/agent-self-improvement/SKILL|Agent Self Improvement]]'
related: []
depends_on: []
---

# Collection Contract

A canonical event is a JSON object with `client`, `session_id`, `message_id`, optional `part_id`, `kind` (`user`, `assistant`, `tool`, `user_correction`, `system_event`), optional `content`, `source_url`, `skills` and `attachments`. `skills` may be empty; an unobserved skill invocation must not be reported as observed. A client hook may provide only metadata; no guessed image contents are permitted. Stable deduplication key: client + project + session + message + part + kind. The source URI is nullable.

The `capture` command reads a bounded canonical JSON event from stdin. A user's project opt-in must exist before capture. `import` reads a newline-delimited sequence of canonical events and rejects malformed lines. Imports are idempotent. Text content is conservatively redacted for obvious credentials and size-bounded; no redactor guarantees removal of every sensitive datum. Do not capture private/customer projects without authorization.

Images, PDFs and other artifacts are stored as SHA-256-addressed bytes via explicit `attach` or through supported opt-in embedded `data:` file parts in the OpenCode plugin. No arbitrary URL or local path is read automatically. A path mentioned inside an untrusted message is never opened by a hook. The session's attachment references remain metadata-only unless an authorized file is actually imported. File limits apply; a failed copy is not a success.

Integration templates are available under `assets/integrations/` and are **not installed by extracting this skill**. OpenCode's sample uses a session-idle SDK snapshot; Codex/Claude sample hooks only capture exposed data, without asserting complete transcripts or byte-level attachment parity. ChatGPT web and mobile require authorized manual export/import and cannot be continuously scraped by this skill.

Retain the original local source IDs; never create fake chat URLs. Resolve state consistently: explicit `--state`, then `AGENT_LEARNING_STATE`, otherwise
`.agents/learning` under the selected project. Keep state ignored by Git and
protected during Kit updates, including explicitly configured external stores.

Session pause is keyed by project, client and session and blocks both event and
attachment ingestion. It never enables collection or erases existing data. The
Codex/Claude bridge marks tool output beyond its 3000-character excerpt as
truncated and marks missing assistant text explicitly. These remain partial
observations. Use the memory contract for quality audit and raw-only retention.

## Delivery Integrity

Capture stores source time separately from receipt time when the client provides
it. Stable client event IDs deduplicate retries; events without IDs receive fresh
synthetic IDs and explicitly lack retry deduplication. Identical text is not proof
of a duplicate. Truncation and missing content remain visible in context pages.

Hooks bound input and execution time and never block primary work on capture
failure. Content-free local health reports last receipt, duplicate/skip/error
counts and reasons. Missing diagnostics means unverified, never healthy. Hooks
must not store exception text, credentials or message contents in health records.
Capture does not invoke analysis, snapshots, remote exchange or Langfuse setup.
