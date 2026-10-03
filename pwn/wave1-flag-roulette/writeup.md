# SecurinetsENIT CTF - Flag Roulette Technical Writeup

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

In `play()`:
```c
char buffer[40];
volatile int lucky_target = 0;

for (int i = 0; i <= 40; i++) {
    char c;
    if (read(0, &c, 1) != 1) break;
    if (c == '\n') break;
    buffer[i] = c;
}
```
Notice the loop condition: `i <= 40`.
An array declared as `char buffer[40]` has valid indices from `0` to `39` (40 elements total).
When `i == 40`, the loop writes a 41st byte into `buffer[40]`, which extends beyond the array boundary.

---

## 2. Memory Layout & The Anti-AI Factor

On the stack, `lucky_target` is placed immediately after `buffer`:
```
+---------------------------------------+  <- buffer[0]
| buffer (40 bytes, index 0 to 39)      |
+---------------------------------------+  <- buffer[40] / lucky_target
| lucky_target (4 bytes)                |
+---------------------------------------+
```
When `buffer[40]` is written, it overwrites the **least significant byte** (LSB) of `lucky_target`.

The verification condition in `main()` is:
```c
if ((result & 0xFF) == 0x77)
```
`0x77` in ASCII is the character `'w'` (as in *win*).

An automated AI solver scanning for large overflows often misses classic `<= N` fence-post errors, assuming the buffer is safely contained. A competitor reading the loop boundary notices the subtle single-byte leak.

---

## 3. Exploitation Walkthrough

1. Send 40 bytes of padding (e.g., `"A" * 40`).
2. Append the single target byte `'w'` (`0x77`).
3. Total input: 41 bytes.
4. `buffer[40]` receives `'w'`, setting the low byte of `lucky_target` to `0x77`.
5. The condition `(result & 0xFF) == 0x77` evaluates to true, triggering `secret_jackpot()`.

---

## 4. Defensive Remediation & Secure Coding

1. **Fix the Fencepost Error:** Use `<` instead of `<=`:
   ```c
   for (int i = 0; i < sizeof(buffer); i++)
   ```
2. **Compiler Bounds Checking:** Use `-Warray-bounds` and `-fstack-protector-strong`.
