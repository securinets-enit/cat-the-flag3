#!/usr/bin/env python3
# Admin Mimi - SecurinetsENIT Cat The Flag v3
# Author: r3t0x

import os
import secrets
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "flag.txt")) as f:
    FLAG = f.read().strip()

MAX_ACTIONS = 40

BANNER = r"""
   /\_/\    CATBOOK
  ( o.o )   The social network for cats (and their humans).
   > ^ <
"""

PHOTOS = [
    r"""
     /\_/\
    ( ^.^ )   Mimi after dinner
     > ~ <
""",
    r"""
     |\__/,|   (`\
   _.|o o  |_   ) )
 -(((---(((--------   Mimi on the windowsill
""",
    r"""
      /\_/\
     ( o o )   Mimi judging you
     ==_Y_==
       `-'
""",
]


def say(msg=""):
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


def ask(prompt):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    line = sys.stdin.readline()
    if not line:
        sys.exit(0)
    return line.rstrip("\n")


def main():
    # name -> password. The real admin's password is random and never shown.
    users = {"admin": secrets.token_hex(16)}
    session = None

    say(BANNER)
    for _ in range(MAX_ACTIONS):
        if session is None:
            say("\n1. Register\n2. Login\n3. Leave")
            choice = ask("> ").strip()
            if choice == "1":
                name = ask("Username: ")
                if name == "admin":
                    say("This username is reserved.")
                    continue
                if not name.strip() or name in users:
                    say("Pick another username.")
                    continue
                users[name] = ask("Password: ")
                say(f"Welcome to Catbook, {name}!")
            elif choice == "2":
                name = ask("Username: ")
                password = ask("Password: ")
                if users.get(name) != password:
                    say("Wrong username or password.")
                    continue
                session = name.strip().lower()      # "clean up" the name for display
                crown = " 👑" if session == "admin" else ""
                say(f"Welcome back, {session}{crown}")
            elif choice == "3":
                say("Bye! Mimi waves her tail.")
                return
            else:
                say("Mimi doesn't understand.")
        else:
            say("\n1. Look at cat photos\n2. Admin panel\n3. Logout")
            choice = ask("> ").strip()
            if choice == "1":
                for p in PHOTOS:
                    say(p)
            elif choice == "2":
                if session == "admin":
                    say("Admin panel. Secret note from Mimi:")
                    say(FLAG)
                    return
                say("Only admin can open the admin panel. Mimi hisses.")
            elif choice == "3":
                session = None
                say("Logged out.")
            else:
                say("Mimi doesn't understand.")

    say("\nMimi is tired. Catbook is closing.")


if __name__ == "__main__":
    main()
