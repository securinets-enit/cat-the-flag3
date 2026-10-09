#!/usr/bin/env python3
# Cat Jail v2 - SecurinetsENIT Cat The Flag v3
# Author: r3t0x

BANNER = r"""
   /\_/\
  ( -.- )   Mimi is back, and she remembers everything you did last time.
   > ^ <    She is in a very bad mood.
"""

BANNED_WORDS = [
    "import", "os", "system", "open", "flag", "exec", "eval",
    "subprocess", "breakpoint", "help", "input", "read",
]
BANNED_CHARS = set("'\"._0123456789")

MAX_LEN = 2000


def hiss():
    print("Mimi hisses at you and walks away.")


def main():
    print(BANNER)
    try:
        code = input(">>> ")
    except EOFError:
        return

    if len(code) > MAX_LEN:
        print("Mimi fell asleep before you finished.")
        return

    if not code.isascii() or BANNED_CHARS & set(code):
        hiss()
        return

    lowered = code.lower()
    if any(word in lowered for word in BANNED_WORDS):
        hiss()
        return

    try:
        print(eval(code))
    except Exception:
        print("Mimi tilts her head. Nothing happens.")


if __name__ == "__main__":
    main()
