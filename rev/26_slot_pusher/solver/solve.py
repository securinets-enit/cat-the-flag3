from __future__ import annotations

import io
import subprocess
import sys
from pathlib import Path


FLAG = b"SecurinetsENIT{slot_cycles_keep_old_truth}"


def encode(value: bytes) -> bytes:
    return bytes(byte ^ ((index * 0x29 + 0x61) & 0xFF)
                 for index, byte in enumerate(value))


def build_payload() -> bytes:
    encoded = encode(FLAG)
    stream = io.BytesIO()
    cursor = 0
    slots: list[int | None] = [None] * len(encoded)

    def command(value: str) -> None:
        stream.write(value.encode("ascii") + b"\n")

    def push(byte: int) -> None:
        nonlocal cursor
        command("1")
        stream.write(bytes([byte]))
        stream.write(b"\n")
        slots[cursor] = byte
        cursor = (cursor + 1) % len(encoded)

    def rewind() -> None:
        nonlocal cursor
        command("2")
        cursor = (cursor + 4) % len(encoded)

    # The attachment consumes one encoded byte per cycle. A push advances by
    # one and a rewind advances by four, giving a coprime stride of five.
    for byte in encoded:
        push(byte)
        rewind()
    while cursor != 12:
        rewind()
    command("4")
    return stream.getvalue()


def main() -> int:
    payload = build_payload()
    if len(sys.argv) == 1:
        sys.stdout.buffer.write(payload)
        return 0
    target = Path(sys.argv[1])
    result = subprocess.run(
        [sys.executable, str(target)],
        input=payload,
        stdout=subprocess.PIPE,
        check=False,
    )
    sys.stdout.buffer.write(result.stdout)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
