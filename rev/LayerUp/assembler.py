#!/usr/bin/env python3
"""
assembler.py - mnemonic -> bytecode compiler for the LayerUp VM.

Usage:
    python3 assembler.py check.asm -o bytecode.h      # emit C header
    python3 assembler.py check.asm --bin check.bin     # also emit raw bytes
    python3 assembler.py check.asm                     # just print a hex dump

Syntax understood:
    ; comment to end of line
    label:                 a jump target (own line, or as a prefix)
    .def NAME value        define a constant symbol
    .target <flagstring>   run the reference accumulator over <flagstring> and
                           define the symbol TARGET as the resulting constant.
                           Requires BASIS / PRIME / ROT to be .def'd first.
    INSTR [operand]        one instruction per line

Operands may be decimal, 0x-hex, or a previously defined symbol / label.
"""

import sys

# opcode byte -> (mnemonic, operand kind). Bytes are deliberately scattered.
OPCODES = {
    "PUSH":   (0x3C, "imm32"),
    "LOAD":   (0x9A, None),
    "LEN":    (0x5E, None),
    "ADD":    (0x71, None),
    "SUB":    (0x24, None),
    "XOR":    (0xB8, None),
    "MUL":    (0x4D, None),
    "ROL":    (0xE2, None),
    "SHR":    (0x53, None),
    "AND":    (0x2F, None),
    "DUP":    (0x17, None),
    "SWAP":   (0xCA, None),
    "POP":    (0x66, None),
    "CMP_EQ": (0x8F, None),
    "JZ":     (0xD3, "addr"),
    "JMP":    (0x1B, "addr"),
    "HALT":   (0x7B, None),
    "STOREV": (0x42, "slot"),
    "LOADV":  (0xAE, "slot"),
}

SIZE = {None: 1, "imm32": 5, "addr": 3, "slot": 2}  # includes the opcode byte

MASK = 0xFFFFFFFF


def rol32(v, c):
    c &= 31
    return ((v << c) | (v >> (32 - c))) & MASK if c else (v & MASK)


def accumulate(flag_bytes, p):
    """Reference implementation of the dual rolling accumulator.

    MUST stay byte-for-byte equivalent to what check.asm executes. `p` is a
    dict of the parameters defined in check.asm (BASIS_A, BASIS_B, MULT_A,
    MULT_B, R1, R2, SHIFT):

        A = BASIS_A
        B = BASIS_B
        for i, b in enumerate(input):
            A  = A ^ b
            A  = rol(A, R1)
            A  = A * MULT_A          # odd -> bijective in A
            A  = A + i
            t  = A >> SHIFT          # LOSSY: keeps only the high bits of A
            B  = B + t * MULT_B      # couples B to A's high bits
            B  = rol(B, R2)
            B  = B ^ b
        verdict = (A == TARGET_A) and (B == TARGET_B)

    The `A >> SHIFT` truncation destroys information, so the chain cannot be
    cleanly inverted backwards; the two coupled targets force a solver.
    """
    A = p["BASIS_A"] & MASK
    B = p["BASIS_B"] & MASK
    for i, b in enumerate(flag_bytes):
        A = (A ^ b) & MASK
        A = rol32(A, p["R1"])
        A = (A * p["MULT_A"]) & MASK
        A = (A + i) & MASK
        t = (A >> (p["SHIFT"] & 31)) & MASK
        B = (B + (t * p["MULT_B"])) & MASK
        B = rol32(B, p["R2"])
        B = (B ^ b) & MASK
    return A, B


def parse_value(tok, symbols):
    tok = tok.strip()
    if tok in symbols:
        return symbols[tok]
    try:
        return int(tok, 0) & MASK
    except ValueError:
        raise SystemExit(f"error: unknown symbol or bad number: {tok!r}")


def tokenize(path):
    """Return a list of (kind, data, lineno) records preserving order."""
    records = []
    with open(path, "r") as f:
        for lineno, raw in enumerate(f, 1):
            line = raw.split(";", 1)[0].rstrip("\n")
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith(".target"):
                # everything after the directive word is the flag, verbatim
                arg = stripped[len(".target"):].strip()
                records.append(("target", arg, lineno))
                continue
            if stripped.startswith(".def"):
                parts = stripped.split()
                if len(parts) != 3:
                    raise SystemExit(f"line {lineno}: .def NAME value")
                records.append(("def", (parts[1], parts[2]), lineno))
                continue
            # a line may be "label:" or "label: INSTR ..." or "INSTR ..."
            if ":" in stripped:
                label, rest = stripped.split(":", 1)
                records.append(("label", label.strip(), lineno))
                stripped = rest.strip()
                if not stripped:
                    continue
            parts = stripped.split(None, 1)
            mnem = parts[0].upper()
            operand = parts[1].strip() if len(parts) > 1 else None
            records.append(("insn", (mnem, operand), lineno))
    return records


