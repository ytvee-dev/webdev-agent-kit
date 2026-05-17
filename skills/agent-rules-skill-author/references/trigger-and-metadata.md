# Trigger And Metadata

Use this guide when writing skill frontmatter and `agents/openai.yaml`.

## Frontmatter

- Keep only `name` and `description`.
- Use lowercase hyphen-case for `name`.
- Write `description` as the primary trigger surface: what the skill does and
  when to use it.
- Mention concrete task shapes in the description, not only broad topics.
- Keep `description` non-empty and under 1024 characters.
- Front-load the most important trigger words because long skill lists may
  shorten descriptions before matching.

## Trigger writing

- Include both verbs and artifacts: `create`, `edit`, `refresh`, `rules`,
  `skills`, `AGENTS.md`, `.agents/project`, `.agents/skills`.
- Mention the target boundary when it matters, such as `inside .agents/`.
- Avoid vague triggers that could accidentally match unrelated app work.
- Describe user intent instead of internal implementation. Say when the user
  needs the workflow, not only what files the skill contains.
- Include near-miss exclusions when keywords overlap with unrelated work.

## Trigger evals

Before finalizing trigger wording for a new or broadened skill:

- Write realistic should-trigger prompts that vary phrasing, explicitness,
  detail, and complexity.
- Write near-miss should-not-trigger prompts that share keywords but require a
  different workflow.
- Confirm explicit invocation still works through `$skill-name`.
- Confirm implicit invocation is appropriate before keeping
  `allow_implicit_invocation: true`.

## UI metadata

- Keep `display_name` human-readable and close to the skill title.
- Keep `short_description` compact and specific.
- Write `default_prompt` as a direct invocation sentence using `$skill-name`.
- Keep `allow_implicit_invocation` aligned with prompt-driven skill selection.
  If a skill should run from user intent, set it to `true` and avoid manual-only
  language in `SKILL.md`.

## Metadata sync checklist

- `description` and `default_prompt` should point at the same workflow.
- `short_description` should not promise more than the skill actually covers.
- If the skill becomes broader or narrower, update both `SKILL.md` and
  `agents/openai.yaml` in the same change.
