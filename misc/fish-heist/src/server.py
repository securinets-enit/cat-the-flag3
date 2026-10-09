#!/usr/bin/env python3
# Fish Heist - SecurinetsENIT Cat The Flag v3
# Author: r3t0x
#
# Nim against a perfect cat. Win GAMES games in a row.
# Games 1..MISERE_FROM-1: whoever takes the last fish wins (normal Nim).
# Games MISERE_FROM..GAMES: whoever takes the last fish loses (misere Nim).
# Before each game the player chooses who starts, so every game is winnable.

import os
import random
import select
import sys
from functools import reduce
from operator import xor

HERE = os.path.dirname(os.path.abspath(__file__))
GAMES = int(os.environ.get("GAMES", 20))
MISERE_FROM = int(os.environ.get("MISERE_FROM", 16))
MOVE_TIME = float(os.environ.get("MOVE_TIME", 10))

with open(os.path.join(HERE, "flag.txt")) as f:
    FLAG = f.read().strip()

BANNER = r"""
   /\_/\    FISH HEIST
  ( o.o )   Take turns. Take as many fish as you want from ONE pile.
   > ^ <    Beat Mimi 20 times in a row and she'll share her treasure.

Moves are written as:  <pile number> <how many fish>     e.g.  2 3
"""


def say(msg=""):
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


def ask(prompt):
    sys.stdout.write(prompt + "\n> ")
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [], [], MOVE_TIME)
    if not ready:
        say("\nToo slow. Mimi ate all the fish while you were thinking.")
        sys.exit(0)
    line = sys.stdin.readline()
    if not line:
        sys.exit(0)
    return line.strip()


# ---------- game theory ----------

def mover_wins(piles, misere):
    """True if the player about to move can force a win."""
    if misere and all(p <= 1 for p in piles):
        return sum(piles) % 2 == 0
    return reduce(xor, piles, 0) != 0


def winning_move(piles, misere):
    """(index, take) leading to a position that is lost for the opponent, or None."""
    big = [i for i, p in enumerate(piles) if p >= 2]
    if misere and len(big) <= 1:
        ones = sum(1 for p in piles if p == 1)
        if not big:                              # only single fish left
            if ones % 2 == 0:
                return next(i for i, p in enumerate(piles) if p == 1), 1
            return None
        i = big[0]                               # one big pile: leave an odd number of single fish
        keep = 1 if ones % 2 == 0 else 0
        return i, piles[i] - keep
    total = reduce(xor, piles, 0)
    if total == 0:
        return None
    for i, p in enumerate(piles):
        target = p ^ total
        if target < p:
            return i, p - target
    return None


def mimi_move(piles, misere, rng):
    move = winning_move(piles, misere)
    if move:
        return move
    i = rng.choice([i for i, p in enumerate(piles) if p > 0])   # losing: stall with a random move
    return i, rng.randint(1, piles[i])


# ---------- rounds ----------

def make_piles(game, rng):
    if game <= 5:
        return [rng.randint(1, 9) for _ in range(rng.randint(2, 3))]
    if game < MISERE_FROM:
        return [rng.randint(1, 1000) for _ in range(rng.randint(4, 8))]
    return [rng.randint(1, 60) for _ in range(rng.randint(3, 6))]


def show(piles):
    say("Piles: " + " ".join(map(str, piles)))


def play(game, rng):
    misere = game >= MISERE_FROM
    piles = make_piles(game, rng)
    rule = "LAST FISH LOSES" if misere else "LAST FISH WINS"
    say(f"Game {game}/{GAMES}  ({rule})")
    if game == MISERE_FROM:
        say("Mimi is bored. From now on, whoever takes the last fish LOSES.")
    show(piles)

    answer = ask("Do you want to go first? (y/n)").lower()
    if answer not in ("y", "n"):
        say("Mimi only understands y or n.")
        return False
    player_turn = answer == "y"

    while True:
        if player_turn:
            move = ask("Your move (pile amount):").split()
            try:
                i, take = int(move[0]) - 1, int(move[1])
                if not (0 <= i < len(piles)) or not (1 <= take <= piles[i]):
                    raise ValueError
            except (ValueError, IndexError):
                say("Illegal move. Mimi wins by forfeit.")
                return False
            piles[i] -= take
        else:
            i, take = mimi_move(piles, misere, rng)
            piles[i] -= take
            say(f"Mimi takes {take} fish from pile {i + 1}.")

        if sum(piles) == 0:
            took_last = "you" if player_turn else "mimi"
            player_won = (took_last == "you") != misere
            if player_won:
                say("You win this one. Mimi's tail twitches.\n")
            else:
                say("Mimi wins. She smiles and licks her paw.")
            return player_won

        show(piles)
        player_turn = not player_turn


def main():
    rng = random.SystemRandom()
    say(BANNER)
    for game in range(1, GAMES + 1):
        if not play(game, rng):
            return
    say("Mimi can't believe it. She drops her treasure at your feet:")
    say(FLAG)


if __name__ == "__main__":
    main()
