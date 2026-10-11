from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLAG = (ROOT / "flag" / "flag.txt").read_text(encoding="utf-8").strip()
OUT = ROOT / "attachment" / "maze.wat"

def main():
    values = [ord(char) ^ ((index * 0x2D + 0x17) & 0xFF)
              for index, char in enumerate(FLAG)]
    bytes_text = " ".join(f"i32.const {value}" for value in values)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(f'''(module
  (memory (export "memory") 1)
  (func (export "unlock") (result i32)
    {bytes_text}
    i32.const 0
    i32.const 0
    i32.store8
    i32.const 1)
  (data (i32.const 128) "WASM-MAZE")
)
''', encoding="utf-8")
    print(f"wrote {OUT}")

if __name__ == "__main__":
    main()
