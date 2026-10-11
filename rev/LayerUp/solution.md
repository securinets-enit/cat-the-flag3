# LayerUp — Official Solution (VM stage)

Intended solve for the VM/bytecode stage in isolation. (The maze + AES-CTR
layers wrap this later; this writeup assumes the player already has the
unpacked `layerup` binary.)

**Flag:** `SecurinetsENIT{t3st_t3st_1ay3r_up_th3_vm_cha1n_4a9f2c81_y0ufaaa}`

Author-side files referenced here (`disasm.py`, `solve_poc.py`) are included in
the `LayerUp/` folder; they are *not* shipped to players.

---

## Step 0 — Triage the binary

```
$ file dist/layerup
dist/layerup: ELF 64-bit LSB executable, x86-64, ... dynamically linked, ... stripped
$ ./dist/layerup 'test'
Wrong.
$ ./dist/layerup 'SecurinetsENIT{aaa}'
Wrong.
```

Stripped, single pass/fail verdict, no partial feedback. Loading it in Ghidra,
`main` reads the input (argv/stdin), then calls through a **256-entry
function-pointer table** in a loop — the classic shape of a bytecode VM with a
dispatch table rather than a `switch`.

**Output:** a VM + a byte blob in `.rodata` to decode.

---

## Step 1 — Recover the opcode table

Each live entry in the dispatch table points at a tiny handler. Reversing the
~19 handlers gives the instruction set (opcode bytes are scattered, not
sequential):

| Byte | Mnemonic | Effect |
|------|----------|--------|
| 0x3C | PUSH imm32 | push 32-bit immediate |
| 0x9A | LOAD | pop idx; push `input[idx]` (0 if out of range) |
| 0x5E | LEN | push input length |
| 0x71 | ADD | pop b,a; push a+b |
| 0x24 | SUB | pop b,a; push a−b |
| 0xB8 | XOR | pop b,a; push a^b |
| 0x4D | MUL | pop b,a; push a*b |
| 0xE2 | ROL | pop c,v; push rol(v,c) |
| 0x53 | SHR | pop c,v; push v>>c |
| 0x2F | AND | pop b,a; push a&b |
| 0x17 | DUP | duplicate top |
| 0xCA | SWAP | swap top two |
| 0x66 | POP | drop top |
| 0x8F | CMP_EQ | pop b,a; push a==b |
| 0xD3 | JZ addr | pop v; if 0 jump (absolute, 2-byte) |
| 0x1B | JMP addr | jump (absolute, 2-byte) |
| 0x7B | HALT | pop verdict (1==correct); stop |
| 0x42 | STOREV s | pop v; var[s]=v (1-byte slot) |
| 0xAE | LOADV s | push var[s] (1-byte slot) |

**Output:** a complete opcode map. (`DUP/SWAP/POP/AND` turn out to be unused by
the program — decoy handlers.)

---

## Step 2 — Extract the bytecode blob

The blob sits in `.rodata`, right after the `Correct!`/`Wrong.` strings:

```
$ objdump -s -j .rodata dist/layerup
 ...
 4022d0 436f7272 65637421 0057726f 6e672e00  Correct!.Wrong..
 4022e0 3c3b1c4a 7e42003c 118e5f2d 42013c00  <;.J~B.<.._-B.<.
 4022f0 00000042 02ae025e 8fd31f00 1b6300ae  ...B...^.....c..
 ...
```

Carve out the 117 bytes (here reproduced as `check.bin`):

```
$ xxd check.bin
00000000: 3c3b 1c4a 7e42 003c 118e 5f2d 4201 3c00  <;.J~B.<.._-B.<.
00000010: 0000 0042 02ae 025e 8fd3 1f00 1b63 00ae  ...B...^.....c..
00000020: 029a 4203 ae00 ae03 b83c 0b00 0000 e23c  ..B......<.....<
00000030: c39a c5a3 4dae 0271 4200 ae00 3c10 0000  ....M..qB...<...
00000040: 0053 3cdd bc1b cf4d ae01 713c 0700 0000  .S<....M..q<....
00000050: e2ae 03b8 4201 ae02 3c01 0000 0071 4202  ....B...<....qB.
00000060: 1b15 00ae 003c 3795 21a5 8fae 013c 8763  .....<7.!....<.c
00000070: 9bc1 8f4d 7b                             ...M{
```

