#!/usr/bin/env python3
"""
solve.py - decrypts the seeded_dreams challenge (organizers only, do NOT ship to players).

Usage:
    python3 solve.py chall.json [YYYY-MM-DD]

The date defaults to 2001-09-11, the answer to the checkpoint_saved riddle.
If chall.json carries an explicit "seed" field (older variant), that is used instead.
"""
import sys
import json
import random
import hashlib

if __name__ == "__main__":
    with open(sys.argv[1] if len(sys.argv) > 1 else "chall.json") as f:
        chall = json.load(f)

    if "seed" in chall:
        seed = chall["seed"]
    else:
        date = sys.argv[2] if len(sys.argv) > 2 else "2001-09-11"
        seed = int(hashlib.sha256(date.encode()).hexdigest()[:8], 16)

    cipher = bytes.fromhex(chall["cipher_hex"])
    r = random.Random(seed)
    mask = bytes(r.randrange(256) for _ in range(len(cipher)))
    plain = bytes(c ^ m for c, m in zip(cipher, mask))

    print(plain.decode())
