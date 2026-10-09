#!/usr/bin/env python3
# Liar's Treat - SecurinetsENIT Cat The Flag v3
# Author: r3t0x
#
# Each round Mimi hides a treat in box 0..65535. The player asks up to 26
# "parity questions" (send a mask m, Mimi answers whether popcount(box & m) is
# odd) and Mimi lies on up to 2 of them. Then the player names the box.
# Solvable with a binary linear code that has 16 data bits, length <= 26 and
# minimum distance 5 (e.g. the [31,21,5] BCH code shortened to [26,16,5]).

import os
import random
import select
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROUNDS = int(os.environ.get("ROUNDS", 10))
QUESTIONS = int(os.environ.get("QUESTIONS", 26))
LIES = int(os.environ.get("LIES", 2))
ROUND_TIME = float(os.environ.get("ROUND_TIME", 30))
BOXES = 1 << 16

with open(os.path.join(HERE, "flag.txt")) as f:
    FLAG = f.read().strip()

BANNER = rf"""
   /\_/\    LIAR'S TREAT
  ( o.o )   Every round, Mimi hides a treat in one of {BOXES} boxes (0 to {BOXES - 1}).
   > ^ <    Find it {ROUNDS} times in a row.

How to ask:  send a number m (1 to {BOXES - 1}).
             Mimi looks at the bits of the box number that are also set in m,
             and answers "odd" if there is an odd number of 1s, "even" otherwise.
How to win:  send   guess <box number>

You may ask at most {QUESTIONS} questions per round.
Mimi is a cat. She will lie to you, up to {LIES} times per round.
"""


def say(msg=""):
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


def read_line(deadline_left):
    sys.stdout.write("> ")
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [], [], max(0.0, deadline_left))
    if not ready:
        return None
    line = sys.stdin.readline()
    if not line:
        sys.exit(0)
    return line.strip()


def play(rnd, rng):
    import time
    box = rng.randrange(BOXES)
    lie_at = set(rng.sample(range(QUESTIONS), LIES))
    asked = 0
    deadline = time.time() + ROUND_TIME
    say(f"Round {rnd}/{ROUNDS}")

    while True:
        line = read_line(deadline - time.time())
        if line is None:
            say("\nToo slow. Mimi ate the treat herself.")
            return False
        if line.lower().startswith("guess"):
            try:
                guess = int(line.split()[1], 0)
            except (IndexError, ValueError):
                say("Mimi doesn't understand that guess.")
                return False
            if guess == box:
                say("Found it! Mimi glares at you.\n")
                return True
            say(f"Empty box. The treat was in box {box}. Mimi purrs smugly.")
            return False

        if asked >= QUESTIONS:
            say("No more questions. Make your guess.")
            continue
        try:
            mask = int(line, 0)
            if not 1 <= mask < BOXES:
                raise ValueError
        except ValueError:
            say(f"Ask with a number between 1 and {BOXES - 1}.")
            continue

        odd = bin(box & mask).count("1") % 2 == 1
        if asked in lie_at:
            odd = not odd
        asked += 1
        say("odd" if odd else "even")


def main():
    rng = random.SystemRandom()
    say(BANNER)
    for rnd in range(1, ROUNDS + 1):
        if not play(rnd, rng):
            return
    say("Mimi can't fool you. She hands over her most precious treat:")
    say(FLAG)


if __name__ == "__main__":
    main()
