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
