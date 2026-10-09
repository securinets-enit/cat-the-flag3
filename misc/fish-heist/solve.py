#!/usr/bin/env python3
"""
Fish Heist - solver (organizers only, do NOT ship to players).

Nim strategy:
  * normal games (last fish wins): leave the XOR of all piles equal to 0
  * misere games (last fish loses): same, except when at most one pile has
    2+ fish: then leave an ODD number of single-fish piles
  * go first only if the starting position is winning for the mover

Usage:
    python3 solve.py [host] [port]      # default localhost 1341
"""
import re
import socket
import sys
from functools import reduce
from operator import xor


def mover_wins(piles, misere):
    if misere and all(p <= 1 for p in piles):
        return sum(piles) % 2 == 0
    return reduce(xor, piles, 0) != 0


def best_move(piles, misere):
    big = [i for i, p in enumerate(piles) if p >= 2]
    if misere and len(big) <= 1:
        ones = sum(1 for p in piles if p == 1)
        if not big:
            return next(i for i, p in enumerate(piles) if p == 1), 1
        i = big[0]
        keep = 1 if ones % 2 == 0 else 0           # leave an odd number of single fish
        return i, piles[i] - keep
    total = reduce(xor, piles, 0)
    for i, p in enumerate(piles):
        if (p ^ total) < p:
            return i, p - (p ^ total)                # make the XOR zero
    i = max(range(len(piles)), key=lambda k: piles[k])
    return i, 1                                      # losing anyway (shouldn't happen)


def main(host, port):
    s = socket.create_connection((host, port), timeout=15)
    buf = ""
    misere = False
    piles = []
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        buf += chunk.decode(errors="replace")
        for m in re.finditer(r"Game (\d+)/\d+\s+\((LAST FISH (?:WINS|LOSES))\)", buf):
            misere = m.group(2).endswith("LOSES")
        all_piles = re.findall(r"Piles: ([\d ]+)\n", buf)
        if all_piles:
            piles = list(map(int, all_piles[-1].split()))
        if buf.endswith("(y/n)\n> "):
            s.sendall(b"y\n" if mover_wins(piles, misere) else b"n\n")
            buf = ""
        elif buf.endswith("(pile amount):\n> "):
            i, take = best_move(piles, misere)
            s.sendall(f"{i + 1} {take}\n".encode())
            buf = ""
        elif "Mimi wins" in buf:
            print("lost a game:", buf[-200:])
            return
    flag = re.search(r"SecurinetsENIT\{[^}]*\}", buf)
    print(flag.group(0) if flag else buf[-300:])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "localhost",
         int(sys.argv[2]) if len(sys.argv) > 2 else 1341)