def assemble(path):
    records = tokenize(path)
    symbols = {}

    # --- pass 0: resolve .def and .target so symbols exist, and lay out labels
    # First handle directives in order (they may depend on earlier defs).
    insns = []  # (mnem, operand, lineno)
    for kind, data, lineno in records:
        if kind == "def":
            name, valtok = data
            symbols[name] = parse_value(valtok, symbols)
        elif kind == "target":
            req = ("BASIS_A", "BASIS_B", "MULT_A", "MULT_B", "R1", "R2", "SHIFT")
            for r in req:
                if r not in symbols:
                    raise SystemExit(
                        f"line {lineno}: .target needs {r} defined first")
            ta, tb = accumulate(data.encode(), symbols)
            symbols["TARGET_A"] = ta
            symbols["TARGET_B"] = tb
            sys.stderr.write(
                f"[.target] {len(data)} bytes -> "
                f"TARGET_A = 0x{ta:08X}, TARGET_B = 0x{tb:08X}\n")
        elif kind == "label":
            insns.append(("__label__", data, lineno))
        elif kind == "insn":
            insns.append((data[0], data[1], lineno))

    # --- pass 1: assign addresses to labels
    addr = 0
    for mnem, operand, lineno in insns:
        if mnem == "__label__":
            if operand in symbols:
                raise SystemExit(f"line {lineno}: duplicate symbol {operand}")
            symbols[operand] = addr
            continue
        if mnem not in OPCODES:
            raise SystemExit(f"line {lineno}: unknown instruction {mnem!r}")
        addr += SIZE[OPCODES[mnem][1]]

    # --- pass 2: emit bytes
    out = bytearray()
    for mnem, operand, lineno in insns:
        if mnem == "__label__":
            continue
        opcode, kind = OPCODES[mnem]
        out.append(opcode)
        if kind is None:
            if operand is not None:
                raise SystemExit(f"line {lineno}: {mnem} takes no operand")
            continue
        if operand is None:
            raise SystemExit(f"line {lineno}: {mnem} needs an operand")
        val = parse_value(operand, symbols)
        if kind == "imm32":
            out += val.to_bytes(4, "little")
        elif kind == "addr":
            if val > 0xFFFF:
                raise SystemExit(f"line {lineno}: address out of range")
            out += val.to_bytes(2, "little")
        elif kind == "slot":
            if val > 0xFF:
                raise SystemExit(f"line {lineno}: slot out of range")
            out.append(val)
    return bytes(out)


def emit_header(data, name="g_bytecode"):
    lines = [
        "/* Auto-generated by assembler.py - do not edit by hand. */",
        "#ifndef LAYERUP_BYTECODE_H",
        "#define LAYERUP_BYTECODE_H",
        "",
        f"static const unsigned char {name}[] = {{",
    ]
    for i in range(0, len(data), 12):
        chunk = data[i:i + 12]
        lines.append("    " + "".join(f"0x{b:02X}, " for b in chunk).rstrip())
    lines.append("};")
    lines.append(f"static const unsigned int {name}_len = {len(data)}U;")
    lines.append("")
    lines.append("#endif /* LAYERUP_BYTECODE_H */")
    return "\n".join(lines) + "\n"


def main(argv):
    if len(argv) < 2:
        raise SystemExit(__doc__)
    src = argv[1]
    out_header = None
    out_bin = None
    i = 2
    while i < len(argv):
        if argv[i] in ("-o", "--out"):
            out_header = argv[i + 1]
            i += 2
        elif argv[i] == "--bin":
            out_bin = argv[i + 1]
            i += 2
        else:
            raise SystemExit(f"unknown option {argv[i]!r}")

    data = assemble(src)

    if out_header:
        with open(out_header, "w") as f:
            f.write(emit_header(data))
        sys.stderr.write(f"wrote {out_header} ({len(data)} bytes)\n")
    if out_bin:
        with open(out_bin, "wb") as f:
            f.write(data)
        sys.stderr.write(f"wrote {out_bin} ({len(data)} bytes)\n")
    if not out_header and not out_bin:
        sys.stderr.write(f"{len(data)} bytes:\n")
        print(" ".join(f"{b:02x}" for b in data))


if __name__ == "__main__":
    main(sys.argv)
