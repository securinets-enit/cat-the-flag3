#!/usr/bin/env python3
"""
Copycat - generator (organizers only, do NOT ship to players).

Draws a pixel-art scene (Mimi on a sofa), saves it as dist/mimi.png, then
saves dist/copycat.png: the same picture where every pixel under the flag
text has its red value changed by exactly 1. The two images look identical;
their difference spells the flag.

Usage:
    python3 gen.py
Requires: Pillow (with FreeType, for the built-in font)
"""
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 900, 560
PX = 10  # size of one "pixel-art" pixel

CAT = [
    "..X..........X..",
    ".XGX........XGX.",
    ".XGGX......XGGX.",
    ".XGGGXXXXXXGGGX.",
    "XGGGGGGGGGGGGGGX",
    "XGGLLGGGGGGLLGGX",
    "XGGLKGGGGGGLKGGX",
    "XGGGGGGPPGGGGGGX",
    "XGGWGGGGGGGGWGGX",
    ".XGGGGWGGWGGGGX.",
    "..XXGGGGGGGGXX..",
    "....XXXXXXXX....",
]
CAT_COLORS = {"X": (35, 35, 35), "G": (120, 120, 128), "L": (210, 230, 120), "K": (20, 20, 20),
              "P": (235, 140, 160), "W": (230, 230, 230)}


def block(d, x, y, w, h, color):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=color)


def scene(rng):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)

    # wall with a soft vertical gradient and some texture
    for y in range(H):
        c = 196 - y // 12
        d.line([(0, y), (W, y)], fill=(c, c - 30, c - 60))
    for _ in range(2500):
        x, y = rng.randrange(W), rng.randrange(330)
        r, g, b = img.getpixel((x, y))
        img.putpixel((x, y), (max(0, r - 8), max(0, g - 8), max(0, b - 8)))

    # window with night sky and moon
    block(d, 600, 50, 220, 170, (60, 45, 30))
    block(d, 612, 62, 196, 146, (25, 30, 70))
    for _ in range(40):
        d.point((rng.randrange(612, 808), rng.randrange(62, 208)), fill=(240, 240, 200))
    d.ellipse([740, 80, 780, 120], fill=(245, 240, 200))
    block(d, 707, 62, 6, 146, (60, 45, 30))
    block(d, 612, 132, 196, 6, (60, 45, 30))

    # floor
    for y in range(400, H):
        c = 120 - (y - 400) // 6
        d.line([(0, y), (W, y)], fill=(c, c - 40, c - 70))
    for x in range(0, W, 60):
        d.line([(x, 400), (x - 40, H)], fill=(80, 50, 30))

    # sofa
    block(d, 70, 230, 470, 120, (150, 40, 50))     # back
    block(d, 40, 300, 530, 90, (170, 50, 60))      # seat
    block(d, 30, 270, 60, 120, (130, 35, 45))      # left arm
    block(d, 520, 270, 60, 120, (130, 35, 45))     # right arm
    block(d, 60, 390, 30, 25, (60, 35, 25))
    block(d, 520, 390, 30, 25, (60, 35, 25))
    block(d, 330, 255, 140, 60, (210, 180, 90))    # cushion

    # plant
    block(d, 760, 330, 70, 80, (170, 90, 50))
    for i in range(9):
        x = 765 + i * 7
        d.line([(795, 330), (x - 25 + i * 3, 250 + (i % 3) * 15)], fill=(40, 120 + i * 8, 50), width=6)

    # Mimi, pixel art, curled on the sofa
    ox, oy = 150, 190
    for r, row in enumerate(CAT):
        for c, ch in enumerate(row):
            if ch in CAT_COLORS:
                block(d, ox + c * PX, oy + r * PX, PX, PX, CAT_COLORS[ch])
    block(d, ox + 16 * PX, oy + 9 * PX, 6 * PX, PX, (120, 120, 128))   # tail
    block(d, ox + 21 * PX, oy + 7 * PX, PX, 3 * PX, (120, 120, 128))
    return img


def main():
    with open(os.path.join(HERE, "flag.txt")) as f:
        flag = f.read().strip()

    rng = random.Random(1337)
    original = scene(rng)

    # Mask of the flag text, written across the middle of the picture
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    font = ImageFont.load_default(size=34)
    tw = md.textlength(flag, font=font)
    md.text(((W - tw) / 2, 150), flag, font=font, fill=255)

    twin = original.copy()
    src, m = twin.load(), mask.load()
    for y in range(H):
        for x in range(W):
            if m[x, y] > 127:
                r, g, b = src[x, y]
                src[x, y] = (r + 1 if r < 255 else r - 1, g, b)

    os.makedirs(os.path.join(HERE, "dist"), exist_ok=True)
    original.save(os.path.join(HERE, "dist", "mimi.png"), optimize=True)
    twin.save(os.path.join(HERE, "dist", "copycat.png"), optimize=True)
    print("wrote dist/mimi.png and dist/copycat.png")


if __name__ == "__main__":
    main()
