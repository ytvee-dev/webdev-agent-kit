# Trigger And Metadata

Use this guide when writing skill frontmatter and `agents/openai.yaml`.

## Frontmatter

- Keep only `name` and `description`.
- Use lowercase hyphen-case for `name`.
- Write `description` as the primary trigger surface: what the skill does and
  when to use it.
- Mention concrete task shapes in the description, not only broad topics.

## Trigger writing

- Include both verbs and artifacts: `create`, `edit`, `refresh`, `rules`,
  `skills`, `AGENTS.md`, `.agents/project`, `.agents/skills`.
- Mention the target boundary when it matters, such as `inside .agents/`.
- Avoid vague triggers that could accidentally match unrelated app work.

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
