---
id: 'agents.support'
title: 'WebDev Agent Kit Support'
doc_type: 'support-guide'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'community/support'
parent: []
related:
    - '[[README|WebDev Agent Kit]]'
    - '[[CONTRIBUTING|Contributing To WebDev Agent Kit]]'
    - '[[SECURITY|WebDev Agent Kit Security Policy]]'
depends_on: []
---

# Support

WebDev Agent Kit is maintained as an open-source project. Support is provided on
a best-effort basis through GitHub Issues; no response-time or resolution-time
guarantee is offered.

## Choose The Right Channel

- **Agent behavior bug:** use the
  [Agent Behavior Bug form](https://github.com/ytvee-dev/webdev-agent-kit/issues/new?template=agent-behavior-bug.yml)
  when an agent ignores scope, selects the wrong workflow, changes unrelated
  files, reports verification incorrectly, or violates another kit rule.
- **Client compatibility:** use the
  [Compatibility Report form](https://github.com/ytvee-dev/webdev-agent-kit/issues/new?template=compatibility-report.yml)
  for installation, archive layout, discovery, sandbox, or target-specific
  behavior in Codex, Claude Code, Cursor, or their VS Code variants.
- **Feature or workflow idea:** use the
  [Feature Request form](https://github.com/ytvee-dev/webdev-agent-kit/issues/new?template=feature-request.yml).
- **New skill, profile, adapter, or core change:** use the
  [Skill Proposal form](https://github.com/ytvee-dev/webdev-agent-kit/issues/new?template=skill-proposal.yml)
  and follow `GOVERNANCE.md` before implementation.
- **Usage question:** use the
  [Support Question form](https://github.com/ytvee-dev/webdev-agent-kit/issues/new?template=support-question.yml).
- **Security vulnerability:** do not open an issue. Follow
  [SECURITY.md](SECURITY.md).
- **Conduct concern:** do not open an issue with sensitive details. Follow
  [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Before Opening An Issue

1. Search existing issues and release notes.
2. Confirm the installed version and actual client target.
3. Verify the archive against `SHA256SUMS` when installation is involved.
4. Reduce the problem to the smallest public reproduction possible.
5. Remove credentials, customer data, private paths, and proprietary source.
6. Record exact commands and distinguish failed, blocked, and skipped checks.

The maintainer may close requests that lack enough public evidence to reproduce,
fall outside the supported scope, or belong in a different channel. A clear
reproduction improves the chance of a useful response but does not guarantee a
fix or inclusion in the roadmap.

## Supported Scope

The current stack-specific profile targets React, Next.js, TypeScript, CSS
Modules, Redux, TanStack, and Axios when those technologies are verified in the
host project. Framework-agnostic planning, design intake, review, visual QA,
tooling, and project-context workflows may apply outside that stack.

Requests for other stacks are welcome as proposals, but support is not implied
until a profile or workflow is accepted and documented.
