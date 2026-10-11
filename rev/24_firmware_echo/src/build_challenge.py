from pathlib import Path
import struct
import zlib

ROOT = Path(__file__).resolve().parents[1]
FLAG = (ROOT / "flag" / "flag.txt").read_text(encoding="utf-8").strip()
OUT = ROOT / "attachment" / "router.fw"

def main():
    config = b"MODEL=ENIT-GW\x00" + bytes(
        char ^ ((index * 0x41 + 0x23) & 0xff)
        for index, char in enumerate(FLAG.encode("ascii"))
    )
    entries = [b"README\x00" + b"offline", b"config.bin\x00" + config]
    table = b"".join(entry.ljust(96, b"\x00") for entry in reversed(entries))
    payload = b"FWS1" + struct.pack("<I", len(table)) + table
    image = b"FIRM" + struct.pack("<BBHI", 1, 0x42, 0, len(payload)) + \
        struct.pack("<I", zlib.crc32(payload) & 0xffffffff) + payload
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(image)
    print(f"wrote {OUT} ({len(image)} bytes)")

if __name__ == "__main__":
    main()
