# Documentation Maintenance Workflow

Use this workflow when the task changes `.agents/`, a skill package, or repo
agent policy stored in overlays.

## Workflow

1. Input analysis.
   - Identify the requested documentation change and why it is needed.
   - Decide whether the change affects `AGENTS.md`, `.agents/common`,
     `.agents/project`, `.agents/skills`, the nested `.agents` git repo
     contract, or
     `.agents/SUMMARY.md`.
2. Impact analysis.
   - List every directly affected file.
   - Check related common docs, project overlays, path indexes, nested-repo
     rules, cross-skill references, and summary entries that may become stale.
3. Structure change procedure.
   - Add, rename, or remove files only when the new structure is clearly
     simpler or more accurate.
   - If a skill package is added or renamed, update its `agents/openai.yaml`,
     `.agents/SUMMARY.md`, and any skill-routing docs that should point to it.
   - If a common doc moves between `.agents/project` and `.agents/common`,
     update every reader so the layer boundary stays explicit.
   - If the nested repo root changes shape, update `.agents/.gitignore`,
     `.agents/README.md`, and any sync contract that mentions canonical paths.
4. Cross-link procedure.
   - Re-check file paths after any rename, move, or new reference.
   - Update summary entries, reference maps, and path-index links in the same
     pass.
5. Rule conflict check.
   - If a project overlay changes, inspect the related skills for duplicated or
     conflicting guidance.
   - If a common doc changes, inspect both skills and local overlays for stale
     assumptions.
   - If a skill changes, inspect the matching common docs and overlays for stale
     assumptions.
6. Pattern propagation.
   - If a new approved pattern is added, check whether the relevant domain
     skills should link to it.
   - If a new anti-pattern is added, check whether the relevant domain skills
     should enforce it.
7. Final consistency pass.
   - Confirm that every referenced file exists.
   - Confirm that no host-project facts leaked into `.agents/common/**`,
     reusable skills, or `.agents/README.md`.
   - Confirm that no repo-specific facts leaked into reusable skills.
   - Confirm that no reusable workflow was buried inside a repo-specific
     overlay.
   - Confirm that the updated tree is reflected in `.agents/SUMMARY.md`.
   - Confirm that any new branch or commit examples follow the
     `[fix|feat]-[description]` and `fix(docs): ...` / `feat(docs): ...`
     contract.
