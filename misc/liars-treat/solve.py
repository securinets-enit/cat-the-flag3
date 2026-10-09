#!/usr/bin/env python3
"""
Liar's Treat - solver (organizers only, do NOT ship to players).

1. Build a binary linear code with 16 data bits, 26 check bits total and
   minimum distance 5: the [31,21,5] BCH code (generator g = m1(x)*m3(x) over
   GF(2^5)) shortened to [26,16,5]. Distance 5 => any 2 wrong answers can be
   corrected.
2. Each codeword bit is a parity of some data bits -> one mask per question.
3. Ask the 26 masks, collect the (possibly lied) answers as a 26-bit word.
4. Decode: the box whose codeword differs from the answers in <= 2 places.
   (Brute force over all 65536 boxes, vectorised with numpy.)

Usage:
    python3 solve.py [host] [port]      # default localhost 1343
    python3 solve.py --check            # verify the code's minimum distance
"""
import re
import socket
import sys

import numpy as np

PRIM = 0b100101          # x^5 + x^2 + 1, primitive over GF(2)


def gf32():
    exp, x = [0] * 62, 1
    for i in range(31):
        exp[i] = x
        x <<= 1
        if x & 32:
            x ^= PRIM
    for i in range(31, 62):
        exp[i] = exp[i - 31]
    log = {exp[i]: i for i in range(31)}
    return exp, log


def minimal_poly(power):
    exp, log = gf32()
    mul = lambda a, b: 0 if not a or not b else exp[log[a] + log[b]]
    roots, r = [], power % 31
    while r not in roots:
        roots.append(r)
        r = r * 2 % 31
    poly = [1]
    for r in roots:                       # multiply by (x + alpha^r)
        new = [0] * (len(poly) + 1)
        for i, c in enumerate(poly):
            new[i + 1] ^= c
            new[i] ^= mul(c, exp[r])
        poly = new
    return sum(c << i for i, c in enumerate(poly))


def pmul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        b >>= 1
    return r


def pmod(a, m):
    d = m.bit_length() - 1
    while a and a.bit_length() - 1 >= d:
        a ^= m << (a.bit_length() - 1 - d)
    return a


G = pmul(minimal_poly(1), minimal_poly(3))       # degree 10 generator of BCH(31,21,5)


def encode(msg):                                  # systematic, shortened to 26 bits
    s = msg << 10
    return s | pmod(s, G)


MASKS = []
for j in range(26):
    MASKS.append(sum(1 << i for i in range(16) if (encode(1 << i) >> j) & 1))

ALL = np.arange(1 << 16, dtype=np.uint32)
CODEWORDS = np.zeros(1 << 16, dtype=np.uint32)
for j, m in enumerate(MASKS):
    CODEWORDS |= ((np.bitwise_count(ALL & m) & 1).astype(np.uint32) << j)


def decode(answers):
    dist = np.bitwise_count(CODEWORDS ^ np.uint32(answers))
    best = int(np.argmin(dist))
    assert dist[best] <= 2
    return best


def check():
    print("min distance:", int(np.bitwise_count(CODEWORDS[1:]).min()), "(>= 5 corrects 2 lies)")
    import random
    rng = random.Random(1)
    for _ in range(2000):
        box = rng.randrange(1 << 16)
        word = int(CODEWORDS[box])
        for j in rng.sample(range(26), 2):
            word ^= 1 << j
        assert decode(word) == box
    print("2000 random boxes with 2 random lies decoded correctly")


def remote(host, port):
    s = socket.create_connection((host, port), timeout=40)
    buf = ""

    def until(marker):
        nonlocal buf
        while marker not in buf:
            chunk = s.recv(4096)
            if not chunk:
                return None
            buf += chunk.decode(errors="replace")
        out, _, buf = buf.partition(marker)
        return out

    while True:
        head = until("> ")
        if head is None:
            break
        m = re.search(r"Round (\d+)/(\d+)", head)
        if not m:
            continue
        answers = 0
        for j, mask in enumerate(MASKS):
            if j:
                until("> ")
            s.sendall(f"{mask}\n".encode())
            line = until("\n").strip()
            while line not in ("odd", "even"):
                line = until("\n").strip()
            if line == "odd":
                answers |= 1 << j
        until("> ")
        box = decode(answers)
        s.sendall(f"guess {box}\n".encode())
        print(f"round {m.group(1)}: box {box}")

    flag = re.search(r"SecurinetsENIT\{[^}]*\}", buf)
    print(flag.group(0) if flag else buf[-300:])


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    else:
        remote(sys.argv[1] if len(sys.argv) > 1 else "localhost",
               int(sys.argv[2]) if len(sys.argv) > 2 else 1343)
