#!/usr/bin/env python3
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
ATTACHMENT = next(ROOT.joinpath("attachments").iterdir())
import base64
print(base64.b64decode(ATTACHMENT.read_bytes()[4:]).decode())
