import re
import sys

PATTERN = r"^(?=^.{42}$)(?=^SecurinetsENIT\\{)(?=.*\\}$)" \
          r"(?=^.{15}r3g3x)(?=^.{20}_)(?=^.{21}constraints)"           r"(?=^.{32}_are_)"           r"(?=^.{36}_)(?=^.{37}code$)" \
          r"[A-Za-z0-9_{}]+$"

def main():
    if len(sys.argv) != 2:
        print("usage: python validator.py <candidate>")
        return 2
    print("accepted" if re.fullmatch(PATTERN, sys.argv[1]) else "rejected")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
