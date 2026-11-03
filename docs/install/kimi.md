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

## Project installation (recommended)

1. Download the [Kimi project package](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-kimi.tar.gz).
2. Extract it into the project root: skills belong under `.agents/skills`, with
   policy, references and scripts alongside them inside `.agents/`.
3. Preserve existing host instructions, `.agents/project/` and `.agents/learning/`
   state. Keep private state excluded from Git.
4. Preview and merge the native startup pointer:

   ```sh
   python .agents/skills/project-onboarding-adapter/scripts/configure_kimi.py --project .
   python .agents/skills/project-onboarding-adapter/scripts/configure_kimi.py --project . --approve
   ```

5. Start a fresh Kimi Code session and invoke `/skill:project-context-adapter`.
   Inspect the project and adapt facts using `.agents/adapters/kimi.md`.
   Verify startup policy, supporting files and one read-only role handoff.

Kimi discovers project skills, but does not automatically read the project's
`.agents/AGENTS.md`. The helper adds a managed pointer in `.kimi-code/AGENTS.md`,
preserving existing text and backing it up before changes. The pointer contains
absolute local paths; keep it local or regenerate after moving the project.
Preview removal with `--remove`, then add `--approve` to remove only its block.
Do not install this working `.agents` directory as a user-wide plugin.

## Alternative: user-wide plugin

Choose this mode instead of the project runtime installation. Extract a fresh
release archive into a clean staging directory outside all host projects:

```text
/plugins install /absolute/path/to/clean-staging/.agents
/plugins reload
/skill:webdev-agent-kit:project-context-adapter
```

Kimi copies the entire source directory into its managed plugin directory,
including unrelated files. Never install from a working project's `.agents`:
it can contain private facts, databases, attachments and local modifications.
Use only a clean release payload. Reinstall from a new clean payload for upgrades.
Project facts and memory belong under the current host's `.agents/project/` and
`.agents/learning/`, never the managed plugin copy.

When migrating from project mode, back up the installation and reconcile vendor
skills/roles with the release manifest using the upgrade workflow. Retire only
verified vendor runtime copies and the managed startup pointer; preserve custom
skills, instructions, project facts and learning state. Do not delete `.agents`.
Check discovery after migration: local roles can shadow plugin updates and local
skills can coexist with namespaced plugin skills.

Both modes include nine native `wdk-*` roles with bounded tools and no nested
subagents. Roles inherit Kimi's model configuration; a configured secondary-model
pool controls subagent selection. Names such as light/deep do not switch models.
Preserve user model/permission choices. K3 needs account availability; this package
does not provision credentials or models. Verify a real handoff before claiming
that delegation works.

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
Capture includes text prompt parts, successful tool output and failed tool errors.
Image/binary prompt parts are excluded. Kimi truncates successful tool output at
2000 characters; boundary-sized output is marked potentially truncated. Current
Stop events contain no final assistant text and are marked missing. Transcripts
and attachment bytes are not read automatically.

## Proposals and evaluation

After reviewing a project-memory run and its diagnosis:

```sh
python SKILL/scripts/learning_cycle.py propose --run RUN_ID --project . --repo . --engine kimi --kimi-model MODEL_ALIAS
python SKILL/scripts/learning_benchmark.py --repo . --proposal PROPOSAL --cases CASES --engine kimi --kimi-model MODEL_ALIAS
```

Use an already installed and authenticated Kimi Code v2. No model credentials
are created by the Kit. Select an alias shown by Kimi `/model`; if omitted,
`config.toml`'s `default_model` is used, which can differ from a TUI session's
selection. Both A/B arms pass the same alias explicitly and reject configuration
changes during evaluation. Recorded provenance is configured identity, not
provider-observed identity. The evaluator has no tools or subagents and sends only
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
