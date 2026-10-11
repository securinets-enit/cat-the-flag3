from pathlib import Path
import re
import sys

def solve(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    function = text.split("(func", 1)[1].split("(data", 1)[0]
    values = [int(x) for x in re.findall(r"i32\.const (\d+)", function)]
    # The final two constants are the store address and return value.
    encoded = values[:-3]
    return "".join(chr(value ^ ((index * 0x2D + 0x17) & 0xFF))
                   for index, value in enumerate(encoded))

if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        Path(__file__).resolve().parents[1] / "attachment" / "maze.wat"
    print(solve(target))
