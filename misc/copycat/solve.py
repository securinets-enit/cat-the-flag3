#!/usr/bin/env python3
"""
Copycat - solver (organizers only, do NOT ship to players).

Subtracts the two images pixel by pixel and paints every changed pixel white.
The flag is written in the result (diff.png).

Usage:
    python3 solve.py [mimi.png copycat.png]
"""
import os
import sys

from PIL import Image, ImageChops

here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
a_path, b_path = sys.argv[1:3] if len(sys.argv) >= 3 else (os.path.join(here, "mimi.png"), os.path.join(here, "copycat.png"))

a = Image.open(a_path).convert("RGB")
b = Image.open(b_path).convert("RGB")

diff = ImageChops.difference(a, b)                          # |a - b| for every pixel
# amplify BEFORE converting to grey: a change of 1 in red alone would round to 0 in greyscale
mask = diff.point(lambda v: 255 if v else 0).convert("L").point(lambda v: 255 if v else 0)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diff.png")
mask.save(out)
print(f"changed pixels: {mask.histogram()[255]}  ->  open {out}")
