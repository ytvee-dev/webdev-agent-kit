# Next.js Security Checklist

## Server/client boundary

- Confirm sensitive server-only code stays off the client — use `import 'server-only'`
  to enforce this at build time.
- Check public entry points such as Route Handlers and Server Actions.
- Verify auth and authorization are enforced close to the data boundary, not
  only in UI conditional rendering.

## Environment variables

- Audit all environment variable names. Variables prefixed with `NEXT_PUBLIC_`
  are embedded in the client bundle and visible in the browser. Secrets must
  never have this prefix.
- Check that no secret (API key, token, database URL) is accidentally exposed
  via a `NEXT_PUBLIC_` variable or via a Server Component that forwards values
  to Client Component props.

## Redirects

- Review all `redirect()` calls. If the redirect target includes user-supplied
  input, validate and allowlist the destination to prevent open redirects.

## HTTP headers

- Verify security-relevant response headers are configured: `Content-Security-Policy`,
  `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`.
- Check headers in `next.config.ts` under the `headers()` export.

## Server Actions

- Ensure every Server Action that mutates data performs its own authorization
  check — do not rely solely on the UI being hidden from unauthorized users.
- Validate and sanitize all inputs to Server Actions before processing, using
  the project's approved boundary-validation approach rather than inventing a
  new dependency by default.
