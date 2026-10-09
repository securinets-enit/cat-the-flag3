#!/usr/bin/env python3
"""
Scattered Kittens - generator (organizers only, do NOT ship to players).

Builds dist/kittens.gif: a fast animation where a pixel kitten runs across the
bottom, and each frame flashes only ONE of the 9 pieces (3x3) of a QR code
holding the flag. Every frame is drawn on a fresh white canvas, so no single
frame (and no viewer) ever shows the whole code.

Usage:
    python3 gen.py
Requires: opencv-python, Pillow
"""
import os
import random

import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))

MODULE = 12          # pixels per QR module
BORDER = 48          # white quiet zone around the QR
STRIP = 90           # running-kitten strip under the QR
GRID = 3             # 3x3 = 9 pieces, one per kitten life
FRAME_MS = 20        # 20 ms per frame: far too fast to see

KITTEN = [
    ".X........X.",
    ".XX......XX.",
    ".XXXXXXXXXX.",
    "XXXXXXXXXXXX",
    "XGGGGGGGGGGX",
    "XGLGGXXGLGGX",
    "XXGGXXXXGGXX",
    "XXXXXPPXXXXX",
    "XXXXMXXMXXXX",
    ".XXXXMMXXXX.",
    "..XXXXXXXX..",
]
COLORS = {"X": (40, 40, 40), "G": (90, 200, 70), "L": (255, 255, 255), "P": (255, 140, 170), "M": (120, 120, 120)}


def qr_image(text: str) -> np.ndarray:
    q = cv2.QRCodeEncoder.create().encode(text)
    q = cv2.resize(q, (q.shape[1] * MODULE, q.shape[0] * MODULE), interpolation=cv2.INTER_NEAREST)
    return cv2.copyMakeBorder(q, BORDER, BORDER, BORDER, BORDER, cv2.BORDER_CONSTANT, value=255)


def draw_kitten(img: Image.Image, x: int, y: int, px: int = 5):
    for r, row in enumerate(KITTEN):
        for c, ch in enumerate(row):
            if ch in COLORS:
                for dy in range(px):
                    for dx in range(px):
                        img.putpixel((x + c * px + dx, y + r * px + dy), COLORS[ch])


def main():
    with open(os.path.join(HERE, "flag.txt")) as f:
        flag = f.read().strip()

    qr = qr_image(flag)
    size = qr.shape[0]
    width, height = size, size + STRIP

    # Cut the QR area (inside the quiet zone) into a 3x3 grid of pieces
    inner = size - 2 * BORDER
    cuts = [BORDER + round(i * inner / GRID) for i in range(GRID + 1)]
    pieces = [(cuts[c], cuts[r], cuts[c + 1], cuts[r + 1]) for r in range(GRID) for c in range(GRID)]

    rng = random.Random(9)
    order = pieces[:] * 3              # each piece shows up 3 times
    rng.shuffle(order)

    frames = []
    steps = len(order) * 2             # empty frames in between keep it chaotic
    kitten_w = len(KITTEN[0]) * 5
    for i in range(steps):
        frame = Image.new("RGB", (width, height), (255, 255, 255))
        if i % 2 == 0:
            x0, y0, x1, y1 = order[i // 2]
            piece = Image.fromarray(qr[y0:y1, x0:x1]).convert("RGB")
            frame.paste(piece, (x0, y0))
        kx = int((width + kitten_w) * i / steps) - kitten_w
        hop = 6 if i % 4 < 2 else 0
        if -kitten_w < kx < width:
            draw_kitten(frame, max(0, min(kx, width - kitten_w)), size + 15 - hop)
        frames.append(frame.convert("P", palette=Image.ADAPTIVE, colors=16))

    out = os.path.join(HERE, "dist", "kittens.gif")
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=FRAME_MS,
                   loop=0, disposal=2, optimize=False)
    print(f"wrote {out}: {len(frames)} frames, {width}x{height}")


if __name__ == "__main__":
    main()
