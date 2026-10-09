#!/usr/bin/env python3
# Cat Jail v3 - Paws Off - SecurinetsENIT Cat The Flag v3
# Author: r3t0x

import sys

BANNER = r"""
   /\_/\    CAT JAIL v3: PAWS OFF
  ( -_- )   Mimi has had enough of your tricks.
   > ^ <    Send your code, then a line with EOF.
"""

BANNED_CHARS = set("()'\"")
BANNED_WORDS = ["exec", "eval", "import", "input", "breakpoint", "help", "compile"]
MAX_LINES = 15
MAX_LEN = 600


def hiss():
    print("Mimi hisses and knocks your code off the table.")


def main():
    print(BANNER)
    sys.stdout.write(">>> ")
    sys.stdout.flush()

    lines = []
    for _ in range(MAX_LINES + 1):
        line = sys.stdin.readline()
        if not line or line.strip() == "EOF":
            break
        lines.append(line.rstrip("\n"))
    code = "\n".join(lines)

    if not code.strip() or len(code) > MAX_LEN or len(lines) > MAX_LINES:
        hiss()
        return
    if not code.isascii() or BANNED_CHARS & set(code):
        hiss()
        return
    if any(word in code.lower() for word in BANNED_WORDS):
        hiss()
        return

    try:
        exec(code, {"__name__": "__main__"})
    except BaseException:
        print("Mimi stares at you. Nothing happens.")


if __name__ == "__main__":
    main()
