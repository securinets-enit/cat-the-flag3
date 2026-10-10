#!/usr/bin/env python3
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
ATTACHMENT = next(ROOT.joinpath("attachments").iterdir())
import re
print(re.findall(r'SecurinetsENIT\{[^}]+\}', ATTACHMENT.read_text())[0])
