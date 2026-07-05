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
depends_on: []
---

# Security Policy

WebDev Agent Kit contains executable instructions for AI coding agents. Treat every rule, skill, script, reference, and generated distribution target as supply-chain-sensitive content.

## Scope

This policy covers:

- runtime instructions in `AGENTS.md`;
- reusable policies in `common/**`;
- skill packages in `skills/**`;
- helper scripts in `scripts/**` and `skills/**/scripts/**`;
- generated Codex and Claude targets in `dist/**`;
- installation, contribution, and release documentation.

Local-only host project overlays under `project/**` are out of scope for the reusable upstream bundle and must not be published.

`README.md` is human-facing only. It must not be used by agents as a policy, routing, inventory, or validation source.

## Security Rules For Contributors

- Do not add hidden instructions, prompt-injection payloads, credential requests, production access steps, or remote execution flows.
- Do not add install commands, package-manager changes, MCP installation steps, or tool configuration changes without explicit approval gates in the relevant rule or skill.
- Prefer pinned and reproducible helper commands in documentation. Avoid ad-hoc curl-pipe-shell patterns.
- Keep scripts small, auditable, deterministic, and limited to bundle validation, packaging, or skill authoring.
- Do not include secrets, tokens, private repository paths, production hostnames, customer data, or copied host-project facts.
- Keep Figma, Browser, Playwright, MCP, and web-access boundaries explicit. Tool availability is not permission to use a tool.

## Review Requirements

Security-sensitive changes need explicit review when they:

- add or modify scripts;
- change generated distribution behavior;
- add tools, MCP dependencies, browser automation, network access, package installation, or command execution instructions;
- loosen approval gates;
- change `allowed-tools`, `policy`, or tool dependency metadata;
- alter source validation, graph validation, or packaging exclusions.

## Reporting A Vulnerability

Open a private security advisory or contact the repository maintainers through the GitHub security channel when available. Do not publish exploit details in a public issue before maintainers have had time to respond.

Include:

- affected file or skill;
- the exact instruction, script, or metadata that creates risk;
- a realistic exploitation scenario;
- expected safe behavior;
- suggested fix when possible.

## Release Safety Checklist

Before tagging or distributing a release:

1. Run `python scripts/validate_skill_pack.py`.
2. Inspect generated `dist/codex` and `dist/claude` targets.
3. Confirm `project/**`, `dist/**` source artifacts, secrets, local notes, and private host-project facts are excluded.
4. Confirm Codex-only files are not shipped to the Claude target.
5. Confirm public docs explain installation, validation, contribution, and security expectations.
6. Record behavior, validation, and security-relevant changes in `CHANGELOG.md`.
