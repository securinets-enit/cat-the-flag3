#!/usr/bin/env python3
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
ATTACHMENT = next(ROOT.joinpath("attachments").iterdir())
print(ATTACHMENT.read_bytes().split(b'PE\0\0', 1)[1].decode())
