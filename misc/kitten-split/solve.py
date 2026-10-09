#!/usr/bin/env python3
"""
Kitten Split - solver (organizers only, do NOT ship to players).

Sprague-Grundy theorem:
  * the game is the sum of independent piles
  * each pile size n has a Grundy number
        g(n) = mex( {g(n-t) : t in 1,3,4}  U  {g(a) XOR g(n-a) : 1 <= a < n-a} )
    (a split creates two piles, worth the XOR of their values)
  * a position is winning for the player to move iff XOR of all g(pile) != 0
  * winning move: on some pile p, reach an option whose value is g(p) XOR total

Usage:
    python3 solve.py [host] [port]      # default localhost 1347
"""
import re
import socket
import sys
from functools import reduce
from operator import xor

TAKES = (1, 3, 4)
N = 400
G = [0] * (N + 1)
for n in range(1, N + 1):
    seen = {G[n - t] for t in TAKES if n - t >= 0}
    seen |= {G[a] ^ G[n - a] for a in range(1, (n + 1) // 2)}
    m = 0
    while m in seen:
        m += 1
    G[n] = m


def total(piles):
    return reduce(xor, (G[p] for p in piles), 0)


def best_move(piles):
    t = total(piles)
    for i, p in enumerate(piles):
        need = G[p] ^ t
        for x in TAKES:
            if x <= p and G[p - x] == need:
                return f"take {i + 1} {x}"
        for a in range(1, (p + 1) // 2):
            if G[a] ^ G[p - a] == need:
                return f"split {i + 1} {a}"
    return f"take {piles.index(max(piles)) + 1} 1"     # losing position (should not happen)


def main(host, port):
    s = socket.create_connection((host, port), timeout=15)
    buf, piles, games = "", [], 0
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        buf += chunk.decode(errors="replace")
        found = re.findall(r"Piles: ([\d ]+)\n", buf)
        if found:
            piles = list(map(int, found[-1].split()))
        if buf.endswith("(y/n)\n> "):
            games += 1
            s.sendall(b"y\n" if total(piles) else b"n\n")
            buf = ""
        elif buf.endswith("Your move:\n> "):
            s.sendall(best_move(piles).encode() + b"\n")
            buf = ""
        elif "She wins" in buf or "forfeit" in buf:
            print(f"lost in game {games}:", buf[-200:])
            return
    flag = re.search(r"SecurinetsENIT\{[^}]*\}", buf)
    print(flag.group(0) if flag else buf[-300:])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "localhost",
         int(sys.argv[2]) if len(sys.argv) > 2 else 1347)
