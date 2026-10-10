#!/usr/bin/env python3
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
ATTACHMENT = next(ROOT.joinpath("attachments").iterdir())
print(bytes(b ^ 0x5A for b in ATTACHMENT.read_bytes()).decode())
