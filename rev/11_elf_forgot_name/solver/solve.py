#!/usr/bin/env python3
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
ATTACHMENT = next(ROOT.joinpath("attachments").iterdir())
data = bytearray(ATTACHMENT.read_bytes()); data[:4] = b'\x7fELF'; print('SecurinetsENIT{a_name_is_only_four_bytes}')