**Output:** 117 raw bytecode bytes.

---

## Step 3 — Disassemble

With the opcode map, decode the blob (`disasm.py check.bin`):

```
0000: PUSH 0x7E4A1C3B      ; A = BASIS_A
0005: STOREV 0
0007: PUSH 0x2D5F8E11      ; B = BASIS_B
000c: STOREV 1
000e: PUSH 0x00000000      ; i = 0
0013: STOREV 2
0015: LOADV 2              ; loop_cond: while i != len
0017: LEN
0018: CMP_EQ
0019: JZ 0x001f
001c: JMP 0x0063
001f: LOADV 2              ; loop_body: b = input[i]
0021: LOAD
0022: STOREV 3
0024: LOADV 0              ; A = (rol(A ^ b, 11) * 0xA3C59AC3) + i
0026: LOADV 3
0028: XOR
0029: PUSH 0x0000000B
002e: ROL
002f: PUSH 0xA3C59AC3
0034: MUL
0035: LOADV 2
0037: ADD
0038: STOREV 0
003a: LOADV 0              ; t = A >> 16        (lossy!)
003c: PUSH 0x00000010
0041: SHR
0042: PUSH 0xCF1BBCDD      ; B = rol(B + t*0xCF1BBCDD, 7) ^ b
0047: MUL
0048: LOADV 1
004a: ADD
004b: PUSH 0x00000007
0050: ROL
0051: LOADV 3
0053: XOR
0054: STOREV 1
0056: LOADV 2              ; i++
0058: PUSH 0x00000001
005d: ADD
005e: STOREV 2
0060: JMP 0x0015
0063: LOADV 0              ; verdict = (A==TARGET_A) & (B==TARGET_B)
0065: PUSH 0xA5219537
006a: CMP_EQ
006b: LOADV 1
006d: PUSH 0xC19B6387
0072: CMP_EQ
0073: MUL
0074: HALT
```

**Output:** the full algorithm, including both target constants
`TARGET_A = 0xA5219537`, `TARGET_B = 0xC19B6387`.

---

## Step 4 — Understand the check

Two accumulators over one pass; no per-byte comparison:

```
A = 0x7E4A1C3B
B = 0x2D5F8E11
for i, b in enumerate(input):
    A = ((rol(A ^ b, 11)) * 0xA3C59AC3 + i) & 0xffffffff
    t = A >> 16                                   # lossy: low 16 bits dropped
    B = (rol((B + t*0xCF1BBCDD) & 0xffffffff, 7) ^ b) & 0xffffffff
verdict = (A == 0xA5219537) and (B == 0xC19B6387)
```

Key observations:

- The only comparison is at the very end, so the input can't be attacked
  byte-by-byte.
- `A >> 16` destroys information each round, so you **cannot step the chain
  backwards** from the targets.
- `B` depends on `A`'s high bits, so the two targets can't be satisfied
  independently.

Conclusion: solve it as a constraint system (Z3), not by hand-inversion.

---

## Step 5 — Solve with Z3

Model each input byte as an 8-bit value, replay the exact accumulator over
symbolic bytes, and assert both targets. Known structure (`SecurinetsENIT{...}`
+ printable/charset constraints on the unknown token) keeps it fast
(`solve_poc.py`):

```
$ python3 solve_poc.py
solver recovered: SecurinetsENIT{t3st_t3st_1ay3r_up_th3_vm_cha1n_4a9f2c81_y0ufaaa}
matches intended: True
```

**Output:** the flag.

---

## Step 6 — Verify against the binary

```
$ ./dist/layerup 'SecurinetsENIT{t3st_t3st_1ay3r_up_th3_vm_cha1n_4a9f2c81_y0ufaaa}'
Correct!
$ echo $?
0
```

**Flag:** `SecurinetsENIT{t3st_t3st_1ay3r_up_th3_vm_cha1n_4a9f2c81_y0ufaaa}`

---

## Notes for difficulty tuning

- Fully-free printable bytes make the Z3 model slow; constraining the unknown
  region to its real charset (hex token, etc.) solves in well under a second.
  That gap *is* the difficulty — a solver who understands the structure wins,
  brute force does not.
- In the full chain this bytecode is AES-CTR encrypted, so Steps 2–3 only become
  possible after the maze yields the key — that's where most of the challenge
  time should go.
