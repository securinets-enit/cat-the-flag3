#!/usr/bin/env python3
"""Play every running threat-intel asker with its answer key over TCP and check that the flag comes back.

    python3 tools/smoke_test.py [host]     (default 127.0.0.1; ports follow ORDER in questions.py: 5010, 5011, ...)
"""

import socket
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from questions import CHALLENGES

ROOT = Path(__file__).resolve().parent.parent
host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
failed = 0
for port, ch in enumerate(CHALLENGES, 5010):
    flag = (ROOT / ch["dir"] / "flag.txt").read_text().strip()
    try:
        s = socket.create_connection((host, port), timeout=10)
        s.sendall(("\n".join(q[1][0] for q in ch["questions"]) + "\n").encode())
        s.shutdown(socket.SHUT_WR)
        data = b""
        while chunk := s.recv(65536):
            data += chunk
        ok = flag in data.decode(errors="replace")
    except OSError as e:
        ok, data = False, str(e).encode()
    failed += not ok
    print(f"{'PASS' if ok else 'FAIL'}  {port}  {ch['dir']}" + ("" if ok else f"  ({data[-120:]!r})"))
print(f"\n{len(CHALLENGES) - failed}/{len(CHALLENGES)} passed")
sys.exit(1 if failed else 0)
