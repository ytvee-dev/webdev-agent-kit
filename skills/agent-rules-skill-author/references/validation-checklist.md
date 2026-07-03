---
id: 'agents.skills.agent-rules-skill-author.references.validation-checklist'
title: 'Validation Checklist'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'agent-rules-skill-author'
tags:
    - 'agents/skill-package'
    - 'agents/authoring'
    - 'agents/reference'
parent:
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
related:
    []
depends_on:
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
---

# Validation Checklist

Use this checklist before and after editing repo-local agent rules or skills.

## Section Map

- `Before saving` for structural, trigger, portability, and packaging checks.
- `After saving` for cold-read review, reference routing, and final validation
  commands.

## Before saving

- SKILL.md frontmatter exists and uses a YAML mapping shape.
- Trigger surface is explicit and narrow enough to avoid unrelated invocations.
- The package clearly states whether it is `.agents`-compatible or strict
  native-portable.
- Trigger wording has at least one realistic should-trigger and one near-miss
  should-not-trigger prompt when the boundary is non-obvious.
- No conflict exists with current `AGENTS.md` policy.
- Removed catalogs and deleted documentation surfaces are not referenced by
  runtime instructions, graph metadata, scaffolding, or validators.
- Documentation file contents and directory structure were inspected through
  filesystem MCP when available, with shell reserved for search, git state,
  diffs, formatting, or executable validation.
- The target layer is correct: `AGENTS.md`, `.agents/common`, `.agents/project`, or
  `.agents/skills`.
- `SKILL.md` stays procedural and compact.
- Skill instructions are grounded in source material, real examples, or known
  failure modes rather than generic advice.
- There are 2-3 realistic workflow prompts ready for a sanity check when the
  skill or its workflow changed materially.
- `name` uses lowercase letters, digits, and hyphens only, with no leading,
  trailing, or repeated hyphens, and stays within 64 characters.
- Inputs, outputs, defaults, failure modes, and validation gates are explicit
  for fragile workflows.
- `description` is a string, avoids angle brackets, and stays within 1024
  characters.
- Expected output format or report shape is explicit when output structure
  matters.
- The validation model fits the workflow: objective checks for objective work,
  human review criteria for judgment-heavy work.
- The choice between instruction-only, `references/`, and `scripts/` is
  justified by repeatability and risk rather than habit.
- For `.agents` skills, `name` and `description` stay first, and graph metadata
  is treated as a local extension after the native contract.
- Every referenced file exists and is linked from `SKILL.md`.
- References longer than 100 lines have a table of contents or another clear
  section map near the top.
- `agents/openai.yaml` exists, is parseable, and aligns with the skill intent.
- `interface.short_description` stays within 25-64 characters.
- If `interface.default_prompt` is present, it mentions `$skill-name`.
- If `dependencies.tools` is present, it documents real tool dependencies.
- No changed files exist outside `.agents/` except the repository root
  `AGENTS.md` when repo-wide policy, skill discovery, or upstream bundle
  maintenance changed.
- Any `.agents/` documentation branch or commit examples follow the
  `[fix|feat]-[description]` and `fix(docs): ...` / `feat(docs): ...` contract.
- Any `.agents/` documentation gitflow examples keep local work on `main`,
  commit only eligible publishable paths, branch only for push/PR, and return
  the local checkout to `main`.
- Publication workflows include a commit gate: no branch, push, PR, or success
  report may happen while eligible publishable documentation changes remain
  uncommitted.
- Branch switching examples include a dirty-tree and unmerged path guard.
- Removed skill names, stale paths, and outdated references were searched across
  `.agents`.
- `.agents/README.md` was updated or explicitly checked when documentation
  changes affected user-facing workflow, skill lists, path policy, or
  sync/publication instructions.
- No auxiliary docs such as `README.md` or `CHANGELOG.md` were added to the
  skill package.
- `agents/openai.yaml` matches the skill trigger and intent.

## After saving

- Re-read the package as if another agent will use it cold.
- Confirm frontmatter alone explains when the skill should load.
- Confirm the frontmatter and body together make the trigger boundary clear
  without relying on the surrounding chat.
- Check that prohibitions, exceptions, and precedence are explicit.
- Check that the workflow leaves no hidden implementation decisions.
- Check that the package still reads like a workflow, not a long article.
- Check that repo-specific facts remain in overlays rather than reusable skill
  text.
- Check that references are loaded by clear conditions, not by vague
  directory-level pointers, and that the skill does not require reading every
  reference on each run.
- Check that output-quality assertions or manual review criteria would catch
  shallow compliance.
- Check that no Claude-specific runner, viewer, packaging, or CLI dependency
  became a hidden requirement for the workflow.
- Run `python skills/agent-rules-skill-author/scripts/validate_agent_skill.py <skill-dir>` for new or materially
  changed `.agents` skills.
- Run `npx prettier --check .` for markdown and skill-only changes.
