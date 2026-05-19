---
id: 'agents.skills.frontend-security-inspector.references.security-checklist-react'
title: 'React Security Checklist'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-security-inspector'
tags:
    - 'agents/skill-package'
    - 'frontend/security'
    - 'agents/reference'
parent:
    - '[[skills/frontend-security-inspector/SKILL|Frontend Security Inspector]]'
related:
    []
depends_on:
    - '[[skills/frontend-security-inspector/SKILL|Frontend Security Inspector]]'
---

# React Security Checklist

Use this checklist for React frontend code, browser-executed code, and client
UI that receives data from URLs, storage, remote APIs, CMS content, or
third-party scripts.

## Secrets and configuration

- Never put secrets in browser-executed code, public assets, or client-exposed
  build-time variables such as `VITE_*`, `REACT_APP_*`, or `NEXT_PUBLIC_*`.
- Treat any value reachable by the browser as public.
- Check `public/`, runtime config files, source maps, and committed `.env`
  examples for accidental exposure.

## Unsafe rendering

- Check every use of `dangerouslySetInnerHTML`. It must never receive
  user-supplied content without prior sanitization.
- Prefer rendering structured data as React elements instead of injecting HTML
  strings.
- Treat markdown, CMS content, rich text, and persisted user content as
  untrusted until sanitized by an approved helper.
- Search for direct DOM sinks such as `innerHTML`, `outerHTML`,
  `insertAdjacentHTML`, `document.write`, `eval`, and `new Function`.

## Client-side storage

- Verify client-side storage (`localStorage`, `sessionStorage`, cookies) does
  not hold secrets, long-lived credentials, or sensitive personal data.
- Session tokens stored in `localStorage` are accessible to JavaScript and
  vulnerable to XSS; prefer `httpOnly` cookies for authentication tokens.

## Data flow

- Review data flow for accidental exposure of sensitive values through props,
  context, or global state that reaches the client bundle.
- Ensure validation is not assumed just because UI constraints exist — server-side
  input validation must stand independently of any client-side form constraints.
- Treat URL parameters, hash fragments, browser storage, postMessage payloads,
  remote API responses, feature flags, CMS content, and third-party script data
  as attacker-influenced unless the repo proves otherwise.

## Navigation and network

- Validate user-influenced redirect and navigation targets with an allowlist.
- Use `rel="noreferrer"` or `rel="noopener noreferrer"` for untrusted external
  links opened in a new tab.
- Review fetch or axios wrappers for dynamic base URLs, credentialed requests,
  and accidental data exfiltration paths.
- If cookie-based auth is used, confirm state-changing requests have server-side
  CSRF protections.

## Third-party scripts

- Audit third-party scripts loaded via `<Script>` or manual `<script>` tags.
  Third-party scripts run with the same origin privileges as your app and can
  access DOM, cookies, and client-side storage.
- Prefer `strategy="lazyOnload"` for non-critical scripts to reduce attack surface
  at initial page load.
- Verify Subresource Integrity or a self-hosting decision for CDN scripts when
  the repo has a production security baseline for it.
