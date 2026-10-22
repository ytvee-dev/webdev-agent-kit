---
id: 'agents.skills.webdev-feedback.references.issue-publication'
title: 'Issue Publication'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'webdev-feedback'
tags:
    - 'agents/reference'
parent:
    - '[[skills/webdev-feedback/SKILL]]'
related: []
depends_on: []
---

# Issue Publication

## Report Fields

Use the destination's current issue template when readable. For Kit behavior
bugs inspect `.github/ISSUE_TEMPLATE/agent-behavior-bug.yml`; for improvements
inspect `.github/ISSUE_TEMPLATE/feature-request.yml`. API/CLI writes must include
the relevant fields in Markdown; do not assume web-form validation ran.
If templates are unavailable, use the following complete fallback.

Bug report:

- Title: concise observable failure; avoid asserting an unverified cause.
- Kit release/commit, client/version, model if exposed, OS/shell and relevant stack.
- Minimal sanitized user request, selected workflow/skill and tool availability.
- Expected behavior, actual behavior and chronological reproduction steps.
- Changed relative paths or "none"; omit sensitive project identifiers.
- Evidence kind: observed run, installation, configuration or synthetic replay.
- Exact checks and results; distinguish user-reported and directly observed facts.
- Hypotheses, unknowns, unrun checks, repeatability and affected versions.
- Public reproduction if available; otherwise say no public reproduction supplied.

Feature request:

- User problem, affected users/workflow and a concrete example.
- Observable desired outcome and acceptance criteria.
- Affected clients, compatibility, exclusions and alternatives.
- Evidence and unknowns; do not manufacture demand or repeated observations.
- Existing related issues or roadmap entries, if actually inspected.

Do not mark template checkboxes completed unless the corresponding search or
public-sharing check was performed. Keep uncertainty in the posted body.

## Transport

Prefer a sufficient connected GitHub tool. Use the user's existing authenticated
identity; a shared token is never part of this Kit. Do not infer issue permissions
from code push permissions. Use plain title/body unless separately authorized
metadata is supported; labels and assignees can need additional privileges.

For an existing GitHub CLI, use its documented noninteractive operations:

```text
gh issue list --repo OWNER/REPO --state all --search "SANITIZED TERMS" --limit 50 --json number,title,url,state
gh issue view NUMBER --repo OWNER/REPO --json title,body,url,state
gh issue create --repo OWNER/REPO --title "SAFE TITLE" --body-file BODY_PATH
```

Replace placeholders from verified facts. Use structured tool arguments or an
argument array; never interpolate chat text into shell code. Write the exact
sanitized body with real newlines to a local temporary file and pass its path.
Scope searches to the target repository, vary symptom terms when necessary and
inspect likely matches. A truncated or failed search is not proof of absence.

Before sending, verify that the repository exists, is the intended destination,
and accepts issues. Authentication or disabled-issues failures produce a draft
with `https://github.com/OWNER/REPO/issues`, not repeated login or install attempts.
Do not create a public gist or upload an attachment as a fallback.

## Recovery

A timeout after create may have succeeded. Inspect recent issues by the current
identity and compare destination/title/body before any retry. If the outcome
cannot be resolved, report submission-unconfirmed and retain the draft. Once an
issue exists, a readback failure is a verification limitation, not permission to
create another. Do not silently mutate an existing issue after a mismatch.

## Official Transport References

- https://cli.github.com/manual/gh_issue_create
- https://cli.github.com/manual/gh_issue_list
- https://docs.github.com/en/rest/issues/issues#create-an-issue

## Evidence And Encoding Review

Summarize chronology instead of pasting an entire dialogue. Distinguish
user-reported observations, quoted agent claims, independently inspected source
and proposed architecture. Do not call an agent's "tests passed" statement your
own verification. Identify expected opt-in behavior separately from defects.
Frame acceptance criteria as requested outcomes, not proof of an existing bug.

Use structured UTF-8 tool arguments or an explicitly UTF-8 body file. After
posting compare the returned/read-back body with the intended text, including
non-ASCII characters. Replacement characters or runs of question marks can
indicate destructive encoding loss: report the mismatch and use the same issue
for an authorized correction, never post a duplicate or guess the lost text.

## Explicit Learning Exclusion

When the user says not to save this task in learning memory, do not create or
update episodes, attach the issue URL, import the conversation or sync it. If
local capture is already active and accessible, the user's request authorizes
turning it off for the affected project through `learning.py off --project ROOT`;
verify `status` and explain that this project-wide pause also affects concurrent
sessions. Do not silently resume. If the user requests session-only suppression,
state that it is not currently implemented and resolve the narrower requirement
before promising it. Never edit client trust to suppress capture.

Hooks may have captured the initiating prompt before the agent saw the request,
and in-flight async capture may race the pause. Do not promise retroactive
absence. If state is inaccessible, say background capture is unverified. Cleanup
of existing records is a separate scoped deletion request; do not purge history
or claim all traces are gone. A pause is not a session-level exclusion guarantee.
