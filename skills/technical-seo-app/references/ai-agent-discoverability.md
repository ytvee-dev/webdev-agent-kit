---
id: 'agents.skills.technical-seo-app.references.ai-agent-discoverability'
title: 'AI Agent Discoverability'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'technical-seo-app'
tags:
    - 'agents/skill-package'
    - 'frontend/seo'
    - 'agents/reference'
parent:
    - '[[skills/technical-seo-app/SKILL|Technical SEO App]]'
related:
    - '[[skills/technical-seo-app/references/source-refresh|Source Refresh]]'
    - '[[skills/technical-seo-app/references/crawling-indexing|Crawling and Indexing]]'
depends_on:
    - '[[skills/technical-seo-app/SKILL|Technical SEO App]]'
---

# AI Agent Discoverability

Use this reference when the user asks for AI-browser, AI-agent, LLM, crawler, or
machine-readable content optimization.

## Principles

- Separate search indexing, AI crawler access, and agent-readable summaries.
  They overlap, but official docs treat them as different controls.
- Do not promise ranking, AI Overview inclusion, or model-training inclusion.
  State only the access or machine-readability effect that the code controls.
- Keep human-visible canonical content as the source of truth. Machine-readable
  files should summarize or point to it, not contradict it.

## What To Audit

- `robots.txt` rules for search crawlers and AI crawlers named in official
  provider docs.
- Page-level robots metadata, snippet controls, and noindex behavior.
- `llms.txt`, `llms-full.txt`, Markdown mirrors, RSS/feed surfaces, sitemap,
  canonical URLs, and structured data.
- Whether dynamic content, tags, dates, and descriptions from external content
  sources flow into machine-readable surfaces.
- Whether important content requires client-only rendering, blocked resources,
  auth, forms, or scripts that crawlers/agents cannot access.

## Provider Notes

- Google AI features rely on normal Google Search eligibility and documented
  preview/snippet controls; do not invent AI-only metadata.
- `Google-Extended` is a robots token for controlling Gemini app and Vertex AI
  grounding/training-related access. Do not treat it as the same as Googlebot.
- OpenAI documents crawler user agents such as `GPTBot`, `ChatGPT-User`, and
  `OAI-SearchBot`; verify current names before writing robots rules.
- Vercel and Next.js document `llms.txt` and Markdown access as agent tooling
  patterns. Treat them as a useful discoverability convention, not a search
  ranking standard.

## Implementation Checklist

- Keep `llms.txt` short and navigational.
- Keep `llms-full.txt` or Markdown mirrors complete enough for agents to find
  canonical sections, current published content, tags, and author/site context.
- Include canonical absolute URLs and language.
- Reuse existing content queries and tag helpers instead of duplicating content
  extraction logic.
- Verify generated text routes use `text/plain; charset=utf-8` or the repo's
  established content type.
