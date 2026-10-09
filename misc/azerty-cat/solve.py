#!/usr/bin/env python3
"""
AZERTY Cat - solver (organizers only, do NOT ship to players).

Reverses the layout mix-up: for every character on screen (US QWERTY), find the
AZERTY label of the same physical key.

Usage:
    python3 solve.py [dist/message.txt]
"""
import os
import re
import sys

QWERTY_TO_AZERTY = {
    "1": "&", "2": "é", "3": '"', "4": "'", "5": "(", "6": "-", "7": "è", "8": "_", "9": "ç", "0": "à", "-": ")", "=": "=",
    "!": "1", "@": "2", "#": "3", "$": "4", "%": "5", "^": "6", "&": "7", "*": "8", "(": "9", ")": "0", "_": "°", "+": "+",
    "q": "a", "w": "z", "Q": "A", "W": "Z",
    "a": "q", ";": "m", "'": "ù", "A": "Q", ":": "M", '"': "%",
    "z": "w", "Z": "W", "m": ",", ",": ";", ".": ":", "/": "!", "M": "?", "<": ".", ">": "/",
}


def fix(text: str) -> str:
    return "".join(QWERTY_TO_AZERTY.get(ch, ch) for ch in text)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist", "message.txt")
    with open(path) as f:
        decoded = fix(f.read())
    print(decoded)
    m = re.search(r"SecurinetsENIT\{[^}]*\}", decoded)
    if m:
        print("FLAG:", m.group(0))
