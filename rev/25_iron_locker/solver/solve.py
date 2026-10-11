from pathlib import Path
import struct
import sys


def solve(path: Path) -> str:
    data = path.read_bytes()
    if data[:4] != b"ILKR":
        raise ValueError("missing leaked record magic")
    version, kind, length = struct.unpack("<BBH", data[4:8])
    if version != 1 or kind != 7:
        raise ValueError("unexpected recovery record")
    encoded = data[8:8 + length]
    if len(encoded) != length:
        raise ValueError("truncated recovery record")
    return bytes(
        value ^ ((index * 0x37 + 0x5D) & 0xFF)
        for index, value in enumerate(encoded)
    ).decode("ascii")


if __name__ == "__main__":
    print(solve(Path(sys.argv[1])))
