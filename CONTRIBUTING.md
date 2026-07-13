---
id: 'agents.contributing'
title: 'Contributing To WebDev Agent Kit'
doc_type: 'contribution-guide'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/contributing'
    - 'governance'
parent: []
related:
    - '[[AGENTS|Canonical Agent Policy]]'
    - '[[CHANGELOG|WebDev Agent Kit Changelog]]'
    - '[[CODE_OF_CONDUCT|Code Of Conduct]]'
    - '[[GOVERNANCE|Project Governance]]'
    - '[[SECURITY|WebDev Agent Kit Security Policy]]'
    - '[[SUPPORT|Project Support]]'
depends_on: []
---

# Contributing

Thank you for helping improve WebDev Agent Kit. The project is a reusable source
bundle for coding-agent workflows, so all changes must remain portable,
progressively disclosed, auditable, and safe to install into a host project.

Read the [Code of Conduct](CODE_OF_CONDUCT.md) before participating. To choose
the right channel, see [Support](SUPPORT.md).

## Ways To Contribute

Useful contributions include:

- reporting reproducible agent behavior that violates an expected rule;
- testing an archive in Codex, Claude Code, Cursor, or VS Code environments;
- adding a trigger, negative-trigger, output, or compatibility eval fixture;
- improving installation guidance, examples, links, or translations;
- proposing a documented frontend pattern or anti-pattern;
- improving client compatibility without weakening the portable core;
- proposing a new profile or skill after demonstrating a distinct recurring
  workflow.

Reproducible failure cases are as valuable as code changes. They let maintainers
turn observed behavior into a focused rule and deterministic regression check.

## Report An Agent Behavior Problem

Use the Agent Behavior Bug issue form and include:

```text
Agent/client:
Project stack:
WebDev Agent Kit version:
User request or minimal prompt:
Expected behavior:
Actual behavior:
Selected workflow or skill, if known:
Available and unavailable tools and MCP servers:
Files changed:
Verification performed:
```

Remove secrets, private repository content, customer data, and personal
information before submitting evidence. Then create an Issue or Pull Request
with a detailed description in the current repository. The title must include a
severity-level marker.

## Contribution Risk Levels

Review depth depends on the affected layer.

### Level 1 — Documentation And Examples

- human-facing documentation;
- translations;
- examples and link fixes;
- installation guide corrections;
- eval fixtures that do not change runtime behavior.

These are the best starting points for first-time contributors.

### Level 2 — Patterns And Evals

- approved patterns and anti-patterns;
- trigger and negative-trigger cases;
- output expectations;
- deterministic fixtures and schema-aligned metadata.

Explain the observed failure mode and why the proposed rule belongs in the
selected layer.

### Level 3 — Skills, Profiles And Adapters

- changes to an existing skill;
- new skills or stack profiles;
- client adapter behavior;
- capability declarations and Codex metadata.

These changes require evidence that the workflow is distinct, portable, and not
already covered by an existing skill.

### Level 4 — Runtime Core And Supply Chain

- runtime core and policy precedence;
- scripts, schemas, packaging, and release workflows;
- approval, security, tool, or sandbox boundaries;
- generated target construction.

These changes require explicit maintainer review, complete validation, and a
clear compatibility and security analysis.

## Contribution Principles

- Keep reusable policy in `common/**` and task-specific procedures in
  `skills/**`.
- Keep host-project facts in local-only `project/**` overlays. Never publish
  current project state in the reusable bundle.
- Prefer precise workflow instructions over broad slogans such as "follow best
  practices".
- Treat skill `description` fields as routing triggers. State what the skill
  does, when it applies, and important non-use boundaries.
- Keep `SKILL.md` compact. Put durable detail in `references/**`, deterministic
  helpers in `scripts/**`, and templates or fixtures in `assets/**` only when
  they reduce repeated context.
- Keep `README.md` human-maintained. It is not runtime policy, routing input, or
  validation authority.
- Do not add dependencies, supported stacks, MCP tools, generated scaffolds, or
  test infrastructure without explicit approval and the required policy and
  validation updates.
- Do not patch generated `dist/**` output directly. Update source files and use
  the existing builders.

## Pull Request Workflow

1. Search existing Issues and pull requests for the same failure mode.
2. Open or reference the appropriate issue when the change affects runtime
   behavior, compatibility, security, packaging, or public direction.
3. Make the smallest coherent source change. Preserve unrelated work and public
   contracts outside the proposal.
4. Add or update only the existing validation fixtures required by the changed
   behavior. New test infrastructure requires explicit maintainer approval.
5. Run the checks for the affected layer and record exact commands and results.
6. Add a `CHANGELOG.md` entry for behavior, packaging, validation, security, or
   public documentation changes.
7. Open a pull request using the repository template.

## Required Checks

For the full structural validation, run:

```bash
python scripts/validate_skill_pack.py
```

For a changed skill, also run:

```bash
python skills/agent-rules-skill-author/scripts/validate_agent_skill.py skills/<skill-name>
```

Documentation changes should run the relevant checks:

```bash
python scripts/validate_schemas.py --strict-graph
python scripts/check_links.py
python scripts/check_readme_boundary.py
python scripts/validate_install_guides.py
```

Use the existing Markdown, YAML, and Python lint commands from
`.github/workflows/quality-ci.yml`. If a check cannot run, state the blocker and
the exact command attempted; do not report it as passed.

## Pull Request Evidence

A pull request that changes rules, skills, or distribution behavior must include:

- the user-facing problem or agent failure mode;
- the changed files and owning layers;
- should-trigger examples;
- near-miss examples that must not trigger the workflow;
- validation commands and results;
- portability, security, and host-agent compatibility risks;
- the related issue or proposal when required;
- a changelog entry when behavior or public contracts changed.

## Adding Or Changing A Skill

Every skill package must keep these files aligned:

```text
skills/<skill-name>/
├── SKILL.md
└── agents/openai.yaml
```

Use `references/**`, `scripts/**`, and `assets/**` only when they make execution
more deterministic or reduce repeated context. A skill is ready for review only
when:

- `name` matches the directory name;
- `description` has a narrow routing boundary;
- required workflow sections are present;
- referenced paths exist;
- `agents/openai.yaml` matches the skill intent;
- trigger and negative-trigger examples are documented;
- capability requirements are declared in the correct metadata layer;
- manifests and graph links are updated when inventory changes;
- validation passes.

A new skill must represent a separate, recurring user workflow that cannot be
safely covered by an existing skill. It must not be added only to increase the
number of integrations or features.

## Review Severity

- `blocking`: breaks validation, packaging, routing, safety, or installation;
- `high`: creates likely false routing, broad context loading, undocumented
  behavior change, or portability drift;
- `medium`: harms maintainability, discoverability, or future extension;
- `low`: improves wording, formatting, or local clarity without changing
  behavior.

Project decision-making and maintainer responsibilities are described in
[Governance](GOVERNANCE.md).
