import sys
OPS={0x3C:("PUSH","imm32"),0x9A:("LOAD",0),0x5E:("LEN",0),0x71:("ADD",0),
0x24:("SUB",0),0xB8:("XOR",0),0x4D:("MUL",0),0xE2:("ROL",0),0x53:("SHR",0),
0x2F:("AND",0),0x17:("DUP",0),0xCA:("SWAP",0),0x66:("POP",0),0x8F:("CMP_EQ",0),
0xD3:("JZ","addr"),0x1B:("JMP","addr"),0x7B:("HALT",0),0x42:("STOREV","slot"),
0xAE:("LOADV","slot")}
d=open(sys.argv[1],'rb').read(); pc=0
while pc<len(d):
    op=d[pc]; name,kind=OPS.get(op,("??",0)); a=pc; pc+=1
    if kind=="imm32":
        v=int.from_bytes(d[pc:pc+4],'little'); pc+=4; print(f"{a:04x}: {name} 0x{v:08X}")
    elif kind=="addr":
        v=int.from_bytes(d[pc:pc+2],'little'); pc+=2; print(f"{a:04x}: {name} 0x{v:04x}")
    elif kind=="slot":
        v=d[pc]; pc+=1; print(f"{a:04x}: {name} {v}")
    else:
        print(f"{a:04x}: {name}")
