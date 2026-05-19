---
id: 'agents.skills.agent-rules-skill-author.references.skill-quality-rubric'
title: 'Skill Quality Rubric'
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

# Skill Quality Rubric

Use this rubric when creating a new skill, widening a skill, changing trigger
behavior, or repairing a skill that produced vague, inconsistent, or
over-broad results.

## Source grounding

- Start from real task examples, user corrections, repo docs, runbooks, API
  docs, schemas, review feedback, or failure cases.
- Use official product documentation for current external APIs, OpenAI
  surfaces, tools, SDKs, pricing, or behavior. Prefer configured docs MCP
  tools when available.
- Do not turn generic best practices into a skill unless they are tied to a
  repeatable workflow, concrete decision point, or known failure mode.
- Record the non-obvious facts an agent would miss without the skill. Remove
  explanations the model can already infer.

## Trigger precision

- Front-load the primary user intent in `description`; agents may only see the
  name and shortened description before activation.
- Include concrete verbs and artifacts the user is likely to mention.
- Name the boundary: where the skill applies, where it must not apply, and
  whether implicit invocation is safe.
- Use near-miss negative cases to tighten wording. A negative case should share
  keywords with the skill but require a different workflow, not be obviously
  unrelated.
- Use positive cases that vary by phrasing style: direct requests, indirect
  requests, casual wording, typo or noisy wording, and prompts that mention
  files or paths.
- Keep `description` within the Agent Skills limit of 1024 characters and short
  enough to survive description shortening in large skill sets.

## Instruction quality

- Write imperative workflow steps with explicit inputs, outputs, defaults, and
  stop conditions.
- Prefer defaults over menus. Mention alternatives only when the agent needs a
  clear escape hatch.
- Match control level to fragility:
  - high freedom for judgment-heavy work with several valid approaches;
  - medium freedom when a preferred pattern exists but adaptation is expected;
  - low freedom for fragile, stateful, repetitive, or hard-to-debug workflows.
- Add gotchas for mistakes agents are likely to make, especially naming
  mismatches, hidden state, compatibility rules, and tool-specific quirks.
- Provide output templates when final format matters more than prose guidance.
- Do not hide product decisions in the skill. Ask the user when success
  criteria, audience, boundaries, or risk tolerance would materially change the
  implementation.

## Resource choice

- Keep `SKILL.md` for trigger, core workflow, constraints, defaults, and gotchas
  needed on every run.
- Use `references/` for detailed examples, rubrics, variants, schemas, and
  optional background. Link each reference from `SKILL.md` and say when to read
  it.
- Use `scripts/` only for deterministic, repeated, fragile, or tool-heavy work.
  Scripts must be non-interactive, documented with `--help`, produce helpful
  errors, and separate structured stdout from diagnostics.
- Use `assets/` for templates or resources that should be copied or adapted in
  outputs, not for instructions the agent must read.
- Do not add auxiliary docs such as `README.md`, `CHANGELOG.md`, or
  `QUICK_REFERENCE.md` inside skill packages.

## Evaluation

- Create a small trigger eval set before finalizing trigger wording:
  8-10 should-trigger prompts and 8-10 near-miss should-not-trigger prompts for
  broad or high-risk skills; fewer examples are acceptable for narrow edits.
- Vary phrasing, explicitness, detail, complexity, typos, and file/path
  mentions so the trigger is tested against realistic user requests.
- After drafting the skill, run 2-3 realistic workflow prompts to see whether
  the instructions improve actual execution, not only frontmatter wording.
- Define output assertions for important behavior. Require concrete evidence
  for pass/fail judgments instead of accepting section labels or vague
  compliance.
- For judgment-heavy workflows, prefer explicit human review criteria over fake
  precision. Use observable checks where they help, and manual review where the
  outcome is inherently qualitative.
- Compare with-skill behavior against without-skill behavior when practical.
  Keep the skill only if it improves correctness, consistency, speed, or
  reviewability enough to justify its context cost.
- Read execution traces, not only final answers. Tighten instructions when the
  agent wastes steps, follows irrelevant branches, or makes inconsistent
  decisions across runs.
- Feed specific human feedback back into the skill. Add durable corrections to
  gotchas, workflow steps, validation gates, or references.

## Anti-overfitting

- Do not patch every failure with a narrow `must` or one more special-case
  bullet.
- Look for the shared cause behind repeated failures and explain the `why`
  inside the skill when that produces more durable behavior.
- Remove instructions that do not improve outcomes or that consistently cause
  wasted work, irrelevant branches, or verbose compliance theater.
- Revise for reusable behavior across prompts, not just the eval case that most
  recently failed.

## Reusable automation heuristic

- If multiple workflow evals repeatedly lead the agent to create the same
  helper steps, helper script, or output scaffold, that is evidence for
  `scripts/` or `assets/`.
- Keep the package instruction-only when the repeated helper work is unstable,
  highly contextual, or too rare to justify more bundle weight.

## Final quality gate

Before finishing, confirm:

- frontmatter alone tells another agent when to load the skill;
- body instructions explain what to do without re-teaching the whole domain;
- all referenced files exist and are loaded only when useful;
- repo-specific facts stay in `.agents/project`, not reusable skill text;
- the package has a clear validation path and no hidden decisions;
- `agents/openai.yaml` matches the trigger, scope, and implicit invocation
  policy.
- the skill improves correctness, consistency, reviewability, or speed enough
  to justify itself over weaker guidance or no skill at all.
