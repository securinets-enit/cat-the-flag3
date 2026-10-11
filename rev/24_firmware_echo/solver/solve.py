from pathlib import Path
import struct
import sys
import zlib

def solve(path: Path) -> str:
    data = path.read_bytes()
    if data[:4] != b"FIRM":
        raise ValueError("not firmware")
    version, arch, reserved, length = struct.unpack("<BBHI", data[4:12])
    expected = struct.unpack("<I", data[12:16])[0]
    payload = data[16:16 + length]
    if zlib.crc32(payload) & 0xffffffff != expected:
        raise ValueError("firmware CRC mismatch")
    if payload[:4] != b"FWS1":
        raise ValueError("missing filesystem marker")
    table_len = struct.unpack("<I", payload[4:8])[0]
    table = payload[8:8 + table_len]
    records = [table[i:i + 96] for i in range(0, len(table), 96)]
    config = next(record for record in records if record.startswith(b"config.bin"))
    encoded = config.split(b"MODEL=ENIT-GW\x00", 1)[1].rstrip(b"\x00")
    return bytes(byte ^ ((i * 0x41 + 0x23) & 0xff)
                 for i, byte in enumerate(encoded)).decode("ascii")

if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        Path(__file__).resolve().parents[1] / "attachment" / "router.fw"
    print(solve(target))
