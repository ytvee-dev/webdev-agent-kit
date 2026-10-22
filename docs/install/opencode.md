---
id: 'agents.docs.install.opencode'
title: 'Install WebDev Agent Kit for OpenCode'
doc_type: 'user-guide'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags:
    - 'docs/install'
    - 'client/opencode'
parent:
    - '[[docs/install/README|Installation Guides]]'
related:
    - '[[docs/install/first-run]]'
    - '[[docs/install/upgrade]]'
depends_on: []
---

# Install WebDev Agent Kit in OpenCode

This is a project-scoped integration for OpenCode Desktop and CLI on Windows. The release includes all 23 portable skills and the Experience Recorder plugin.

## One-command Windows installation

The example below pins v1.5.0, the first OpenCode installer release. For a newer
published release, replace both version strings with that release's tag. Use the
script and bundle from the same release:

```powershell
$project = "C:\Projects\my-app"
$installer = "$env:TEMP\install-opencode-v1.5.0.ps1"
Invoke-WebRequest "https://github.com/ytvee-dev/webdev-agent-kit/releases/download/v1.5.0/install-opencode.ps1" -OutFile $installer
& $installer -Project $project
```

The installer downloads the pinned Codex project bundle (portable `.agents/skills` layout), verifies it against the release `SHA256SUMS`, merges `.agents/AGENTS.md` into `opencode.json` instructions, and installs the OpenCode recorder at `.opencode/plugins/experience-recorder.js`. It preserves unrelated settings, backs up an existing `opencode.json`, and refuses to overwrite an existing vendor Kit or an existing recorder.

**Capture is disabled by default.** To enable it after reviewing project privacy:

```powershell
$learn = Join-Path $project ".agents\skills\agent-self-improvement\scripts\learning.py"
python $learn on --project $project
python $learn status --project $project
```

Restart OpenCode Desktop, open the project root, and inspect available skills. The plugin resolves the local recorder path without requiring user-wide environment variables.

## Existing installations and conflicts

If `.agents` already exists, use the existing [upgrade procedure](upgrade.md) to reconcile vendor code and preserve local changes before installing the recorder. The installer deliberately refuses to overwrite an existing Kit, plugin, or `opencode.jsonc`. For JSONC, merge `".agents/AGENTS.md"` into `instructions` manually.

The learning engine analyzes selected private sessions through your chosen model provider and writes **review-only** proposals. It never changes skills merely because the plugin is installed. See [the skill integration guide](../../skills/agent-self-improvement/assets/integrations/INTEGRATIONS.md) for checks and proposal approval.

## Privacy and compatibility

Installed experience data is private local state, not part of Git. Images and documents are retained automatically only if OpenCode exposes embedded data URLs. Remote links and arbitrary local paths are not fetched. Actual client behavior must be verified in the local installation; CI validates installer packaging and repeatable synthetic behavior only.
