---
id: 'agents.skills.project-onboarding-adapter.references.path-audit-checklist'
title: 'Path Audit Checklist'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'project-onboarding-adapter'
tags:
    - 'agents/skill-package'
    - 'agents/onboarding'
    - 'agents/reference'
parent:
    - '[[skills/project-onboarding-adapter/SKILL|Project Onboarding Adapter]]'
related:
    []
depends_on:
    - '[[skills/project-onboarding-adapter/SKILL|Project Onboarding Adapter]]'
---

# Path Audit Checklist

Use this checklist in Plan Mode to verify that `.agents` docs and skills refer
to paths that exist or are intentionally documented as templates.

## Bundle Docs To Audit

Check path references in:

- host-root `AGENTS.md`;
- `.agents/AGENTS.md`;
- `.agents/SUMMARY.md`;
- `.agents/README.md`;
- `.agents/common/**`;
- `.agents/skills/*/SKILL.md`;
- `.agents/skills/*/agents/openai.yaml`;
- `.agents/skills/*/references/**`;
- `.agents/project/**`.
- host project frontend manifests, configs, source roots, routes, styles, tests,
  and verification scripts referenced by `project/**`.

## What Counts As Valid

A referenced path is valid when it is one of:

- an existing file or directory;
- an intentionally local-only path protected by `.agents/.gitignore`;
- a documented template pattern such as `skills/<skill-name>/SKILL.md`;
- a future file explicitly planned for creation during adaptation;
- an external URL that resolves to the intended official or project source.
- an official MCP server or documentation source that is reported as missing
  but not required for the current execution step.

## What To Flag

Flag these as drift in the adaptation plan:

- missing concrete files or directories;
- renamed skills still referenced by old names;
- `agents/openai.yaml` paths without matching skill folders;
- references named in `SKILL.md` that do not exist;
- files under `.agents/project/**` described as publishable;
- missing `project/mcp-profile.md` or stale MCP dependency facts after
  `skills/*/agents/openai.yaml` changed;
- missing `project/design-reference-profile.md` or remaining references to the
  old design-source overlay after the neutral design-reference overlay is
  adopted;
- publishable docs containing host-project-specific source paths or facts;
- root `AGENTS.md` content that mirrors `.agents/AGENTS.md` instead of pointing
  to it;
- sync or publication instructions that operate from the host root instead of
  the nested `.agents` checkout.
- app source files, framework configs, package manifests, routes, components,
  styles, tests, or build scripts planned for creation during new-project
  onboarding.
- Figma MCP, whiteboard, live-design inspection, canvas editing, file creation,
  design-system generation, or Code Connect tooling listed as a required or
  fallback dependency.

## Output Format

Group findings in the adaptation plan as:

- `Valid paths`: important paths that were verified.
- `Missing paths to create`: expected project overlays or pointer files.
- `Stale paths to fix`: existing docs or skills that reference wrong paths.
- `Template paths`: examples that should stay as patterns.
- `Local-only paths`: paths that must not be staged or published upstream.
- `MCP findings`: required, available, missing, approved, installed, skipped, or
  blocked MCP capabilities from current skill metadata.
