---
id: 'agents.changelog'
title: 'WebDev Agent Kit Changelog'
doc_type: 'changelog'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/changelog'
    - 'release-management'
parent: []
related:
    - '[[README|WebDev Agent Kit README]]'
    - '[[AGENTS|Canonical Agent Policy]]'
depends_on: []
---

# Changelog

All notable changes to WebDev Agent Kit should be recorded in this file.

Use this changelog for source-bundle and distribution-target changes that affect routing, skills, rules, validation, packaging, security, or installation behavior.

## Unreleased

### Added

- Added repository JSON schemas for bundle manifest metadata, skill frontmatter, OpenAI agent metadata, and graph document frontmatter.
- Added `scripts/validate_schemas.py` as a first schema-first validation pass before source and target validation.
- Added Apache License 2.0 through root `LICENSE` and bundle manifest metadata.
- Added a GitHub Actions validation workflow for source-bundle and generated-target checks.
- Added public contribution and security guidance for the reusable skill bundle.
- Added an audit-driven optimization plan that turns the prior research findings into tracked engineering work.

### Changed

- Split CI validation into explicit schema, source, build, target, and orchestrator steps with uploaded validation logs for failures.
- Hardened source validation so a clean reusable-bundle checkout does not require local-only `project/**` overlays.
- Removed README inventory checks from source validation because `README.md` is human-facing documentation, not an agent runtime or validation source.
- Clarified in runtime policy and authoring rules that `README.md` stays user-facing and outside agent reads.
- Included public OSS docs and `LICENSE` in generated Codex and Claude distribution targets when those files exist.
- `scripts/validate_skill_pack.py` now runs schema validation before legacy source, build, and target validators.

### Fixed

- Tolerated explicit indented empty-list syntax in frontmatter parsing.
- Allowed `skill-reference` as a valid graph document layer for skill reference files.
