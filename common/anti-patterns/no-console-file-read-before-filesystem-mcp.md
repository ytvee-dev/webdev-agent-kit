---
id: 'agents.common.anti-patterns.no-console-file-read-before-filesystem-mcp'
title: 'No Console File Read Before Filesystem MCP'
doc_type: 'anti-pattern-template'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'anti-patterns/tooling'
parent:
    - '[[common/anti-patterns/README|Anti-Pattern Templates]]'
related:
    - '[[common/tool-capability-model|Tool Capability Model]]'
    - '[[common/mcp-availability-detection-rules|MCP Availability Detection Rules]]'
depends_on: []
---

# No Console File Read Before Filesystem MCP

## Rule

Use the `project_files` capability for project file reads before falling back to shell or console reads.

When configured filesystem/project-files MCP is available, prefer it. If it is unavailable, use host-native file tools. Use targeted shell reads only as the final fallback.

## Avoid

```text
Run: cat src/app/page.tsx
```

when a file-reading capability is already available.

## Prefer

```text
Read the project file through the configured project_files/filesystem capability.
```

## Exception

Use targeted shell reads when the file capability is unavailable, failed, or the task specifically requires shell output behavior.

## Apply When

Use this for project inspection, onboarding, implementation, bugfix, refactor, and review work.
