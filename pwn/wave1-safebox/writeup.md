# SecurinetsENIT CTF - Safebox Technical Writeup

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

The source code reveals a stack-allocated structure:
```c
struct Vault {
    char key_buffer[28];
    unsigned long long master_key;
    int is_unlocked;
};
```
The application calls:
```c
read(0, vault.key_buffer, 48);
```
Because `key_buffer` is only 28 bytes inside the struct, reading up to 48 bytes overflows into the adjacent struct fields: `master_key` and `is_unlocked`.

---

## 2. The Anti-AI Trap: Compiler Alignment & Padding

An LLM analyzing purely the source code line `char key_buffer[28]` will naively conclude:
- Offset to `master_key` = 28 bytes.
- Payload = `"A" * 28 + p64(0x5345435552495445)`.

However, under the **System V AMD64 ABI**, 64-bit integer types (`unsigned long long`, `uint64_t`) **must be 8-byte aligned** in memory.
- `key_buffer` starts at offset 0 and takes 28 bytes (`0x1C`).
- Offset 28 is **not divisible by 8**.
- GCC automatically inserts **4 bytes of invisible padding** between `key_buffer` and `master_key` to align `master_key` at offset 32 (`0x20`).

If a player or automated tool sends 28 bytes of filler followed by the key, the 4 padding bytes absorb the first 4 bytes of the key, resulting in an immediate mismatch.

In GDB, this is verified instantly:
```gdb
(gdb) print (size_t)&((struct Vault*)0)->master_key
$1 = 32
```

---

## 3. Endianness & Memory Layout

The expected value is:
`0x5345435552495445`

In ASCII:
- 0x53 = 'S'
- 0x45 = 'E'
- 0x43 = 'C'
- 0x55 = 'U'
- 0x52 = 'R'
- 0x49 = 'I'
- 0x54 = 'T'
- 0x45 = 'E'

Because x86-64 is **little-endian**, multi-byte integers are stored with the least significant byte at the lowest memory address. Therefore, in memory, the bytes must appear as:
`\x45\x54\x49\x52\x55\x43\x45\x53` (the reverse string: `ETIRUCES`).

### Memory Diagram:
```
+---------------------------------------+  <- vault.key_buffer (offset 0)
| 28 bytes of user input                |
+---------------------------------------+  <- (offset 28 / 0x1C)
| 4 bytes compiler alignment padding    |
+---------------------------------------+  <- vault.master_key (offset 32 / 0x20)
| 8 bytes: 0x5345435552495445 (SECURITE)|
+---------------------------------------+
```

---

## 4. Exploitation Walkthrough

1. Send 32 bytes of filler (`b"A" * 32`).
2. Append the 64-bit packed integer `0x5345435552495445`.
3. Total payload length: 40 bytes (well within the 48-byte limit).
4. `vault.master_key` is matched, invoking `win()` to display `flag.txt`.

---

## 5. Defensive Remediation & Secure Coding

To secure this code against buffer overflows:
1. **Enforce Strict Bounds:** Use `sizeof(vault.key_buffer)` instead of hardcoded numbers:
   ```c
   ssize_t n = read(0, vault.key_buffer, sizeof(vault.key_buffer));
   ```
2. **Compiler Protections:** Compile with `-fstack-protector-strong` and `-D_FORTIFY_SOURCE=2`.
