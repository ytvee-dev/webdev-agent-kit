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

Retain the original local source IDs; never create fake chat URLs. The state root lives outside the Kit and outside host Git repositories by default.
