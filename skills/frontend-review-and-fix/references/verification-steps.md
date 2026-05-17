---
id: 'agents.skills.frontend-review-and-fix.references.verification-steps'
title: 'Verification Steps'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-review-and-fix'
tags:
    - 'agents/skill-package'
    - 'frontend/review'
    - 'agents/reference'
parent:
    - '[[skills/frontend-review-and-fix/SKILL|Frontend Review and Fix]]'
related:
    []
depends_on:
    - '[[skills/frontend-review-and-fix/SKILL|Frontend Review and Fix]]'
---

# Verification Steps

Start from `.agents/project/verification-profile.md` for the exact commands.

## Which checks to run

| Change type | Run |
|---|---|
| TypeScript source files changed | `tsc --noEmit` |
| ESLint-covered files changed | `eslint .` |
| Any text or code file changed | `prettier --check .` |
| Route files, layouts, or Next.js config changed | `npm run build` |
| Doc-only or skill-only change | `prettier --check .` only |

## Process

1. Run only the checks relevant to the touched surface (see table above).
2. Stop and report the first failing check before running the next one.
3. Fix the failure, then re-run the same check to confirm it passes.
4. Do not pile on all checks at once — failing output from multiple tools is
   harder to act on than one clear failure at a time.
5. Do not use `npm run dev` as a substitute for the verification flow.
6. Do not point any verification step at production systems or production data.
