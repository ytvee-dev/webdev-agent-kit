---
id: 'agents.docs.install.first-run'
title: 'First Run And Installation Checks'
doc_type: 'guide'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags: []
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related: 
    - '[[docs/install/upgrade]]'
    - '[[docs/architecture/runtime-target-contracts]]'
depends_on: []
---

# First Run And Installation Checks

Use this checklist alongside your client's installation guide. It covers the
download, file layout and first session.

## Choose The Package

| Package | Base package | Where files go | How the client loads them |
| --- | --- | --- | --- |
| `opencode` (installer) | `codex` portable skills | host `.agents/` and `.opencode/plugins/` | `opencode.json` instructions + native plugin |
| `codex` | `codex` | host `.agents/` | host `AGENTS.md` pointer to `.agents/AGENTS.md` |
| `kimi` | `kimi` | Project archive | `.agents/skills` |
| `vs-code-codex` | `codex` | host `.agents/` | same Codex contract |
| `cursor` | `cursor` | host `.agents/` and `.cursor/` | `.cursor/rules/webdev-agent-kit.mdc` |
| `claude-code` | `claude-code` | external `webdev-agent-kit/` | native plugin and local marketplace |
| `vs-code-claude` | `claude-code` | external `webdev-agent-kit/` | same Claude plugin contract |

The VS Code packages reuse the corresponding Codex or Claude Code package. `claude` is a build alias;
there is no separate `webdev-agent-kit-claude.tar.gz` release asset.

## Before Extraction

1. Choose one release tag. Download its target archive and `SHA256SUMS` from
   that same release. Record the tag, archive filename, and checksum.
2. Verify the selected archive against its exact filename in `SHA256SUMS`.
   On Linux/macOS use `sha256sum <archive>` or `shasum -a 256 <archive>`;
   on PowerShell use `Get-FileHash <archive> -Algorithm SHA256`. Compare the
   complete digest, ignoring letter case. A mismatch stops installation.
3. List entries with `tar -tzf <archive>` and extract first into an empty
   staging directory. Do not extract inside an existing `.agents/` directory.
4. Check the roots in the table. A source-code ZIP or cloned repository is
   authoring source, not a client release package.
5. If a kit, native rule, or plugin already exists, follow
   [upgrade and rollback](upgrade.md). Preserve host instructions and local
   project records before replacing anything. A `.gitignore` rule does not untrack
   a file already committed; do not remove tracked team instructions.

## Adapt The Host

For Codex or Cursor, start at the host project root:

```text
Adapt this kit to the existing project. Preserve existing instructions and show
any proposed merge. Save project facts in .agents/project/: the stack, useful
paths, available tools and what each check command covers. Do not change app
code or install tools. Do not change model configuration.
```

For Claude, complete the native plugin installation in the client guide first.
Invoke the plugin's onboarding skill from the host project. Keep local project
facts under host `.agents/project/`, outside the installed plugin. Native skill
discovery does not require copying plugin skills into `.agents/skills/`.
Create a shared-policy pointer only if that shared policy is actually installed
and its use is approved; never create a pointer to a missing `.agents/AGENTS.md`.

## What Counts As Ready

- Installed: the package roots, version, and native manifests are correct.
- Discovered: the client lists or loads the expected skill.
- Adapted: instruction links work, old instructions are preserved, and saved
  project facts match the source files.
- Exercised: a small task has an observed result and retained evidence.

Check discovery in a fresh session, then ask a read-only question such as
вЂњWhich existing command checks types, and what source proves that?вЂќ.
Installation and discovery alone do not establish agent quality or cross-client
compatibility. Do not run an app merely to claim onboarding success.

## Diagnose A Failed Step

| Symptom | Next check |
| --- | --- |
| `.agents/.agents/` | Return to staging and extract from the host root |
| Missing skill | Confirm selected target, discovery root, and fresh-session client result |
| Old version after update | Check active plugin location or project bundle, not only downloaded filename |
| Browser listed but no screenshot | Confirm current callable tool; report the rendered check as unverified |
| Windows `npm.ps1` blocked | One equivalent `npm.cmd` fallback; preserve execution policy |
| Sandbox blocks startup | Follow approved fallback budget; retain blocked verification if unavailable |

Use the [compatibility report form](https://github.com/ytvee-dev/webdev-agent-kit/issues/new?template=compatibility-report.yml)
with the exact failing step, client version, OS, shell, archive, and evidence.

## Codex Model Routing

Full Codex adaptation includes missing local subagent setup. The facts-only
prompt above skips that step. Existing working model settings are preserved.

If a role is configured but does not run, follow the
[model-routing guide](gpt-model-routing.md). The report should distinguish a role
file on disk, a role listed by the client and a successful invocation. Project
trust and sandbox permissions remain under your control.
