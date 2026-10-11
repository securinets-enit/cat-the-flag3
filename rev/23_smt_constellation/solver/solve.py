from pathlib import Path
import re
import sys

def solve(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    equations = re.findall(
        r"\(\(b\[(\d+)\] \^ (\d+)\) \+ b\[(\d+)\]\) & 255 == (\d+)",
        text,
    )
    length = int(re.search(r"len\(b\) != (\d+)", text).group(1))
    prefix = list(b"SecurinetsENIT{")
    suffix = ord("}")
    values = [None] * length
    for index, value in enumerate(prefix):
        values[index] = value
    values[-1] = suffix
    # The chain can be solved backwards from the known closing brace.
    for left, xor_key, right, target in reversed(equations):
        i, j = int(left), int(right)
        if values[j] is None:
            continue
        candidates = [x for x in range(256)
                      if (((x ^ int(xor_key)) + values[j]) & 255)
                      == int(target)]
        printable = [x for x in candidates if 32 <= x <= 126]
        if len(printable) != 1:
            raise ValueError(f"constraint at {i} is not uniquely printable")
        values[i] = printable[0]
    if any(value is None for value in values):
        raise ValueError("underconstrained checker; use Z3 directly")
    return bytes(values).decode()

if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        Path(__file__).resolve().parents[1] / "attachment" / "checker.py"
    print(solve(target))
