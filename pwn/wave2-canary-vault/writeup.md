# SecurinetsENIT CTF - Canary Vault Technical Writeup

- **Wave:** 2 (Control Hijacking & Gadgets)
- **Category:** Pwn / Binary Exploitation
- **Difficulty:** Intermediate
- **Target OS:** Ubuntu 22.04 LTS (x86_64)
- **Mitigations:**
  - Canary: **Enabled** (`-fstack-protector-all`)
  - NX: Enabled
  - PIE: Disabled (`-no-pie`)

---

## 1. Vulnerability Analysis

This challenge features a two-stage exploitation flow:
1. **Stage 1 (`stage1_leak`):**
   ```c
   char name[32];
   read(0, name, 32);
   printf("Agent registered: %s\n", name);
   ```
   `read()` does NOT append a null byte. If the user sends 32 non-null characters, `name` is no longer null-terminated.
   In GCC x86-64, the stack canary (`fs:0x28`) is placed immediately adjacent to the local buffer.
   Crucially, **the lowest byte of the stack canary is always a null byte (`0x00`)**!
   By filling the 32 bytes of `name` plus overwriting the null byte with a non-null character, `printf("%s\n", name)` continues printing past the buffer, dumping the remaining 7 bytes of the active canary!

2. **Stage 2 (`stage2_overflow`):**
   ```c
   char response[64];
   read(0, response, 128);
   ```
   A standard buffer overflow. However, if we corrupt the canary, GCC calls `__stack_chk_fail` and terminates.
   By inserting the canary leaked from Stage 1 into the payload, the integrity check passes, allowing us to hijack Saved RIP to `win()`!

---

## 2. The Anti-AI Trap: The 7-byte Canary vs 8-byte Canary

Automated AI tools consistently fail on two aspects:
1. **Leading Null Byte:** A canary is 8 bytes in 64-bit Linux, but its least significant byte is ALWAYS `0x00` (designed specifically to prevent string leaks). An AI script often fails to reconstruct the full 8 bytes by prepending `b"\x00"`.
2. **Stateful Coordination:** Multi-step protocols (leaking in step 1, using in step 2) break one-shot prompt bots.

---

## 3. Exploitation Walkthrough

### Step 1: Leak Canary
1. Send 33 bytes: 32 bytes of `b"A"` + 1 byte `b"B"` to overwrite the canary null byte.
2. Read the response: `name[32] + "B" + canary[1:8]`.
3. Reconstruct the full 8-byte canary:
   ```python
   canary = b"\x00" + leaked_bytes[:7]
   ```

### Step 2: Smashing with Canary Intact
1. Offset to canary in `stage2_overflow`:
   - `response`: 64 bytes
   - Canary at offset: 64
2. Structure of payload:
   ```
   [ 64 bytes Padding ]
   [ 8 bytes Canary ]         <- Exact leaked canary value
   [ 8 bytes Saved RBP ]      <- Junk filler
   [ 8 bytes: ret gadget ]    <- 16-byte stack alignment
   [ 8 bytes: win() address ] <- Control flow hijack
   ```
3. The function epilogue verifies `canary == fs:0x28`. The check succeeds!
4. The `ret` instruction executes, jumping cleanly to `win()` and printing `flag.txt`.

---

## 4. Defensive Remediation & Secure Coding

1. Always null-terminate strings after `read()`:
   ```c
   ssize_t n = read(0, name, sizeof(name) - 1);
   name[n] = 0;
   ```
2. Bound all input reading to the destination buffer size.
