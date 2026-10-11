from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
FLAG = (ROOT / "flag" / "flag.txt").read_text(encoding="utf-8").strip()
OUT = ROOT / "attachment" / "validator.py"

def main():
    expected = json.dumps(FLAG)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(f'''import re
import sys

# Generated constraints. The useful information is in the lookaheads.
PATTERN = r"^(?=^.{{{len(FLAG)}}}$)(?=^SecurinetsENIT\\\\{{)(?=.*\\\\}}$)" \\
          r"(?=^.{{15}}r3g3x)(?=^.{{20}}_)(?=^.{{21}}constraints)" \
          r"(?=^.{{32}}_are_)" \
          r"(?=^.{{36}}_)(?=^.{{37}}code$)" \\
          r"[A-Za-z0-9_{{}}]+$"

def main():
    if len(sys.argv) != 2:
        print("usage: python validator.py <candidate>")
        return 2
    print("accepted" if re.fullmatch(PATTERN, sys.argv[1]) else "rejected")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
''', encoding="utf-8")
    print(f"wrote {OUT}")

if __name__ == "__main__":
    main()
