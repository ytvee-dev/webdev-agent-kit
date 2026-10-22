## Problem

<!-- Describe the user-facing problem, observed agent failure, or documentation gap. -->

## Scope

<!-- List the affected files and parts of the Kit. Explain important exclusions. -->

## Changes

<!-- Summarize the changes and their effect on users. -->

## Skill Selection

<!-- For rule or skill changes, show when the workflow should and should not apply. Use N/A when routing is unaffected. -->

Requests that should use this workflow:

```text

```

Similar requests that should not use it:

```text

```

## Verification

<!-- List exact commands and results. Distinguish passed, failed, blocked, and skipped checks. -->

## Risks

<!-- Cover portability, security, approval, generated-target, and compatibility risks. -->

## Checklist

- [ ] The change is limited to the accepted scope and preserves unrelated work.
- [ ] Public technical claims are supported by source, configuration, CI, or a real check.
- [ ] Required graph links, manifests, schemas, and generated contracts are aligned.
- [ ] No dependency, tool, supported stack, or test infrastructure was added without approval.
- [ ] Relevant validation commands and results are listed above.
- [ ] `CHANGELOG.md` was updated for behavior, packaging, validation, security, or public documentation changes, or the omission is explained.
- [ ] No secrets, private project facts, customer data, or generated `dist/**` edits are included.
