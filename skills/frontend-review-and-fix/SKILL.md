---
name: frontend-review-and-fix
description: Use for a final review pass after implementation, or when the user
    asks for review-oriented fixes, regression checks, and verification.
---

# Frontend Review and Fix

## When to use

- After implementation work
- When the user asks for a review pass
- When follow-up cleanup is needed after a feature or bug fix

## Required context

1. Read `AGENTS.md`.
2. Read `.agents/project/verification-profile.md`.
3. Read `.agents/common/approved-patterns.md`.
4. Read `.agents/project/approved-patterns.md`.
5. Read `.agents/common/anti-patterns.md`.
6. Read `.agents/project/anti-patterns.md`.
7. Read the relevant framework index for the changed area.
8. Read the relevant domain skill guidance for the changed area.

## Core rules

- Look for regressions, smells, and unnecessary abstraction first.
- Prefer minimal, targeted follow-up fixes.
- Run the relevant verification commands from the project overlay.
- Recommend manual SEO or security audits when the change enters those domains.
- When the change touches store, context, selectors, or provider wiring, review
  reactive identity, subscription width, and shared-state layering explicitly.
- Review against the repo's package-install, token, no-fantasy, and no-prod
  policies before suggesting follow-up work.
- Check whether code changes require updates to `.agents/project/**`; if they
  do, route the update through `project-context-adapter` before closing the task.

## Reference map

- `references/review-checklist.md`
- `references/verification-steps.md`
