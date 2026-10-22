---
id: 'agents.support'
title: 'WebDev Agent Kit Support'
doc_type: 'support-guide'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'maintenance/support'
parent: []
related:
    - '[[README|WebDev Agent Kit]]'
    - '[[MAINTENANCE|Maintainer Change Process]]'
    - '[[SECURITY|WebDev Agent Kit Security Policy]]'
depends_on: []
---

# Support

Development and releases are managed by the project owner. GitHub Issues track
usage problems and approved work; no response-time or resolution-time guarantee
is offered.

## Choose The Right Channel

- **Agent behavior bug:** use the
  [Agent Behavior Bug form](https://github.com/ytvee-dev/webdev-agent-kit/issues/new?template=agent-behavior-bug.yml)
  when an agent ignores scope, selects the wrong workflow, changes unrelated
  files, reports verification incorrectly, or violates another kit rule.
- **Client compatibility:** use the
  [Compatibility Report form](https://github.com/ytvee-dev/webdev-agent-kit/issues/new?template=compatibility-report.yml)
  for installation, missing skills, archive layout, permissions, or client-specific
  behavior in Codex, Claude Code, Cursor, or their VS Code variants.
- **Feature or workflow idea:** use the
  [Feature Request form](https://github.com/ytvee-dev/webdev-agent-kit/issues/new?template=feature-request.yml).
- **New skill, profile, adapter, or core change:** use the
  [Skill Proposal form](https://github.com/ytvee-dev/webdev-agent-kit/issues/new?template=skill-proposal.yml)
  and follow `MAINTENANCE.md` before implementation.
- **Usage question:** use the
  [Support Question form](https://github.com/ytvee-dev/webdev-agent-kit/issues/new?template=support-question.yml).
- **Security vulnerability:** do not open an issue. Follow
  [SECURITY.md](SECURITY.md).

## Before Opening An Issue

1. Search existing issues and release notes.
2. Confirm the installed version and actual client target.
3. Verify the archive against `SHA256SUMS` when installation is involved.
4. Reduce the problem to the smallest public reproduction possible.
5. Remove credentials, customer data, private paths, and proprietary source.
6. Record exact commands and distinguish failed, blocked, and skipped checks.

If you cannot reproduce the problem, include what you observed and what remains
unknown. The maintainer may ask for more detail or direct you to the relevant
project. Submitting a report does not guarantee a fix.

## Supported Scope

The current stack-specific profile targets React, Next.js, TypeScript, CSS
Modules, Redux, TanStack, and Axios when those technologies are verified in the
host project. Framework-agnostic planning, design intake, review, visual QA,
tooling, and project-context workflows may apply outside that stack.

Other stacks are unsupported unless an applicable profile or workflow is
accepted and documented by the owner.
