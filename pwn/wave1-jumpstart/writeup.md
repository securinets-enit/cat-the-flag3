# SecurinetsENIT CTF - Jumpstart Technical Writeup

- **Wave:** 1 (The Stack Fundamentals)
- **Category:** Pwn / Binary Exploitation
- **Difficulty:** Novice
- **Target OS:** Ubuntu 22.04 LTS (x86_64)
- **Mitigations:**
  - Canary: Disabled (`-fno-stack-protector`)
  - NX: Enabled
  - PIE: Disabled (`-no-pie`)

---

## 1. Vulnerability Analysis

In `vuln()`:
```c
char buffer[64];
read(0, buffer, 128);
```
A 64-byte stack buffer receives up to 128 bytes. This allows overwriting:
1. `buffer` (64 bytes)
2. Saved Base Pointer `RBP` (8 bytes)
3. Saved Return Instruction Pointer `RIP` (8 bytes)

Offset from start of `buffer` to `saved_rip`:
`64 + 8 = 72 bytes`.

---

## 2. The Anti-AI Trap: The 16-byte `movaps` Stack Alignment Crash

When standard automated tools or LLMs generate an exploit for `ret2win`, they typically output:
```python
payload = b"A" * 72 + p64(win_addr)
```
On **Ubuntu 22.04**, this payload reliably crashes with **SIGSEGV** inside `system()`!

### Why does it crash?
Under the **System V AMD64 ABI**:
> *The end of the input argument area shall be aligned on a 16-byte boundary. In other words, the value (%rsp + 8) is always a multiple of 16 when control is transferred to the function entry point.*

When a normal `call` instruction executes:
1. The CPU pushes an 8-byte return address onto the stack (`rsp` decreases by 8).
2. Upon entry into the target function, `rsp % 16 == 8`.
3. The function prologue executes `push rbp` (`rsp` decreases by another 8), making `rsp % 16 == 0` (16-byte aligned).

However, in a `ret2win` exploit:
- Execution reaches `win()` via a `ret` instruction (not a `call`).
- The `ret` pops the address from the stack (`rsp` increases by 8).
- Upon entry into `win()`, `rsp % 16 == 0`.
- When `win()` calls `system()`, the subsequent call pushes another 8 bytes (`rsp % 16 == 8`).
- Inside glibc `do_system`, modern compilers emit SSE vectorized instructions such as:
  ```assembly
  movaps XMMWORD PTR [rsp + 0x40], xmm0
  ```
- The `movaps` instruction hardware-faults if the memory address is not strictly 16-byte aligned.

---

## 3. How to Solve It

There are two clean ways to fix the alignment:

### Method 1: Add a `ret` Gadget (ROP Alignment)
Find a single `ret` gadget in the binary:
```bash
ROPgadget --binary jumpstart | grep ret
```
Prepend the `ret` gadget to the payload:
```
[ 72 bytes Padding ] + [ p64(ret_gadget) ] + [ p64(win_addr) ]
```
The `ret` gadget pops an address, shifting `rsp` by 8 bytes and restoring 16-byte alignment before entering `win()`.

### Method 2: Jump to `win + 1` or `win + 5`
Skip the `push rbp` in `win()` prologue by jumping directly to `win + 1` (or `win + 5`), adjusting the stack depth accordingly.

---

## 4. Defensive Remediation & Secure Coding

1. Replace `read()` with bounds-enforcing calls or check input size against buffer length:
   ```c
   read(0, buffer, sizeof(buffer));
   ```
2. Enable compiler stack canaries: `-fstack-protector-strong`.
