#!/usr/bin/env python3
"""
solve_poc.py - author-side proof that LayerUp is solvable with a solver.

Given the reversed VM semantics and the two extracted targets, Z3 recovers the
flag. This models the realistic player scenario: the flag structure/charset is
known, the random token is not. Needs: pip install z3-solver

NOT part of the player distribution - this is a solution artifact.
"""
import z3

# --- parameters a player extracts by reversing the VM + bytecode ----------
BASIS_A, BASIS_B = 0x7E4A1C3B, 0x2D5F8E11
MULT_A,  MULT_B  = 0xA3C59AC3, 0xCF1BBCDD
R1, R2, SHIFT    = 11, 7, 16
TARGET_A, TARGET_B = 0xA5219537, 0xC19B6387

flag = b"SecurinetsENIT{t3st_t3st_1ay3r_up_th3_vm_cha1n_4a9f2c81_y0ufaaa}"
LEN = len(flag)

# Treat the 8-hex token as unknown (constrained to [0-9a-f]); rest is known.
tok = flag.index(b"4a9f2c81")
unknown = set(range(tok, tok + 8))

s = z3.Solver()
inp = []
for i in range(LEN):
    if i in unknown:
        c = z3.BitVec(f"c{i}", 32)
        s.add(z3.Or(z3.And(c >= ord('0'), c <= ord('9')),
                    z3.And(c >= ord('a'), c <= ord('f'))))
        inp.append(c)
    else:
        inp.append(z3.BitVecVal(flag[i], 32))

A = z3.BitVecVal(BASIS_A, 32)
B = z3.BitVecVal(BASIS_B, 32)
for i in range(LEN):
    b = inp[i] & 0xff
    A = A ^ b
    A = z3.RotateLeft(A, R1)
    A = A * MULT_A
    A = A + i
    t = z3.LShR(A, SHIFT)
    B = B + t * MULT_B
    B = z3.RotateLeft(B, R2)
    B = B ^ b
s.add(A == TARGET_A, B == TARGET_B)

assert s.check() == z3.sat, "UNSAT - challenge would be unfair!"
m = s.model()
out = bytearray(flag)
for i in unknown:
    out[i] = m[inp[i]].as_long() & 0xff
print("solver recovered:", out.decode())
print("matches intended:", bytes(out) == flag)
