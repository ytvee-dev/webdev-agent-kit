---
id: 'agents.skills.design-screenshot-spec.references.design-source-inspection'
title: 'Design Source Inspection'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'design-screenshot-spec'
tags:
    - 'frontend/design'
    - 'agents/reference'
parent:
    - '[[skills/design-screenshot-spec/SKILL|Design Screenshot Spec]]'
related:
    - '[[common/tool-capability-model|Tool Capability Model]]'
    - '[[skills/design-screenshot-spec/references/spec-extraction-checklist|Spec Extraction Checklist]]'
depends_on: []
---

# Design Source Inspection

Use for a supplied live design link. For images without a link, go directly to
the extraction checklist. Sections cover routing, MCP, browser inspection,
coverage, and the source basis.

## Route From Actual Access

1. Identify the supplied file URL and requested frame/node, page, variant, and
   viewport. Preserve the user's link; do not substitute another file or a
   current desktop selection without matching its identity.
2. Discover callable read tools. A configured server or old profile is only a
   candidate; a successful scoped read establishes access to this file.
3. Prefer Figma MCP reads. If absent, denied, rate-limited, or unusable, try
   available browser/computer use on the supplied link. Partial MCP evidence
   remains useful: inspect missing properties or motion in the browser.
4. If both live paths are blocked, analyze any supplied screenshots and identify
   the remaining access/coverage gap. If no usable evidence exists, ask for
   access or exports showing the exact frame, selected layer, and property panel.
5. Without a link, inspect supplied images. Use a desktop selection only when
   the user explicitly identifies it as the source and the provider supports it.

Do not silently repair MCP configuration, install providers, request new sharing
permissions, bypass login, or turn intake into canvas editing. Reuse an allowed
session. If login requires the user, report the exact visible requirement and
resume from fresh state after confirmation. A public preview is not editor access.

## MCP Inspection

- Read the available tool contract and any required host skill first. Tool names
  below describe common Figma capabilities, not guaranteed callable APIs.
- Fetch design context for the exact node (`get_design_context` when exposed)
  and visually inspect its matching screenshot (`get_screenshot` or equivalent).
  Generated framework code is design evidence, not proof of intended behavior
  or a mandate to change the host stack.
- If scope is ambiguous, locate pages/frames through metadata and ask which
  plausible target is intended. Never inspect an entire unrelated workspace.
- If context is truncated or too coarse, use metadata to locate child nodes and
  request bounded sections. Metadata alone does not establish styles. Continue
  until every in-scope section and distinct component/state has evidence.
- Read text runs, auto-layout direction/wrapping, gap and padding, alignment,
  fixed/hug/fill sizing, constraints, clipping, fills, strokes, effects, radii,
  assets, component identity, variants, and instance overrides when exposed.
- Fetch relevant variables/styles and record binding, resolved value, mode,
  aliases, and units. Read existing Code Connect mappings when available; do
  not create mappings or substitute a merely similar project component.
- Inspect prototype interactions and animation data when present. Use a motion
  context read if exposed; otherwise inspect prototype settings/playback in the
  browser. Missing motion data means unknown, not zero animation.
- Use returned assets where authorized and accessible. Record export scale,
  crop, and format. Temporary URLs are not durable production asset paths;
  missing assets must not be silently replaced by stock icons or approximations.

## Browser / Computer Use Inspection

Follow the current host's browser/computer-use instructions, using only exposed
APIs. The fallback needs visual screenshots plus mouse/pointer control; a
DOM-only or text-only reader may be insufficient for a design canvas.

1. Open the supplied link in the permitted browser/session. Verify file title,
   page/frame, and actual access. Wait for the design and fonts to render; take
   a fresh overview screenshot before selecting anything.
2. Use observed layer names or current screenshot coordinates to select the
   intended frame. Zoom/pan until its contents and property panel are legible.
   Never infer a canvas layer's styles from the surrounding web editor's CSS.
3. For each distinct component, select its actual layer using the layers panel
   or canvas pointer. Expand groups or select nested text/icon/background layers
   as needed. Verify the selection outline, layer name, and parent context.
4. Open the available Design/Inspect/Dev Mode panels without changing access or
   buying a seat. Read dimensions, auto-layout, typography, fills, strokes,
   effects, variables/styles, component variants, and responsive constraints.
   Expand/scroll collapsed property sections and capture the selected layer
   together with the values. Recheck selection after every navigation or click.
5. Inspect other supplied states and viewports, instance overrides, menus,
   dialogs, drawers, validation, and empty/loading/error frames when available.
   Read prototype trigger, destination, overlay placement/dismissal, transition,
   easing, duration, delay, and scroll rules. Preview only interactions that stay
   within authorized inspection; do not submit real forms or follow external
   actions that mutate data.
6. Capture fresh evidence after meaningful selection/state changes. Restore
   view/selection when practical; never drag, resize, recolor, detach, or edit
   source layers to discover their properties.

If Dev Mode, a property, or prototype settings are unavailable, record precisely
what is inaccessible and use other permitted views. Do not repeat a failing
path indefinitely or claim exact values from an illegible panel. Request the
smallest missing selection/property capture after available inspection is used.

## Coverage And Stop Condition

Maintain a compact component ledger: source ID, node/layer path, parent,
variant/state, viewport/mode, properties inspected, evidence pointer,
confidence, and missing details. Shared properties may cite a verified base
component; record every override and inspect each distinct state separately.

Stop acquisition when every in-scope component has evidence or a stated gap,
not after the first overview. Keep unrelated pages outside the ledger. Pass
unresolved visual conflicts and behavior gaps to the product review; never mark
an unreadable, truncated, or access-denied source fully inspected.

## Source Basis

Reviewed 2026-09-14; these are evidence sources, not additional runtime reading
or authority over the user's task.

- [OpenAI Figma skill](https://github.com/openai/skills/blob/main/skills/.curated/figma/SKILL.md): pair structured context with visual evidence, recover truncated reads by node, reuse project conventions.
- [OpenAI implementation skill](https://github.com/openai/skills/blob/main/skills/.curated/figma-implement-design/SKILL.md): exact selection, asset provenance, visual comparison. Token conflicts in this kit require explicit resolution rather than silent substitution.
- [Figma tool contracts](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/): metadata, variables, motion, asset exports, and remote versus desktop selection.
- [Figma frame sizing guidance](https://developers.figma.com/docs/figma-mcp-server/avoid-large-frames/): split large selections into inspectable sections.
- [Anthropic browser testing skill](https://github.com/anthropics/skills/blob/main/skills/webapp-testing/SKILL.md): inspect rendered state before acting. This kit uses the available host controls and does not require its Python runner.

The MCP-to-browser fallback and user-decision gate are this kit's product
requirements; they are not claimed as guarantees made by those upstream skills.
