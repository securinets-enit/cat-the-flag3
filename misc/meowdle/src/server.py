#!/usr/bin/env python3
# Meowdle - SecurinetsENIT Cat The Flag v3
# Author: r3t0x
#
# Wordle over netcat: win ROUNDS games in a row, MAX_GUESSES guesses each,
# within TIME_LIMIT seconds in total. From round LIE_FROM, Mimi lies once per
# round: one tile of one of the first three feedback rows has the wrong color.
# Set LIE_FROM=0 to disable the lies.

import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))

ROUNDS = int(os.environ.get("ROUNDS", 30))
MAX_GUESSES = int(os.environ.get("MAX_GUESSES", 7))
TIME_LIMIT = float(os.environ.get("TIME_LIMIT", 60))
LIE_FROM = int(os.environ.get("LIE_FROM", 21))

GREEN, YELLOW, BLACK = "🟩", "🟨", "⬛"

BANNER = r"""
   /\_/\    MEOWDLE
  ( o.o )   Mimi bets you can't win {rounds} in a row.
   > ^ <    You have {limit} seconds. Good luck, human.
"""


def load(name):
    with open(os.path.join(HERE, name)) as f:
        return f.read()


WORDS = [w for w in load("words.txt").split() if len(w) == 5]
WORDSET = set(WORDS)
FLAG = load("flag.txt").strip()


def score(guess: str, secret: str) -> list:
    """Standard Wordle colors, duplicates handled: greens first, then yellows."""
    res = [BLACK] * 5
    left = {}
    for i in range(5):
        if guess[i] == secret[i]:
            res[i] = GREEN
        else:
            left[secret[i]] = left.get(secret[i], 0) + 1
    for i in range(5):
        if res[i] != GREEN and left.get(guess[i], 0) > 0:
            res[i] = YELLOW
            left[guess[i]] -= 1
    return res


def lie(tiles: list, rng: random.Random) -> list:
    """Flip exactly one tile to a different color, never producing all green."""
    while True:
        out = tiles[:]
        i = rng.randrange(5)
        out[i] = rng.choice([c for c in (GREEN, YELLOW, BLACK) if c != tiles[i]])
        if out != [GREEN] * 5:
            return out


def say(msg=""):
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


def main():
    rng = random.SystemRandom()
    say(BANNER.format(rounds=ROUNDS, limit=int(TIME_LIMIT)))
    deadline = time.time() + TIME_LIMIT

    for rnd in range(1, ROUNDS + 1):
        secret = rng.choice(WORDS)
        lie_at = rng.randrange(3) if LIE_FROM and rnd >= LIE_FROM else -1
        say(f"Round {rnd}/{ROUNDS}")
        guesses = 0
        while True:
            sys.stdout.write("> ")
            sys.stdout.flush()
            line = sys.stdin.readline()
            if not line:
                return
            if time.time() > deadline:
                say("Too slow. Mimi fell asleep on the keyboard.")
                return
            guess = line.strip().lower()
            if guess not in WORDSET:
                say("Mimi doesn't know that word.")
                continue
            tiles = score(guess, secret)
            if tiles == [GREEN] * 5:
                say("".join(tiles) + "  Mimi is annoyed.")
                break
            if guesses == lie_at:
                tiles = lie(tiles, rng)
            say("".join(tiles))
            guesses += 1
            if guesses >= MAX_GUESSES:
                say(f"Out of guesses. The word was '{secret}'. Mimi wins.")
                return
        say()

    say("Mimi knocks your coffee off the table in anger.")
    say(FLAG)


if __name__ == "__main__":
    main()
