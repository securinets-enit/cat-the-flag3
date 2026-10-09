#!/usr/bin/env python3
# Mimi's Vending Machine - SecurinetsENIT Cat The Flag v3
# Author: r3t0x

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "flag.txt")) as f:
    FLAG = f.read().strip()

MAX_ACTIONS = 30

ITEMS = {
    "1": ("Tuna can", 10),
    "2": ("Catnip", 25),
    "3": ("Laser pointer", 40),
    "4": ("GOLDEN FLAG", 1000),
}

BANNER = r"""
   /\_/\    MIMI'S VENDING MACHINE
  ( o.o )   Only the finest products for discerning cats.
   > ^ <
"""


def say(msg=""):
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


def ask(prompt):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    line = sys.stdin.readline()
    if not line:
        sys.exit(0)
    return line.strip()


def menu(wallet):
    say(f"\nYour wallet: {wallet} coins\n")
    for key, (name, price) in ITEMS.items():
        say(f"  {key}. {name:<14} {price:>5} coins")
    say("  5. Leave")


def main():
    wallet = 50
    say(BANNER)
    for _ in range(MAX_ACTIONS):
        menu(wallet)
        choice = ask("\nChoose item: ")
        if choice == "5":
            say("Mimi waves goodbye with her tail.")
            return
        if choice not in ITEMS:
            say("Mimi doesn't sell that.")
            continue
        name, price = ITEMS[choice]

        try:
            quantity = int(ask("How many? "))
        except ValueError:
            say("Mimi only counts in whole numbers.")
            continue
        if quantity == 0:
            say("You bought nothing. Mimi is not impressed.")
            continue

        total = price * quantity
        if total > wallet:
            say(f"That costs {total} coins. You only have {wallet}. Mimi hisses.")
            continue

        wallet -= total
        say(f"You bought {quantity} x {name} for {total} coins.")

        if name == "GOLDEN FLAG" and quantity >= 1:
            say("\nThe machine rumbles and drops a shiny golden flag:")
            say(FLAG)
            return

    say("\nMimi is tired of you. The machine shuts down.")


if __name__ == "__main__":
    main()
