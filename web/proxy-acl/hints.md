# Hints · 05 proxy-acl

**Hint 1 (free):** The flag is at `/secret/flag.txt` but that path returns 403.
The block is enforced by the reverse proxy, not the app.

**Hint 2:** There's a second location, `/files`, that serves downloads. Look very
carefully at whether it has a trailing slash. `alias` + a prefix location without
a trailing slash is a classic footgun.

**Hint 3:** `/files` maps to `/var/www/protected/files/`. What does `/files../`
resolve to on disk? Does the `/secret` ACL even match a URL that starts with
`/files`?

**Hint 4:** `GET /files../secret/flag.txt` (send it raw — don't let your client
collapse the `../`). In curl: `curl --path-as-is`.
