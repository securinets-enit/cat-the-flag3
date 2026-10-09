#!/usr/bin/env python3
"""Generate the deterministic binary attachment for Silent Beacon."""

from __future__ import annotations

import random
import struct
from pathlib import Path


ASM = b"\x1a\xcf\xfc\x1d"
COVERT = b"h0us3k33p1ng_4n0m4ly"
OUT = Path(__file__).parent


def packet(apid: int, sequence_count: int, payload: bytes) -> bytes:
    word0 = apid & 0x07FF
    word1 = 0xC000 | (sequence_count & 0x3FFF)
    word2 = len(payload) - 1
    return ASM + struct.pack(">HHH", word0, word1, word2) + payload


def housekeeping(mode: int, sequence_count: int) -> bytes:
    payload = bytes([mode]) + struct.pack(">Hh", 5120, 2430) + bytes(9)
    return packet(100, sequence_count, payload)


def main() -> None:
    rng = random.Random(0x5EED)
    frames: list[tuple[int, bytes]] = []
    covert_index = 0

    for sequence_count in range(89):
        if sequence_count % 7 == 0:
            payload = f"station heartbeat seq={sequence_count}".encode()
            frames.append((sequence_count, packet(50, sequence_count, payload)))
        elif sequence_count % 5 == 0:
            frames.append((sequence_count, packet(200, sequence_count, bytes([0xA5]) * 8)))
        else:
            if covert_index < len(COVERT):
                mode = COVERT[covert_index]
                covert_index += 1
            else:
                mode = sequence_count % 8
            frames.append((sequence_count, housekeeping(mode, sequence_count)))

    # Place frames in capture order with deterministic noise and deliberately
    # out-of-order sequence counts. The solver must sort HK packets.
    rng.shuffle(frames)
    capture = bytearray()
    for sequence_count, frame in frames:
        capture.extend(rng.randbytes(rng.randint(2, 11)))
        capture.extend(frame)
        if sequence_count % 9 == 0:
            capture.extend(rng.randbytes(3))

    (OUT / "capture.bin").write_bytes(capture)
    ids = ["# sequence_count, apid"]
    ids.extend(f"{sequence_count:02d}, {apid}" for sequence_count, apid in (
        (sequence_count, 50 if sequence_count % 7 == 0 else 200 if sequence_count % 5 == 0 else 100)
        for sequence_count in range(89)
    ))
    (OUT / "packet_ids.txt").write_text("\n".join(ids) + "\n", encoding="ascii")


if __name__ == "__main__":
    main()
