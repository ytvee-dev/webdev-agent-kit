## Problem Or Failure Mode

<!-- Describe the user-facing problem, observed agent failure, or documentation gap. -->

## Scope And Layer

<!-- List the affected files and owning layers. Explain important exclusions. -->

## Changes

<!-- Summarize the smallest coherent change made. -->

## Routing Evidence

<!-- For rule or skill changes, include should-trigger and near-miss examples. Use N/A when routing is unaffected. -->

Should trigger:

```text

```

Should not trigger:

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
