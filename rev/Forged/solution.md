# Forged — Official Solution

Intended solve for the "Forged" stage. The player gets a single stripped binary
(`dist/forge`) and `dist/challenge.txt`. There is **no key comparison anywhere in
the binary**: the correct key's MD5 digests *assemble into the machine code* that
prints the flag. A disassembler shows the hashing and an `mmap`+indirect-call, but
never a check to patch.

**Flag:** `SecurinetsENIT{c0d3_f0rg3d_fr0m_1ts_0wn_h4sh_1s_th3_0nly_judg3}`

Author-side files referenced here (`task.c`, `solve.c`, `solve.py`, `build.py`) live
in the `Forged/` folder; they are *not* shipped to players. Addresses and the key
change on every rebuild — `answer.txt` is the source of truth.

---

## Step 0 — Triage the binary

```
$ file dist/forge
dist/forge: ELF 64-bit LSB executable, x86-64, no-pie, dynamically linked, stripped
$ ./dist/forge
key: 41414141414141414141414141414141
nope.
$ strings dist/forge | grep -i securinets        # nothing
$ strace ./dist/forge
ptrace(PTRACE_TRACEME) = -1 EPERM
Not while you're watching.
```

Stripped, single verdict, no flag string, and it dies the moment anything traces
it. Two problems to solve: get it to run under a debugger at all, then work out
what it actually checks.

**Output:** an anti-debug gate and a hashing routine that never compares anything.

---

## Step 1 — Get past the watcher

The first thing `main` calls is a tiny function that runs
`ptrace(PTRACE_TRACEME, 0, 0, 0)` and exits on `-1`. A process can only be traced
once, so if a debugger (or `strace`) is already attached, the self-attach fails
and the program bails with *"Not while you're watching."*

Any of these defeats it:

```
# a) LD_PRELOAD a stub that returns 0  (cleanest for scripting)
echo 'long ptrace(int r,int p,void*a,void*d){return 0;}' > stub.c
gcc -shared -fPIC -o stub.so stub.c
LD_PRELOAD=./stub.so ./dist/forge

# b) in gdb, lie about the syscall result
catch syscall ptrace
run
set $rax = 0
delete 1
continue

# c) patch the conditional jump after cmp rax,-1  (0x75 jne -> 0xeb jmp)
```

With the gate bypassed the prompt `key:` appears and the real mechanism runs.

**Output:** a runnable binary.

---

## Step 2 — Read the mechanism (there is no comparison)

In the decompiler, `main` after the gate does, in order:

```c
read 32 hex chars -> 16 bytes key[16]
page = mmap(RWX); memset(page, 0xC3, 4096);        // 0xC3 = ret everywhere
for (i = 0; i < 4; i++) {
    md5( key[4i : 4i+4]  ||  SUFFIX[i] )            // 4 input + 8 fixed = 12 bytes
    page[3i + 0] = digest[POS[0]];
    page[3i + 1] = digest[POS[1]];                  // 3 chosen bytes per chunk
    page[3i + 2] = digest[POS[2]];
}
((void(*)())page)();                                // CALL the forged bytes
```

That is the whole trick. The input is split into **four independent 4-byte
chunks**; each is glued to a different fixed **8-byte suffix** and MD5'd alone;
**three bytes** of each digest (at fixed positions `POS`) are copied into an
executable page; the page is then **called as code**. There is no `if (hash ==
...)` — the digest *is* the program that decides the outcome.

So the attack is not "find the key". It is: decide what 12 bytes of machine code
you want forged, then find an input that hashes to them.

Three constants must be lifted out of the binary:

- the four **8-byte suffixes** (a `SUFFIX[4][8]` array in `.rodata`),
- the three **digest positions** `POS`,
- and the **target opcodes** you want — which means finding `reveal` and `MAGIC`.

---

## Step 3 — Find the target: `reveal` and `MAGIC`

One function, never called directly by `main`, prints the flag. It takes a single
argument and begins with `if (arg != 0x5EED1E57) { puts("nope."); _exit(1); }` —
so `MAGIC = 0x5EED1E57`, read straight from the immediate. If the argument
matches, it decodes the flag with a MAGIC-seeded xorshift keystream and prints it
(that is why the flag never appears in `strings`).

Because the binary is `-no-pie`, `reveal` sits at a fixed address (e.g.
`0x400a4c`; read it from the symbol or the disassembly of this build). So the
machine code we want the page to contain is simply "call `reveal` with
`rdi = MAGIC`":

