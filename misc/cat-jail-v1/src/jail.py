#!/usr/bin/env python3
# Cat Jail v1 - SecurinetsENIT Cat The Flag v3
# Author: r3t0x

BANNER = r"""
   /\_/\    Welcome to Mimi's Cat Jail
  ( o.o )   Mimi runs your Python... but she HATES some words.
   > ^ <    Her treats are hidden in /flag.txt

  Forbidden: import os system open flag exec eval subprocess
             breakpoint help input
"""

BANNED = [
    "import", "os", "system", "open", "flag", "exec", "eval",
    "subprocess", "breakpoint", "help", "input",
]

MAX_LEN = 300


def main():
    print(BANNER)
    try:
        code = input(">>> ")
    except EOFError:
        return

    if len(code) > MAX_LEN:
        print("Mimi fell asleep halfway through. Keep it under 300 characters.")
        return

    for word in BANNED:
        if word in code.lower():
            print(f"Mimi hisses: '{word}' is forbidden!")
            return

    try:
        print(eval(code))
    except Exception as e:
        print("Mimi is confused:", type(e).__name__)


if __name__ == "__main__":
    main()
