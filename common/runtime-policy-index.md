---
id: 'agents.common.runtime-policy-index'
title: 'Runtime Policy Index'
doc_type: 'common-index'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'routing/progressive-disclosure'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/test-policy|Test Change And Verification Policy]]'
    - '[[common/readme-policy|README Read And Edit Policy]]'
    - '[[common/policy-precedence|Policy Precedence]]'
    - '[[common/core/runtime-core-policy|Portable Runtime Core Policy]]'
    - '[[profiles/react-typescript/PROFILE|React TypeScript Profile]]'
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
    - '[[common/target-stack-policy|Target Stack Policy]]'
    - '[[common/skill-applicability-policy|Skill Applicability Policy]]'
    - '[[common/rendered-visual-verification-policy|Rendered Visual Verification Policy]]'
    - '[[common/lightweight-routing-policy|Lightweight Routing Policy]]'
    - '[[common/documentation-maintenance|Documentation Maintenance]]'
    - '[[common/prompt-intent-routing-rules|Prompt Intent Routing Rules]]'
    - '[[common/approved-patterns|Approved Patterns]]'
    - '[[common/anti-patterns|Common Anti-Patterns]]'
    - '[[common/design-quality-rubric|Design Quality Rubric]]'
    - '[[common/anti-template-defaults|Anti-Template Defaults]]'
    - '[[common/interface-copy-rules|Interface Copy Rules]]'
    - '[[common/motion-rules|Motion Rules]]'
    - '[[common/ui-ux-priority-checklist|UI UX Priority Checklist]]'
    - '[[common/css-modules-specificity-rules|CSS Modules Specificity Rules]]'
    - '[[common/form-feedback-rules|Form Feedback Rules]]'
    - '[[common/navigation-ux-rules|Navigation UX Rules]]'
    - '[[common/data-visualization-rules|Data Visualization Rules]]'
    - '[[common/icon-quality-rules|Icon Quality Rules]]'
    - '[[common/mobile-responsive-rules|Mobile Responsive Rules]]'
    - '[[common/agent-loop-policy|Agent Loop Policy]]'
    - '[[common/stop-criteria-rules|Stop Criteria Rules]]'
    - '[[common/bounded-retry-rules|Bounded Retry Rules]]'
    - '[[common/verification-loop-rules|Verification Loop Rules]]'
    - '[[common/windows-shell-sandbox-rules|Windows Shell Sandbox Rules]]'
    - '[[common/context-compaction-rules|Context Compaction Rules]]'
    - '[[common/independent-review-rules|Independent Review Rules]]'
    - '[[common/worktree-parallelism-rules|Worktree Parallelism Rules]]'
    - '[[common/agent-operating-model|Agent Operating Model]]'
    - '[[common/framework-adaptation-policy|Framework Adaptation Policy]]'
    - '[[common/typescript-discipline|TypeScript Discipline]]'
    - '[[skills/frontend-design-intelligence/SKILL|Frontend Design Intelligence]]'
    - '[[skills/loop-workflow-planner/SKILL|Loop Workflow Planner]]'
    - '[[skills/greenfield-project-builder/SKILL|Greenfield Project Builder]]'
    - '[[skills/project-onboarding-adapter/SKILL|Project Onboarding Adapter]]'
    - '[[skills/project-context-adapter/SKILL|Project Context Adapter]]'
    - '[[skills/mcp-toolchain-manager/SKILL|MCP Toolchain Manager]]'
depends_on: []
---

# Runtime Policy Index

Purpose: keep source-graph navigation out of the always-on runtime entrypoint.

Load policy from the owning skill or affected surface, not from this index as a batch. The compact entrypoint selects workflow scale and skill; `common/core/runtime-core-policy.md` supplies shared behavior; the selected skill then points to any detailed common rules or references needed for the active slice.

Graph metadata in this source file supports maintenance and link validation. Generated runtime targets strip that metadata.
