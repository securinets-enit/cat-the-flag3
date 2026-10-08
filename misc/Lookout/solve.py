#!/usr/bin/env python3
"""
solve.py — decrypts a seeded-PRNG XOR challenge instance (internal, for
grading/writeup use — do NOT ship to players).

Usage:
    python3 solve.py chall.json
"""
import sys
import json
import random

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        chall = json.load(f)

    cipher = bytes.fromhex(chall["cipher_hex"])
    r = random.Random(chall["seed"])
    mask = bytes(r.randrange(256) for _ in range(len(cipher)))
    plain = bytes(c ^ m for c, m in zip(cipher, mask))

    print(plain.decode())
