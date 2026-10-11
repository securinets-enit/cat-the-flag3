from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLAG = (ROOT / "flag" / "flag.txt").read_text(encoding="utf-8").strip()
OUT = ROOT / "attachment" / "checker.py"

def main():
    constraints = "\n".join(
        f"    assert ((b[{i}] ^ {i + 0x31}) + b[{i + 1}]) & 255 == "
        f"{((ord(FLAG[i]) ^ (i + 0x31)) + ord(FLAG[i + 1])) & 255}"
        for i in range(len(FLAG) - 1)
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(f'''import sys

def check(candidate):
    b = candidate.encode("ascii")
    if len(b) != {len(FLAG)}:
        return False
{constraints}
    return b.startswith(b"SecurinetsENIT{{") and b.endswith(b"}}")

if __name__ == "__main__":
    print("accepted" if check(sys.argv[1]) else "rejected")
''', encoding="utf-8")
    print(f"wrote {OUT}")

if __name__ == "__main__":
    main()
