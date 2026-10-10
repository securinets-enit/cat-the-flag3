#!/usr/bin/env python3
from pathlib import Path
import dis
from importlib.machinery import SourcelessFileLoader

ROOT = Path(__file__).resolve().parents[1]
ATTACHMENT = ROOT / "attachments" / "challenge.pyc"
module = SourcelessFileLoader("challenge", str(ATTACHMENT)).load_module()
dis.dis(module.reveal)
print(module.reveal())