```
BF 57 1E ED 5E     mov edi, 0x5EED1E57     ; the magic argument
B8 4C 0A 40 00     mov eax, 0x00400a4c     ; &reveal (fits in 32 bits, no-pie)
FF E0              jmp rax
```

Twelve bytes — exactly four chunks × three forged bytes. `jmp` (not `call`) keeps
the stack aligned on entry to `reveal`, and `reveal`'s own `ret`/`_exit` ends the
program cleanly. Wrong keys forge nonsense; the first bytes either trap (a
SIGSEGV/SIGILL handler turns that into *"nope."*) or hit the `0xC3` filler and
return without ever reaching `reveal`.

**Target bytes:** `bf571eed5eb84c0a4000ffe0`.

---

## Step 4 — Map the 12 bytes onto the four chunks

Chunk *i* owns `page[3i .. 3i+2]`, so slice the target accordingly:

| Chunk | Hashed as | Must produce (digest[POS]) |
|-------|-----------|----------------------------|
| 0 | `md5(c0 ‖ SUFFIX[0])` | `bf 57 1e` |
| 1 | `md5(c1 ‖ SUFFIX[1])` | `ed 5e b8` |
| 2 | `md5(c2 ‖ SUFFIX[2])` | `4c 0a 40` |
| 3 | `md5(c3 ‖ SUFFIX[3])` | `00 ff e0` |

Each is an independent constraint on **3 bytes** of an MD5 output: probability
`2^-24` per guess, so ~16M tries expected per chunk — trivially brute-forceable,
and the four searches run in parallel.

---

## Step 5 — Brute-force the chunks

`solve.c` searches the 2^32 space of 4 input bytes per chunk with OpenMP until the
three digest bytes at `POS` match the target slice:

```
$ gcc -O3 -fopenmp -o solve solve.c
$ ./solve <POS0> <POS1> <POS2> <suf0> <suf1> <suf2> <suf3> bf571eed5eb84c0a4000ffe0
chunk 0: 004c4884
chunk 1: 004b7115
chunk 2: 46b67f00
chunk 3: 00f93911
84484c004b71150046b67f00f9391100
```

(`build.py` runs exactly this and writes the result to `answer.txt`.) All four
chunks resolve in a few seconds on a many-core box.

---

## Step 6 — Verify, then enter

`solve.py` replays the whole pipeline in Python — chunk → MD5 → pick `POS` bytes —
and confirms the forged 12 bytes equal the target *before* touching the binary:

```
$ python3 solve.py
target code = bf571eed5eb84c0a4000ffe0
forged code = bf571eed5eb84c0a4000ffe0
MATCH - this key forges reveal(MAGIC). Flag will print.
```

Then feed it to the real binary (with the ptrace gate bypassed):

```
$ LD_PRELOAD=./stub.so ./dist/forge
key: 84484c004b71150046b67f00f9391100
The lock forges its own key and swings open:
SecurinetsENIT{c0d3_f0rg3d_fr0m_1ts_0wn_h4sh_1s_th3_0nly_judg3}
```

**Flag:** `SecurinetsENIT{c0d3_f0rg3d_fr0m_1ts_0wn_h4sh_1s_th3_0nly_judg3}`

---

## Why the usual shortcuts fail

- **Nothing to patch.** There is no comparison and no stored hash; the verdict is
  manufactured from your input at runtime. Patching "the check" means patching
  code that does not exist.
- **Can't run it backwards.** MD5 is one-way, so you cannot derive an input from
  the desired output bytes — you have to search. The split into four 3-byte
  constraints is what keeps that search in the "seconds" range instead of `2^128`.
- **The flag isn't in the file.** It is XOR'd with a MAGIC-derived keystream and
  only reconstructed inside `reveal(MAGIC)`, which is reached solely by forged
  code — so dumping strings or forcing the branch with the wrong magic yields
  nothing.

## Notes for difficulty tuning

- The gate is a single well-known check; the real time sink is recognising the
  "mmap + call the hash" shape and realising you must *choose* the target code.
- `POS`, the suffixes, `MAGIC` and the flag all change with `SEED` / `MAGIC` /
  `FLAG` env vars at build time, so the challenge re-rolls cleanly.
- Needs a kernel that allows `PTRACE_TRACEME`; under a seccomp profile that blocks
  `ptrace` (some container defaults) the binary exits as if watched — run it in a
  normal Linux / VM.
