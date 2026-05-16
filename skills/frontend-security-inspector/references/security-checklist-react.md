# React Security Checklist

## Unsafe rendering

- Check every use of `dangerouslySetInnerHTML`. It must never receive
  user-supplied content without prior sanitization. Use a trusted HTML sanitizer
  (e.g. DOMPurify) before passing to `__html`.

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

## Third-party scripts

- Audit third-party scripts loaded via `<Script>` or manual `<script>` tags.
  Third-party scripts run with the same origin privileges as your app and can
  access DOM, cookies, and client-side storage.
- Prefer `strategy="lazyOnload"` for non-critical scripts to reduce attack surface
  at initial page load.
