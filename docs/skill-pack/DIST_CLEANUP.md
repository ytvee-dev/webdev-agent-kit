# Dist Cleanup Policy

Status: active cleanup note.

Source files are the source of truth for the skill pack.

Generated distribution output under `dist/codex/**` and `dist/claude/**` must not be used for normal source editing, prompt routing, skill selection, or runtime context gathering.

## Current Policy

- Edit source files first: `AGENTS.md`, `common/**`, `skills/**`, `templates/**`, `examples/**`, `plugin.json`, and human docs.
- Rebuild distribution targets after source changes.
- Do not manually patch only one generated target.
- Do not read `dist/**` during normal agent runtime.
- Keep `dist/**` ignored for future local generation.

## Cleanup Target

The preferred release shape is source-first:

- source files stay in the branch;
- generated `dist/**` is produced during packaging or release;
- generated output is not treated as durable source.

If committed distribution targets are kept for release reasons, each target must be regenerated from source before release and treated as generated output.

## Known Cleanup Item

`webdev_assistant_remaining_work_plan.md` is a downloaded planning artifact and should not remain in the repository. Remove it when the file deletion tool allows it.
