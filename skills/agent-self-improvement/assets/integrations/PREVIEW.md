---
id: 'agents.skills.agent-self-improvement.assets.preview'
title: 'Preview Integration Status'
doc_type: 'skill-reference'
layer: 'skill'
status: 'draft'
publishable: true
local_only: false
skill: 'agent-self-improvement'
tags:
    - 'agents/learning'
parent:
    - '[[skills/agent-self-improvement/SKILL|Agent Self Improvement]]'
related: []
depends_on: []
---

# Preview integration status

The optional bridge receives Codex/Claude lifecycle JSON over stdin, stores user prompts and tool-name metadata in the private local store, and ignores the host transcript path rather than reading arbitrary client files. It does not claim to capture all assistant messages or uploaded attachment bytes.

To install, locate \`hook_bridge.py\` inside the extracted \`skills/agent-self-improvement/assets/integrations/\` directory and resolve an absolute Python invocation. Merge selected events with the client's existing hooks; inspect and trust configuration in the native UI.

For the OpenCode pilot, copy \`opencode/experience-recorder.js\` to the local plugin directory and point \`AGENT_LEARNING_SCRIPT\` to the absolute installed learning CLI. The plugin reads messages on \`session.idle\`, after checking that learning is enabled for that project.

Explicit file import example:
\`\`\`sh
python /absolute/path/to/learning.py attach --project /path/to/project --client opencode --session session123 --file /approved/path/screenshot.png
\`\`\`

Use the operating-system scheduler if you want regular offline triage. Such a timer generates findings only. An LLM-based autonomous trainer and automatic skill changes are not shipped in this preview.
