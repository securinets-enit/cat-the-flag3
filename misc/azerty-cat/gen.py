#!/usr/bin/env python3
"""
AZERTY Cat - generator (organizers only, do NOT ship to players).

Simulates someone typing on a French AZERTY keyboard while the OS layout is
set to US QWERTY: every key is pressed where it sits on the AZERTY keyboard,
but the computer outputs what that same physical key means on QWERTY.

Usage:
    python3 gen.py            # writes dist/message.txt from flag.txt
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# What the person meant (AZERTY label) -> what the screen shows (US QWERTY, same physical key)
AZERTY_TO_QWERTY = {
    # number row, unshifted / shifted
    "&": "1", "é": "2", '"': "3", "'": "4", "(": "5", "-": "6", "è": "7", "_": "8", "ç": "9", "à": "0", ")": "-", "=": "=",
    "1": "!", "2": "@", "3": "#", "4": "$", "5": "%", "6": "^", "7": "&", "8": "*", "9": "(", "0": ")", "°": "_", "+": "+",
    # top row
    "a": "q", "z": "w", "A": "Q", "Z": "W",
    # home row
    "q": "a", "m": ";", "ù": "'", "Q": "A", "M": ":", "%": '"',
    # bottom row
    "w": "z", "W": "Z", ",": "m", ";": ",", ":": ".", "!": "/", "?": "M", ".": "<", "/": ">",
}
# Everything else (e, r, t, y, s, d, ..., space, newline, braces) lands on the same character.

MESSAGE = (
    "Salam ! J'ai laisse mon PC allume et ma chatte Mimi a marche sur le clavier... "
    "Elle a change la langue du clavier en anglais sans que je remarque.\n"
    "Bref, voici le flag que tu m'as demande hier, je l'ai tape a la main :\n"
    "{flag}\n"
    "Miaou, a demain au CTF !\n"
)


def azerty_typed_on_qwerty(text: str) -> str:
    return "".join(AZERTY_TO_QWERTY.get(ch, ch) for ch in text)


def main():
    with open(os.path.join(HERE, "flag.txt")) as f:
        flag = f.read().strip()
    garbled = azerty_typed_on_qwerty(MESSAGE.format(flag=flag))
    os.makedirs(os.path.join(HERE, "dist"), exist_ok=True)
    with open(os.path.join(HERE, "dist", "message.txt"), "w") as f:
        f.write(garbled)
    print(garbled)


if __name__ == "__main__":
    main()
