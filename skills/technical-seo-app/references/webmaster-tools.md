---
id: 'agents.skills.technical-seo-app.references.webmaster-tools'
title: 'Webmaster Tools'
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
depends_on:
    - '[[skills/technical-seo-app/SKILL|Technical SEO App]]'
---

# Webmaster Tools

Use this reference for Google Search Console or Yandex Webmaster setup that
requires code changes.

## Verification Rules

- Never invent verification tokens.
- Prefer an existing repo config or user-provided token. If neither exists, ask
  for the exact token and stop before implementation.
- Do not log into webmaster dashboards or claim ownership verification was
  completed unless the user provided proof or an approved connector did it.
- Keep verification code close to the existing metadata or static-file pattern.

## Google Search Console

- Official ownership methods include DNS records, uploaded HTML files, HTML
  tags, Google Analytics, Google Tag Manager, and Google Sites/Blogger methods.
- For Next.js App Router, prefer `metadata.verification.google` when the user
  provides an HTML tag content token and the repo already centralizes metadata.
- Use a public static verification file only when the user provides the file
  name and exact content and the repo convention supports serving it unchanged.
- After code deployment, the user still needs to run verification in Search
  Console and submit or inspect the sitemap there.

## Yandex Webmaster

- Yandex supports access-right verification methods such as DNS, HTML file, or
  meta tag depending on the property.
- For Next.js App Router, prefer `metadata.verification.yandex` when the user
  provides the Yandex meta tag value and the repo already uses Metadata API.
- Confirm the generated meta tag is present on the production canonical host
  before telling the user to re-check verification in Yandex Webmaster.

## Sitemap Submission

- Keep sitemap URL absolute and stable, usually `https://example.com/sitemap.xml`.
- Include the sitemap in `robots.txt` when the site already generates robots.
- Tell the user which dashboard action remains manual: submit sitemap, inspect
  URL, request indexing, or re-run ownership verification.
