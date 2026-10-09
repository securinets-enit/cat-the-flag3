#!/usr/bin/env python3
# Cat Stairs - SecurinetsENIT Cat The Flag v3
# Author: r3t0x
#
# 40 rounds: "Mimi can jump these sizes, the roof is at step N, how many
# different jump sequences land exactly on N?" (mod 1e9+7), 3 seconds each.
# The stairs grow from ~10 steps to ~1e18, so only an O(k^3 log N) solution
# survives the last stage.

import math
import os
import random
import select
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MOD = 1_000_000_007
ROUNDS = int(os.environ.get("ROUNDS", 40))
ROUND_TIME = float(os.environ.get("ROUND_TIME", 3))

with open(os.path.join(HERE, "flag.txt")) as f:
    FLAG = f.read().strip()

BANNER = r"""
   /\_/\    CAT STAIRS
  ( o.o )   Mimi wants to reach the roof.
   > ^ <    Tell her how many ways she can climb. Quickly.
"""


# ---------- the math (same idea players have to find) ----------

def mat_mul(A, B):
    n = len(A)
    Bt = list(zip(*B))
    return [[sum(a * b for a, b in zip(row, col)) % MOD for col in Bt] for row in A]


def mat_pow(M, p):
    n = len(M)
    R = [[int(i == j) for j in range(n)] for i in range(n)]
    while p:
        if p & 1:
            R = mat_mul(R, M)
        M = mat_mul(M, M)
        p >>= 1
    return R


def ways(n, jumps):
    k = max(jumps)
    M = [[0] * k for _ in range(k)]
    for s in jumps:
        M[0][s - 1] = 1
    for i in range(1, k):
        M[i][i - 1] = 1
    return mat_pow(M, n)[0][0]


# ---------- rounds ----------

def make_round(rnd, rng):
    """Stage 1: tiny stairs, simple jumps.  Stage 2: any jumps, thousands of steps.
    Stage 3: up to a million steps.  Stage 4: up to 1e18 steps."""
    while True:
        if rnd <= 10:
            jumps = rng.choice([[1, 2], [1, 2, 3], [1, 3], [2, 3], [1, 2, 4]])
            n = rng.randint(5, 30)
        elif rnd <= 20:
            jumps = sorted(rng.sample(range(1, 10), rng.randint(2, 4)))
            n = rng.randint(1_000, 100_000)
        elif rnd <= 30:
            jumps = sorted(rng.sample(range(1, 11), rng.randint(2, 4)))
            n = rng.randint(200_000, 1_000_000)
        else:
            jumps = sorted(rng.sample(range(1, 13), rng.randint(2, 4)))
            n = rng.randint(10**15, 10**18)
        if math.gcd(*jumps) == 1:          # every big enough step is reachable
            return jumps, n


def say(msg=""):
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


def read_answer(timeout):
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if not ready:
        return None
    return sys.stdin.readline()


def main():
    rng = random.SystemRandom()
    say(BANNER)
    for rnd in range(1, ROUNDS + 1):
        jumps, n = make_round(rnd, rng)
        expected = ways(n, jumps)
        say(f"Round {rnd}/{ROUNDS}")
        say("Mimi can jump: " + " ".join(map(str, jumps)))
        say(f"Steps to the roof: {n}")
        sys.stdout.write(f"Answer (mod {MOD}):\n> ")
        sys.stdout.flush()

        line = read_answer(ROUND_TIME)
        if line is None:
            say("\nToo slow. Mimi got bored and took the elevator.")
            return
        if not line:
            return
        try:
            answer = int(line.strip())
        except ValueError:
            say("That's not a number. Mimi is confused.")
            return
        if answer % MOD != expected:
            say("Wrong! Mimi slips down the stairs.")
            return
        say("Correct!\n")

    say("Mimi reached the roof and looks at the moon. She leaves you a gift:")
    say(FLAG)


if __name__ == "__main__":
    main()
