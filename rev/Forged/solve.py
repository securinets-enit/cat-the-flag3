#!/usr/bin/env python3
"""
solve.py - author reference: replay the Forged pipeline in pure Python and
verify a candidate key reproduces the target code, independently of solve.c.

Reads parameters from generated.h + answer.txt (author files), or pass a key to
mimic a player who extracted MAGIC / &reveal / suffixes / POS from the binary.

    python3 solve.py                     # read generated.h + answer.txt, verify KEY
    python3 solve.py --key <32hex>       # verify a specific key
"""
import argparse, hashlib, re, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))

def parse_generated():
    txt = open(os.path.join(HERE, "generated.h")).read()
    magic = int(re.search(r"#define MAGIC 0x([0-9a-fA-F]+)u", txt).group(1), 16)
    pos = [int(x) for x in re.search(r"POS\[3\]\s*=\s*\{(\d+),(\d+),(\d+)\}", txt).groups()]
    suf = []
    for row in re.findall(r"\{((?:0x[0-9a-fA-F]+,?){8})\}", txt):
        suf.append(bytes(int(b, 16) for b in re.findall(r"0x[0-9a-fA-F]+", row)))
    return magic, pos, suf[:4]

def parse_answer():
    d = {}
    for ln in open(os.path.join(HERE, "answer.txt")):
        if "=" in ln:
            k, v = ln.strip().split("=", 1)
            d[k] = v
    return d

def target_code(magic, reveal_addr):
    return (b"\xBF" + struct.pack("<I", magic) +
            b"\xB8" + struct.pack("<I", reveal_addr) + b"\xFF\xE0")

def forge(key, suffixes, pos):
    out = bytearray()
    for i in range(4):
        dig = hashlib.md5(key[4*i:4*i+4] + suffixes[i]).digest()
        out += bytes(dig[p] for p in pos)
    return bytes(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", help="32 hex digits; default: KEY from answer.txt")
    a = ap.parse_args()

    magic, pos, suffixes = parse_generated()
    ans = parse_answer()
    reveal_addr = int(ans["reveal"], 16)
    key_hex = a.key or ans["KEY"]
    key = bytes.fromhex(key_hex)

    print(f"MAGIC       = 0x{magic:08x}")
    print(f"&reveal     = 0x{reveal_addr:x}")
    print(f"POS         = {pos}")
    for i, s in enumerate(suffixes):
        print(f"suffix[{i}]   = {s.hex()}")
    print(f"key         = {key_hex}")

    tgt = target_code(magic, reveal_addr)
    got = forge(key, suffixes, pos)
    print(f"target code = {tgt.hex()}")
    print(f"forged code = {got.hex()}")
    if got == tgt:
        print("MATCH - this key forges reveal(MAGIC). Flag will print.")
        return 0
    print("MISMATCH - this key does NOT forge the target.", file=sys.stderr)
    return 1

if __name__ == "__main__":
    sys.exit(main())
