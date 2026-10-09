#!/usr/bin/env python3
"""
Meowdle - solver (organizers only, do NOT ship to players).

Elimination solver that tolerates Mimi's lie: a candidate survives if its
expected colors differ from what the server said in at most ONE tile across
the whole round (a truthful round simply has zero mismatches).

Usage:
    python3 solve.py [host] [port]          # default localhost 1339
    python3 solve.py --sim [games]          # offline win-rate test, no server
"""
import os
import random
import re
import socket
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORDS = [w for w in open(os.path.join(HERE, "dist", "words.txt")).read().split() if len(w) == 5]

G, Y, B = "🟩", "🟨", "⬛"
OPENER = "tares"


def score(guess, secret):
    res = [B] * 5
    left = {}
    for i in range(5):
        if guess[i] == secret[i]:
            res[i] = G
        else:
            left[secret[i]] = left.get(secret[i], 0) + 1
    for i in range(5):
        if res[i] != G and left.get(guess[i], 0) > 0:
            res[i] = Y
            left[guess[i]] -= 1
    return res


def mismatches(word, history):
    total = 0
    for guess, tiles in history:
        total += sum(a != b for a, b in zip(score(guess, word), tiles))
        if total > 1:
            break
    return total


def candidates(history, allow_lie):
    scored = [(w, mismatches(w, history)) for w in WORDS]
    exact = [w for w, m in scored if m == 0]
    if not allow_lie:
        return exact
    # prefer words that fit perfectly, keep the "one lie" words as backup
    return exact + [w for w, m in scored if m == 1]


def pick(cands, history):
    if not history:
        return OPENER if OPENER in WORDS else cands[0]
    pool = cands[:60]
    if len(pool) <= 2:
        return pool[0]
    best, best_worst = pool[0], 10**9
    for g in pool:
        buckets = {}
        for s in pool:
            k = "".join(score(g, s))
            buckets[k] = buckets.get(k, 0) + 1
        worst = max(buckets.values())
        if worst < best_worst:
            best, best_worst = g, worst
    return best


def play_round(ask, allow_lie, max_guesses=6):
    history = []
    for _ in range(max_guesses):
        cands = candidates(history, allow_lie)
        if not cands:
            cands = candidates(history, True)
        guess = pick(cands, history)
        tiles = ask(guess)
        if tiles == [G] * 5:
            return True
        history.append((guess, tiles))
    return False


def simulate(games, max_guesses=7):
    rng = random.Random(1)
    wins = 0
    for _ in range(games):
        secret = rng.choice(WORDS)
        lie_at = rng.randrange(3)
        state = {"n": 0}

        def ask(guess):
            t = score(guess, secret)
            if t != [G] * 5 and state["n"] == lie_at:
                while True:
                    o = t[:]
                    i = rng.randrange(5)
                    o[i] = rng.choice([c for c in (G, Y, B) if c != t[i]])
                    if o != [G] * 5:
                        t = o
                        break
            state["n"] += 1
            return t

        wins += play_round(ask, allow_lie=True, max_guesses=max_guesses)
    print(f"lying rounds won with {max_guesses} guesses: {wins}/{games} ({100*wins/games:.2f}%)")


def remote(host, port):
    s = socket.create_connection((host, port), timeout=15)
    f = s.makefile("rwb", buffering=0)

    def read_until(marker):
        buf = b""
        while not buf.endswith(marker):
            c = f.read(1)
            if not c:
                raise EOFError(buf.decode(errors="replace"))
            buf += c
        return buf.decode()

    def ask(guess):
        f.write(guess.encode() + b"\n")
        line = read_until(b"\n")
        return [ch for ch in line if ch in (G, Y, B)][:5] if "Mimi doesn't" not in line else None

    def read_prompt():
        # the cat in the banner also contains "> ", so wait for a real round prompt
        text = ""
        while not re.search(r"Round \d+/\d+\n> $", text):
            text += read_until(b"> ")
        return text

    text = read_prompt()
    while True:
        m = re.search(r"Round (\d+)/(\d+)", text)
        rnd = int(m.group(1))
        # Lies only start late in the game; being tolerant from round 1 is also fine.
        ok = play_round(ask, allow_lie=True, max_guesses=7)
        if not ok:
            print("lost round", rnd)
            print(f.read().decode(errors="replace"))
            return
        try:
            text = read_prompt()
        except EOFError as e:
            out = str(e)
            flag = re.search(r"SecurinetsENIT\{[^}]*\}", out)
            print(flag.group(0) if flag else out)
            return


if __name__ == "__main__":
    if "--sim" in sys.argv:
        n = int(sys.argv[-1]) if sys.argv[-1].isdigit() else 500
        simulate(n)
    else:
        host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 1339
        remote(host, port)
