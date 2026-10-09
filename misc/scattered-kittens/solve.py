#!/usr/bin/env python3
"""
Scattered Kittens - solver (organizers only, do NOT ship to players).

Split the GIF into frames, keep the darkest value of every pixel across all
frames (stacking them), cut off the kitten strip and scan the QR code.

Usage:
    python3 solve.py [dist/kittens.gif]
Requires: opencv-python, Pillow
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageSequence

path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist", "kittens.gif")
gif = Image.open(path)

stack = None
for frame in ImageSequence.Iterator(gif):
    gray = np.array(frame.convert("L"))
    stack = gray if stack is None else np.minimum(stack, gray)

w = stack.shape[1]
qr = stack[:w, :w]                       # the QR is the square on top; the kitten strip is below
cv2.imwrite(os.path.join(os.path.dirname(os.path.abspath(path)), "..", "stacked.png"), qr) if "--save" in sys.argv else None
text, _, _ = cv2.QRCodeDetector().detectAndDecode(qr)
print(text or "QR not decoded")
