---
id: 'agents.security'
title: 'WebDev Agent Kit Security Policy'
doc_type: 'security-policy'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/security'
    - 'supply-chain'
parent: []
related:
    - '[[AGENTS|Canonical Agent Policy]]'
    - '[[CONTRIBUTING|Contributing To WebDev Agent Kit]]'
    - '[[GOVERNANCE|Project Governance]]'
depends_on: []
---

# Security Policy

WebDev Agent Kit contains executable instructions for AI coding agents. Treat
every rule, skill, script, reference, metadata file, and generated distribution
target as supply-chain-sensitive content.

## Supported Versions

Security fixes are developed for the latest published release line.

| Version | Supported |
| --- | --- |
| `0.4.x` | Yes |
| `< 0.4` | No |

Users of an older release should upgrade to the latest release before reporting
an issue that has already been fixed. A coordinated fix may include a new patch
release when the latest published package is affected.

## Scope

This policy covers:

- runtime instructions in `AGENTS.md`;
- reusable policies in `common/**`;
- skill packages in `skills/**`;
- helper scripts in `scripts/**` and `skills/**/scripts/**`;
- schemas, eval fixtures, capability metadata, and client adapters;
- generated Codex, Claude Code, and Cursor targets;
- installation, packaging, contribution, and release workflows.

Local-only host project overlays under `project/**` are outside the reusable
upstream bundle and must not be published.

`README.md` is human-facing only. It is not agent policy, routing input,
inventory authority, or validation evidence.

## Report A Vulnerability Privately

Do not open a public issue for an undisclosed vulnerability.

Use the repository's
[private security advisory form](https://github.com/ytvee-dev/webdev-agent-kit/security/advisories/new)
when it is available. If private reporting is unavailable, contact the
maintainer through the private contact options published on the
[@ytvee-dev GitHub profile](https://github.com/ytvee-dev) and include the
repository name in the subject.

Include:

- affected release, archive, file, or skill;
- the exact instruction, script, metadata, or packaging behavior that creates
  the risk;
- a realistic exploitation scenario and prerequisites;
- expected safe behavior;
- a minimal reproduction or suggested fix when possible;
- whether the report may be credited after disclosure.

Do not include active credentials, customer data, private source code, or an
unnecessary working exploit.

## Coordinated Disclosure

The maintainer will acknowledge a report through the selected private channel,
assess impact, and coordinate remediation and disclosure with the reporter.
Timelines depend on severity, reproducibility, affected release targets, and the
need to rotate or rebuild artifacts.

Keep exploit details private until a fix or mitigation is available and the
maintainer has agreed on disclosure. After remediation, the project may publish
a GitHub Security Advisory, release notes, affected versions, mitigation steps,
and reporter credit when consented.

## Security Rules For Contributors

- Do not add hidden instructions, prompt-injection payloads, credential requests,
  production access steps, or unreviewed remote execution flows.
- Do not add install commands, package-manager changes, MCP installation, or tool
  configuration without explicit approval gates in the owning rule or skill.
- Prefer pinned and reproducible helper commands. Do not use curl-pipe-shell
  installation patterns.
- Keep scripts small, auditable, deterministic, and limited to approved bundle
  validation, packaging, release, or skill-authoring responsibilities.
- Do not include secrets, tokens, private repository paths, production
  hostnames, customer data, or copied host-project facts.
- Keep browser, MCP, network, filesystem, and command-execution boundaries
  explicit. Tool availability is never permission to use a tool.

## Review Requirements

Security-sensitive changes need explicit maintainer review when they:

- add or modify scripts;
- change generated distribution or release behavior;
- add tools, MCP dependencies, browser automation, network access, package
  installation, or command execution;
- loosen approval gates;
- change `allowed-tools`, policy, or capability metadata;
- alter source validation, graph validation, or packaging exclusions.

## Release Safety Checklist

Before tagging or distributing a release:

1. Run `python scripts/validate_skill_pack.py`.
2. Inspect every generated canonical target and compatibility alias.
3. Confirm local overlays, secrets, private notes, dependencies, and build caches
   are excluded.
4. Confirm client-specific files do not leak into another client's target.
5. Confirm public documentation describes installation, validation,
   contribution, and security boundaries accurately.
6. Record behavior, validation, and security changes in `CHANGELOG.md`.
7. Verify release archives and `SHA256SUMS` through the existing archive
   validator.
