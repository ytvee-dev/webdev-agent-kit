---
id: 'agents.docs.install.kimi'
title: 'Install WebDev Agent Kit for Kimi Code'
doc_type: 'user-guide'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags:
    - 'docs/install'
    - 'client/kimi'
parent:
    - '[[docs/install/README|Installation Guides]]'
related:
    - '[[docs/install/gpt-model-routing]]'
    - '[[docs/install/first-run|First Run And Installation Checks]]'
    - '[[docs/install/upgrade|Upgrade And Rollback]]'
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
    - '[[common/mcp-installation-policy|MCP Installation Policy]]'
    - '[[docs/mcp/README|MCP for WebDev Agent Kit]]'
depends_on: []
---

# Install WebDev Agent Kit for Kimi Code

Complete the [first-run checks](first-run.md). Preserve existing installations
using [upgrade and rollback](upgrade.md).

1. Download the [Kimi project package](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-kimi.tar.gz).
2. Extract it into the project root: skills belong under `.agents/skills`, with
   policy, references and scripts alongside them inside `.agents/`.
3. Preserve existing host instructions and `.agents/project/` and
   `.agents/learning/` state. Keep private state excluded from Git.
4. Start a fresh Kimi Code session in that project and invoke
   `/skill:project-context-adapter`. Ask it to inspect the project and adapt
   project facts, using `.agents/adapters/kimi.md`. Verify that the skill loads
   its policy and supporting files. Do not overwrite an existing AGENTS.md.
5. Keep the selected model and permissions. K3 requires availability in the
   user's Kimi account; this package does not provision credentials or models.

## Activate at session start

The archive supports project-local discovery directly. To also load WebDev
instructions at session start through the native plugin system:

```text
/plugins install /absolute/path/to/project/.agents
/plugins reload
/skill:webdev-agent-kit:project-context-adapter
```

Kimi copies the plugin into its managed directory. Installation is user-wide;
reinstall after updating the archive. Use one installation mode to avoid
unintentional duplicate skills. Existing host AGENTS.md is never overwritten.
Project facts and memory stay under the current project's `.agents` directory.
The package includes nine native `wdk-*` roles with bounded tool access. Verify
one real lookup/review handoff before treating delegation as operational.

## Optional experience capture

From the project root, replace `SKILL` below with the absolute installed path to
`skills/agent-self-improvement` (the managed plugin copy when using plugin mode).
Python 3.11 or newer is required for the TOML installer.

```sh
python SKILL/scripts/install_kimi_hooks.py --project .
python SKILL/scripts/install_kimi_hooks.py --project . --approve
python SKILL/scripts/learning.py on --project .
```

Installation preserves existing configuration, writes a backup on changes and
filters the global hooks to this exact project. Use `--config PATH` for an
explicit Kimi config. Restart the Kimi session after hook changes. To disable
recording run `learning.py off --project .`; to remove these project's hooks
run `install_kimi_hooks.py --project . --remove --approve`.
Use TOML array-of-table declarations for hooks for existing nonempty hook arrays; inline arrays must
be converted manually. On Windows use paths without shell metacharacters
(`&`, `%`, `!`, parentheses and similar characters). Ordinary spaces are supported.
Only exposed prompt/tool payloads are collected. Current Kimi Stop events do
not contain the final assistant response; this remains marked missing. Missing assistant
text is marked; transcripts and attachment bytes are not read automatically.

## Proposals and evaluation

After reviewing a project-memory run and its diagnosis:

```sh
python SKILL/scripts/learning_cycle.py propose --run RUN_ID --project . --repo . --engine kimi
python SKILL/scripts/learning_benchmark.py --repo . --proposal PROPOSAL --cases CASES --engine kimi
```

Use an already installed and authenticated Kimi Code v2. No model credentials
are created by the Kit. The evaluator has no tools or subagents and sends only
the supplied text to the selected provider. Visual attachments remain metadata.
Review the proposal, run independent held-out cases and explicitly approve
application through the existing learning workflow. Text assertions do not
replace real coding behavior checks.

## Acceptance before publication

Verify on an authenticated installation: skill and policy discovery, one
read-only subagent, capture on/off and project isolation, a reviewed proposal,
and baseline/candidate evaluation on the same model. Repeat the installer on
Windows with paths containing spaces. Structural checks and synthetic payloads
must never be described as a live Kimi pass.

[Official skill documentation](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html)

[All installation guides](README.md)
