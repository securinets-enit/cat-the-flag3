#!/usr/bin/env python3
# Kitten Split - SecurinetsENIT Cat The Flag v3
# Author: r3t0x
#
# Impartial game against a perfect cat. On your turn, pick one pile and either
#   take 1, 3 or 4 fish from it, or
#   split it into two non-empty piles of DIFFERENT sizes.
# Whoever makes the last move wins. Win GAMES games in a row; before each game
# the player chooses who starts, so every game is winnable with perfect play.
# Intended: Sprague-Grundy theorem (the Grundy values of this game have no
# simple pattern, they must be computed).

import os
import random
import select
import sys
from functools import reduce
from operator import xor

HERE = os.path.dirname(os.path.abspath(__file__))
GAMES = int(os.environ.get("GAMES", 10))
MAX_PILE = int(os.environ.get("MAX_PILE", 60))
MOVE_TIME = float(os.environ.get("MOVE_TIME", 5))
TAKES = (1, 3, 4)

with open(os.path.join(HERE, "flag.txt")) as f:
    FLAG = f.read().strip()

BANNER = rf"""
   /\_/\    KITTEN SPLIT
  ( o.o )   Mimi has new rules, and she has never lost with them.
   > ^ <    Beat her {GAMES} times in a row.

On your turn, choose ONE pile and either:
   take 1, 3 or 4 fish from it            ->  take <pile> <amount>
   split it into two piles of DIFFERENT   ->  split <pile> <size of one part>
   sizes (both non-empty)
Whoever makes the last move wins.
"""


def build_grundy(n):
    g = [0] * (n + 1)
    for size in range(1, n + 1):
        seen = {g[size - t] for t in TAKES if size - t >= 0}
        for a in range(1, (size + 1) // 2):
            seen.add(g[a] ^ g[size - a])
        m = 0
        while m in seen:
            m += 1
        g[size] = m
    return g


G = build_grundy(MAX_PILE)


def options(size):
    for t in TAKES:
        if size - t >= 0:
            yield ("take", t, [size - t] if size - t else [])
    for a in range(1, (size + 1) // 2):
        yield ("split", a, [a, size - a])


def total(piles):
    return reduce(xor, (G[p] for p in piles), 0)


def winning_move(piles):
    t = total(piles)
    if t == 0:
        return None
    for i, p in enumerate(piles):
        need = G[p] ^ t
        for kind, x, result in options(p):
            if reduce(xor, (G[r] for r in result), 0) == need:
                return i, kind, x
    return None


def apply(piles, i, kind, x):
    p = piles[i]
    rest = piles[:i] + piles[i + 1:]
    if kind == "take":
        new = [p - x] if p - x else []
    else:
        new = [x, p - x]
    return rest[:i] + new + rest[i:]


def legal(piles, i, kind, x):
    if not 0 <= i < len(piles):
        return False
    p = piles[i]
    if kind == "take":
        return x in TAKES and x <= p
    if kind == "split":
        return 1 <= x < p and x != p - x
    return False


def say(msg=""):
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


def ask(prompt):
    sys.stdout.write(prompt + "\n> ")
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [], [], MOVE_TIME)
    if not ready:
        say("\nToo slow. Mimi curls up and falls asleep on the fish.")
        sys.exit(0)
    line = sys.stdin.readline()
    if not line:
        sys.exit(0)
    return line.strip()


def mimi_move(piles, rng):
    move = winning_move(piles)
    if move:
        return move
    # losing anyway: grab as much as possible so games don't drag on
    i = max(range(len(piles)), key=lambda k: piles[k])
    for t in sorted(TAKES, reverse=True):
        if t <= piles[i]:
            return i, "take", t
    return i, "take", 1


def play(game, rng):
    piles = [rng.randint(1, MAX_PILE) for _ in range(rng.randint(3, 6))]
    say(f"Game {game}/{GAMES}")
    say("Piles: " + " ".join(map(str, piles)))
    answer = ask("Do you want to go first? (y/n)").lower()
    if answer not in ("y", "n"):
        say("Mimi only understands y or n.")
        return False
    player_turn = answer == "y"

    while piles:
        if player_turn:
            parts = ask("Your move:").split()
            try:
                kind, i, x = parts[0].lower(), int(parts[1]) - 1, int(parts[2])
            except (IndexError, ValueError):
                say("Mimi doesn't understand that move. She wins by forfeit.")
                return False
            if not legal(piles, i, kind, x):
                say("Illegal move. Mimi wins by forfeit.")
                return False
        else:
            i, kind, x = mimi_move(piles, rng)
            if kind == "take":
                say(f"Mimi takes {x} fish from pile {i + 1}.")
            else:
                say(f"Mimi splits pile {i + 1} into {x} and {piles[i] - x}.")
        piles = apply(piles, i, kind, x)
        if not piles:
            if player_turn:
                say("You made the last move! Mimi's ears flatten.\n")
                return True
            say("Mimi made the last move. She wins and licks her paw.")
            return False
        say("Piles: " + " ".join(map(str, piles)))
        player_turn = not player_turn
    return False


def main():
    rng = random.SystemRandom()
    say(BANNER)
    for game in range(1, GAMES + 1):
        if not play(game, rng):
            return
    say("Mimi bows. For the first time, she has been outplayed:")
    say(FLAG)


if __name__ == "__main__":
    main()
