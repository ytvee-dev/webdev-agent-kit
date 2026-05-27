---
id: 'agents.skills.technical-seo-app.references.external-content-taxonomy'
title: 'External Content Taxonomy'
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
    - '[[skills/technical-seo-app/references/audit-rubric|Audit Rubric]]'
depends_on:
    - '[[skills/technical-seo-app/SKILL|Technical SEO App]]'
---

# External Content Taxonomy

Use this reference when posts, essays, products, docs, or other SEO-relevant
content live outside the application repository and are loaded during build or
server rendering.

## Audit Steps

1. Locate the content-source boundary and schema/parser for frontmatter.
2. Identify which fields drive SEO: title, SEO title, description, slug, date,
   updated date, published state, tags, locale, social image, canonical path,
   and body text extraction.
3. Trace those fields into listing pages, detail metadata, sitemap entries,
   structured data, tag/taxonomy pages, feeds, and AI-readable summaries.
4. Confirm unpublished or invalid content cannot appear in indexable sitemap,
   tag pages, metadata, or machine-readable documents.
5. Check tag normalization, duplicate handling, slug generation, language, and
   visible links before changing keyword or taxonomy behavior.

## Implementation Rules

- Reuse the existing parser, content queries, tag helpers, and SEO helpers.
- Validate and normalize at the content boundary instead of adding downstream
  fallback coercion.
- Keep stable site-wide keywords separate from content-derived tags.
- Do not hardcode one host project's remote repository names in reusable skill
  instructions; put those facts in `.agents/project/**`.
- If content is private or token-gated, do not request or expose secrets. Report
  the missing access and verify only the local code path.

## Output Expectations

For taxonomy work, report:

- source fields inspected;
- generated SEO surfaces affected;
- normalization and duplicate behavior;
- missing or risky propagation paths;
- verification commands or manual checks needed after content changes.
