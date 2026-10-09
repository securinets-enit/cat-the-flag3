# Hints · 07 samesite-csrf

**Hint 1 (free):** Getting the flag means becoming `admin`. You can't read the
admin cookie (`HttpOnly`) and you don't know the password — but `POST
/password-reset` changes the *current* user's password with no old password and
no CSRF token. How do you make the admin's browser send that request?

**Hint 2:** The session cookie is `SameSite=Lax`, so a request forged from *your*
site (a classic CSRF form) won't carry it — cross-site is exactly what SameSite
blocks. What SameSite does **not** block is a request made by script running on
the challenge's *own* origin. You need XSS on this site, not a form on yours.

**Hint 3:** The "report a user profile" bot only opens `…/profile/<user>` links,
and profiles render your bio as raw HTML. But view the response headers: the
profile page ships `Content-Security-Policy: default-src 'self'`, so an inline
`<img onerror=…>` in your bio won't execute *there*. Where on this site is there
a sink with **no** CSP?

**Hint 4:** The home page's `/app.js` reads `location.hash` and drops it into
`innerHTML` — a DOM XSS with no CSP. You can't get the admin to a `/#…` link
directly (only profile links are accepted), so **pivot**: inject markup on your
profile that loads the home page for you — e.g. an `<iframe src="/#PAYLOAD">`.
The iframe is same-origin, so the payload runs in the admin's session.

**Hint 5:** Put this in your bio (URL-encode the fragment), report
`/profile/<you>`, then log in as admin with the password you set:
```html
<iframe src="/#<img src=x onerror=fetch('/password-reset',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'password=pwned'})>"></iframe>
```
Then `GET /admin`. (Trying to exfiltrate the flag directly won't work — the bot
has no outbound network; resetting the password is the way out.)
