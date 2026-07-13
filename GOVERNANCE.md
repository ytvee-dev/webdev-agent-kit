---
id: 'agents.governance'
title: 'WebDev Agent Kit Governance'
doc_type: 'governance-policy'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'community/governance'
    - 'governance'
parent: []
related:
    - '[[CONTRIBUTING|Contributing To WebDev Agent Kit]]'
    - '[[CODE_OF_CONDUCT|Code Of Conduct]]'
    - '[[ROADMAP|Project Roadmap]]'
depends_on: []
---

# Governance

WebDev Agent Kit currently uses a single-maintainer governance model. The
maintainer is [@ytvee-dev](https://github.com/ytvee-dev).

## Responsibilities

The maintainer is responsible for:

- setting project direction and maintaining the public roadmap;
- reviewing and merging contributions;
- protecting runtime, security, portability, and release boundaries;
- maintaining release artifacts and supported-version information;
- moderating community spaces under the Code of Conduct;
- making final decisions when consensus cannot be reached.

Contributors are responsible for providing reproducible evidence, keeping
changes within an agreed scope, running applicable checks, and disclosing risks
or conflicts of interest.

## Decision Process

Routine documentation, examples, and narrowly scoped fixes are proposed through
pull requests. They require green applicable CI and maintainer approval.

Changes to runtime core, policy precedence, approval boundaries, security,
scripts, schemas, packaging, release workflows, supported stacks, new profiles,
new adapters, or new skills require a proposal before implementation. Use the
Skill Proposal issue form and describe:

- the recurring user problem or observed agent failure mode;
- why an existing workflow cannot safely cover it;
- affected clients, layers, capabilities, and public contracts;
- trigger and non-trigger examples;
- validation, compatibility, migration, and security impact;
- alternatives considered.

The maintainer may accept, request changes, defer, or reject a proposal. Silence
does not indicate acceptance. Implementation should begin only after scope and
acceptance criteria are recorded in the issue.

## Review Requirements

All changes must preserve unrelated work and use the smallest coherent source
edit. Review depth follows the four risk levels in `CONTRIBUTING.md`.

Core and supply-chain changes additionally require:

- a documented failure mode or requirement;
- deterministic validation or eval coverage where the behavior is testable;
- analysis of client portability and generated targets;
- review of approval, network, filesystem, and command-execution boundaries;
- a changelog entry and release impact assessment.

## Stability Lifecycle

New skills, profiles, adapters, and major workflows start as **experimental**
unless the proposal explicitly proves an existing stable contract.

An experimental feature may become **stable** when:

- its scope, triggers, non-triggers, and failure behavior are documented;
- source and generated-target validation pass;
- at least two independent project or client reports confirm the intended
  workflow where portability is relevant;
- known security and compatibility risks are documented;
- the maintainer records the decision in the changelog.

A feature may be **deprecated** when it is unsafe, redundant, incompatible with
current clients, or no longer maintainable. Deprecation should be announced in
the changelog and migration guidance should be provided when a safe replacement
exists. Before version 1.0, breaking changes may occur in a minor release, but
they must be explicit in release notes.

## Maintainer Changes

Additional maintainers may be invited after sustained, high-quality
contributions and demonstrated judgment across runtime safety, portability,
review, and community conduct. The current maintainer decides invitations and
records changes publicly in this document.

If the current maintainer can no longer maintain the project, they may appoint a
successor or archive the repository with its final support status documented.

## Conflicts And Appeals

Technical disagreements should be resolved with repository evidence,
reproducible examples, and documented tradeoffs. The maintainer makes the final
project decision after considering that evidence.

Conduct enforcement appeals may be submitted privately through the reporting
channel in `CODE_OF_CONDUCT.md`. If no independent maintainer exists, the final
decision remains with the repository owner; this limitation will be revisited
when the maintainer team grows.
