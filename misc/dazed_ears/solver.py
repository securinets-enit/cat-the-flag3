#!/usr/bin/env python3
"""Recover the covert mode bytes from the Silent Beacon capture."""

from __future__ import annotations

import struct
from pathlib import Path


ASM = b"\x1a\xcf\xfc\x1d"
APID_HK_NOMINAL = 100


def parse_packets(raw: bytes) -> list[tuple[int, int]]:
    records: list[tuple[int, int]] = []
    search_from = 0

    while True:
        asm_at = raw.find(ASM, search_from)
        if asm_at < 0:
            break

        header_at = asm_at + len(ASM)
        header = raw[header_at : header_at + 6]
        if len(header) != 6:
            break

        word0, word1, word2 = struct.unpack(">HHH", header)
        apid = word0 & 0x07FF
        sequence_count = word1 & 0x3FFF
        data_length = word2 + 1
        payload_at = header_at + 6
        payload = raw[payload_at : payload_at + data_length]

        if apid == APID_HK_NOMINAL and len(payload) >= 1:
            records.append((sequence_count, payload[0]))

        search_from = asm_at + 1

    return records


def main() -> None:
    raw = (Path(__file__).parent / "capture.bin").read_bytes()
    records = sorted(parse_packets(raw), key=lambda record: record[0])
    covert = bytes(mode for _, mode in records if mode > 7)
    message = covert.decode("ascii")
    print(f"SecurinetsENIT{{{message}}}")


if __name__ == "__main__":
    main()
