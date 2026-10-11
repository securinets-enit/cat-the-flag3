# Notes Vault v3 — hard CSPT

A note-taking portal with a hardened, client-side "slug" checker and a backend WAF.
The flag lives in the admin vault. You cannot read it as a normal user, and the
admin's password is random. The only way in is to make the **admin's own browser**
issue a request you cannot issue yourself — same origin, so SameSite is no help.

`GET /` renders the notes page. It reads `file` from the URL **fragment** and
builds the API URL in `public/app.js`:

```js
const target = new URL('/api/v1/notes/' + file, location.origin);
fetch(target.href, { credentials: 'same-origin' });
```

The fragment is attacker-controlled and is never sent to the server. The page also
autosaves a `draft` value from the fragment back to that same URL with `POST`.

Before building the URL, the slug passes a sanitizer:

```js
if (slug.includes('..')) return false;
if (slug.includes('\\')) return false;
if (/%2e|%2f|%5c|%25/i.test(slug)) return false;
```

And the backend WAF (on `/api`) rejects `..`, `%2f`/`%5c` and `%25` in the raw
and once-decoded URL.

## Goal

Change the admin's password using the admin bot's session, then log in as admin
and read `/api/v1/admin/flag`.

## Hints

**Hint 1 (free):** The obvious `../` and its encoded forms (`%2e%2e`, `%2f`,
`%5c`, double-encoding) are blocked twice — once in the browser and once in the
WAF. But *the browser and the sanitizer do not parse the string the same way*.

**Hint 2:** `slug` is validated as a plain JavaScript string, but it is later fed
to `new URL()`, which parses it according to the WHATWG URL Standard. What does
that spec do to ASCII **tab (0x09)**, **LF (0x0A)** and **CR (0x0D)** characters,
wherever they appear in the URL?

**Hint 3:** The tab has to be a real character when it reaches `new URL()`, but the
fragment must survive `new URL(raw)` on the server (`/report`) and the browser's
address bar. Percent-encoding in the fragment is only decoded by code that reads
the fragment — i.e. `new URLSearchParams(location.hash.slice(1))`. Which encoding
(`%09`) decodes to a tab exactly there?

**Hint 4:** You need to walk from `/api/v1/notes/` to a *different* `/api/v1/...`
path: the password endpoint. The notes page is viewable after registering; the
profile page shows the endpoint that changes the password. The autosave sends
`draft` as the request body, so you can choose the new password.

**Hint 5:** Report this link to the admin bot (bot reviews `/` links only):

```
http://HOST:3002/#file=.%09./profile/password&draft=password%3Dpwned
```

Then log in as `admin` / `pwned`.
