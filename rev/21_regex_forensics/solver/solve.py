from pathlib import Path
import re
import sys

def solve(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    length = int(re.search(r"\.\{(\d+)\}", text).group(1))
    pieces = {}
    for match in re.finditer(r"\^\.\{(\d+)\}([A-Za-z0-9_]+)", text):
        pieces[int(match.group(1))] = match.group(2)
    result = ["?"] * length
    prefix = "SecurinetsENIT{"
    result[:len(prefix)] = prefix
    for offset, value in pieces.items():
        result[offset:offset + len(value)] = value
    result[-1] = "}"
    flag = "".join(result)
    if "?" in flag:
        raise ValueError("not all regex constraints were extracted")
    return flag

if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        Path(__file__).resolve().parents[1] / "attachment" / "validator.py"
    print(solve(target))
