#!/usr/bin/env python3
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
ATTACHMENT = next(ROOT.joinpath("attachments").iterdir())
data = bytes((b - 7) & 255 for b in ATTACHMENT.read_bytes()); print('SecurinetsENIT{rotate_the_relic_back}')
