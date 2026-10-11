# Notes Vault v3 — hard CSPT

CSPT ("client-side path traversal") is a CSRF amplifier: you control part of a
URL *path* built by client-side JavaScript, and because the **browser** normalizes
the path before sending it, server-side traversal filters never see the `..`.

## The app

- `GET /` → notes page (`public/app.js`). Reads `file` from the fragment:
  ```js
  const target = new URL('/api/v1/notes/' + file, location.origin);
  fetch(target.href, { credentials: 'same-origin' });
  ```
  and, if a `draft` param is present, `POST`s that body to `target.href`.
- The slug passes a client sanitizer that rejects `..`, `\`, `%2e`, `%2f`, `%5c`,
  `%25`.
- A backend WAF on `/api` rejects `..`, encoded slashes and `%25`.
- The admin bot (`/report`) opens submitted **`/` links only** with an admin
  session cookie (`HttpOnly; SameSite=Lax`), same pattern as other bots here.
- The flag is `GET /api/v1/admin/flag`, admin-only.

## Vulnerability

The sanitizer reasons about the slug as a string. `new URL()` reasons about it as
a **WHATWG URL**: the spec removes every ASCII tab (0x09), LF (0x0A) and CR (0x0D)
from the input *before* parsing. So a slug like `.\t./profile/password` contains
no `..` substring (it is `.`, TAB, `.`), passes the sanitizer, and only then
becomes `../profile/password` inside the parser.

```
'/api/v1/notes/' + '.\t./profile/password'
   -> WHATWG strips TAB
'/api/v1/notes/../profile/password'
   -> normalization
'/api/v1/profile/password'
```

The server WAF is irrelevant here: by the time the request leaves the browser its
path is already `/api/v1/profile/password`, with no `..` to detect.

Forcing the tab in the right place is the subtle part. The value must survive:

1. `new URL(raw).hash` on the server (in `/report`) — a literal tab would be
   stripped by the same URL parser, so it must be percent-encoded as `%09`.
2. the browser navigation — `%09` is preserved in the fragment.
3. the client — `new URLSearchParams(location.hash.slice(1)).get('file')` decodes
   `%09` back into a real TAB, which is exactly what `new URL()` then strips.

Secondary ban-tricks that are **blocked** here on purpose: `..\..\` (backslash is
a separator in special schemes, but `\` is rejected), `%2e%2e` (rejected by the
regex), `%2f` (rejected, and it is not a separator in WHATWG paths anyway).

## Exploitation

The autosave body is attacker-controlled, so point the traversal at the password
endpoint and set the admin's password to a value we know. The request is made by
the admin's own page, same-origin, so the `SameSite=Lax` cookie rides along.

```
#file=.%09./profile/password&draft=password%3Dpwned
```

1. Register an account, then `POST /report` with
   `http://HOST:3002/#file=.%09./profile/password&draft=password%3Dpwned`.
2. The admin bot loads the notes page. `new URL` strips the decoded tab, the
   client `POST`s `password=pwned` to `/api/v1/profile/password` with the admin
   cookie, and the admin password becomes `pwned`.
3. `POST /login username=admin&password=pwned`, then `GET /api/v1/admin/flag`.

`solve/solve.py` and `solver.sh` automate it.

## Flag

```
SecurinetsENIT{wh4twg_ur1_strips_t4b5_s0_d0t_t4b_d0t_b3c0m3z_d0t_d0t}
```

## Fix

- Never build paths by string-concatenating user input; use
  `new URL(encodeURIComponent(slug), base)` and verify the resulting
  `target.origin === location.origin` **and** that `target.pathname` is still
  under the intended prefix *after* URL parsing (the parser is the only source of
  truth — sanitizing the raw string is a differential waiting to happen).
- Give state-changing endpoints CSRF protection; don't rely on `SameSite` alone.
- Require the current password (and re-auth) to change a password.
- Keep the review bot egress-denied, and scope reported URLs to a route allowlist,
  not just "pathname === '/'".
