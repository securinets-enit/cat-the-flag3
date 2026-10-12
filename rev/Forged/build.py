#!/usr/bin/env python3
"""
build.py - build "Forged" and compute the answer key.

Steps:
  1. Pick MAGIC / SUFFIX / POS, encode the flag, write generated.h.
  2. Compile forge.c (-O0 -no-pie, unstripped), read &reveal via nm.
  3. Assemble the 12-byte target shellcode: mov edi,MAGIC; mov eax,&reveal; jmp rax.
  4. Compile & run solve.c to brute-force the four 4-byte chunks.
  5. Verify the key against the real binary, then strip into dist/.

Env overrides: FLAG=..., MAGIC=0x..., SEED=0x... (for suffixes/positions).
"""
import os, re, struct, subprocess, hashlib, random, sys, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")
BIN  = "forge"            # shipped binary name

FLAG  = os.environ.get("FLAG", "SecurinetsENIT{c0d3_f0rg3d_fr0m_1ts_0wn_h4sh_1s_th3_0nly_judg3}")
MAGIC = int(os.environ.get("MAGIC", "0x5EED1E57"), 16) & 0xFFFFFFFF
SEED  = int(os.environ.get("SEED", "0xC0FFEE"), 16)

def sh(cmd, **kw):
    print("  $", " ".join(cmd))
    return subprocess.run(cmd, check=True, **kw)

def xorshift32_stream(seed, n):
    s = seed & 0xFFFFFFFF
    out = []
    for _ in range(n):
        s ^= (s << 13) & 0xFFFFFFFF
        s ^= (s >> 17)
        s ^= (s << 5)  & 0xFFFFFFFF
        out.append(s & 0xFF)
    return out

def main():
    rnd = random.Random(SEED)
    suffixes = [bytes(rnd.randrange(256) for _ in range(8)) for _ in range(4)]
    POS = sorted(rnd.sample(range(16), 3))    # three digest byte positions

    flag_bytes = FLAG.encode()
    ks = xorshift32_stream(MAGIC, len(flag_bytes))
    flag_enc = bytes(b ^ k for b, k in zip(flag_bytes, ks))

    # ---- generated.h -------------------------------------------------------
    def carr(name, data):
        return "static const unsigned char %s[] = {%s};" % (
            name, ",".join("0x%02x" % b for b in data))
    gh = ["#ifndef GENERATED_H\n#define GENERATED_H\n"]
    gh.append("#define MAGIC 0x%08xu" % MAGIC)
    gh.append("#define FLAG_LEN %d" % len(flag_bytes))
    gh.append(carr("FLAG_ENC", flag_enc))
    gh.append("static const int POS[3] = {%d,%d,%d};" % tuple(POS))
    gh.append("static const unsigned char SUFFIX[4][8] = {")
    for s in suffixes:
        gh.append("  {%s}," % ",".join("0x%02x" % b for b in s))
    gh.append("};")
    gh.append("#endif")
    open(os.path.join(HERE, "generated.h"), "w").write("\n".join(gh) + "\n")
    print("[*] MAGIC=0x%08x  POS=%s" % (MAGIC, POS))
    for i, s in enumerate(suffixes):
        print("    suffix[%d] = %s" % (i, s.hex()))

    # ---- compile forge -----------------------------------------------------
    forge_un = os.path.join(HERE, "forge.unstripped")
    sh(["gcc", "-O0", "-no-pie", "-fno-stack-protector", "-fcf-protection=none",
        "-o", forge_un, os.path.join(HERE, "task.c")])

    nm = subprocess.run(["nm", forge_un], capture_output=True, text=True).stdout
    m = re.search(r"^([0-9a-fA-F]+)\s+[Tt]\s+reveal$", nm, re.M)
    if not m:
        print("could not find reveal symbol", file=sys.stderr); sys.exit(1)
    reveal_addr = int(m.group(1), 16)
    print("[*] &reveal = 0x%x" % reveal_addr)
    if reveal_addr > 0xFFFFFFFF:
        print("reveal address does not fit in 32 bits", file=sys.stderr); sys.exit(1)

    # ---- target shellcode (12 bytes) --------------------------------------
    #   BF <imm32>   mov edi, MAGIC
    #   B8 <imm32>   mov eax, &reveal
    #   FF E0        jmp rax
    shell = b"\xBF" + struct.pack("<I", MAGIC) + \
            b"\xB8" + struct.pack("<I", reveal_addr) + b"\xFF\xE0"
    assert len(shell) == 12, len(shell)
    print("[*] target code = %s" % shell.hex())

    # ---- solve -------------------------------------------------------------
    solver = os.path.join(HERE, "solve")
    sh(["gcc", "-O3", "-fopenmp", "-o", solver, os.path.join(HERE, "solve.c")])
    args = [solver, str(POS[0]), str(POS[1]), str(POS[2])] + \
           [s.hex() for s in suffixes] + [shell.hex()]
    print("[*] brute-forcing four chunks ...")
    res = subprocess.run(args, capture_output=True, text=True)
    sys.stderr.write(res.stderr)
    if res.returncode != 0:
        print("solver failed", file=sys.stderr); sys.exit(1)
    key_hex = res.stdout.strip()
    print("[*] KEY = %s" % key_hex)

    # ---- verify in Python (replay the pipeline) ---------------------------
    key = bytes.fromhex(key_hex)
    forged = bytearray()
    for i in range(4):
        dig = hashlib.md5(key[4*i:4*i+4] + suffixes[i]).digest()
        forged += bytes(dig[p] for p in POS)
    assert bytes(forged) == shell, (bytes(forged).hex(), shell.hex())
    print("[*] python replay reproduces target code  OK")

    # ---- verify against the real binary -----------------------------------
    stub_c  = os.path.join(HERE, ".ptrace_stub.c")
    stub_so = os.path.join(HERE, ".ptrace_stub.so")
    open(stub_c, "w").write("long ptrace(int r,int p,void*a,void*d){return 0;}\n")
    sh(["gcc", "-shared", "-fPIC", "-o", stub_so, stub_c])
    env = dict(os.environ, LD_PRELOAD=stub_so)
    out = subprocess.run([forge_un], input=key_hex + "\n", env=env,
                         capture_output=True, text=True).stdout
    print("[*] binary says:")
    for ln in out.splitlines():
        print("      " + ln)
    assert FLAG in out, "flag not printed by real binary!"
    print("[*] real binary prints the flag  OK")

    # ---- stage dist/ -------------------------------------------------------
    os.makedirs(DIST, exist_ok=True)
    dist_bin = os.path.join(DIST, BIN)
    shutil.copy(forge_un, dist_bin)
    sh(["strip", "-s", dist_bin])
    open(os.path.join(DIST, "challenge.txt"), "w").write(CHALLENGE)
    print("[*] dist/ staged:", DIST)

    # record the answer for the author
    open(os.path.join(HERE, "answer.txt"), "w").write(
        "KEY=%s\nMAGIC=0x%08x\nreveal=0x%x\nPOS=%s\ntarget=%s\nFLAG=%s\n"
        % (key_hex, MAGIC, reveal_addr, POS, shell.hex(), FLAG))
    print("[*] answer.txt written. Done.")

CHALLENGE = """Forged

The gate has been sealed... and there is no way to enter.

No lock to pick, no code to read, no answer stored anywhere. The gate
forges its own verdict from whatever you feed it. Hand it the right
16 bytes (32 hex digits) and it writes the key that opens itself. Hand
it anything else and there is nothing to patch.

  ./forge
  key: <32 hex digits>

Flag format: SecurinetsENIT{...}
"""

if __name__ == "__main__":
    main()
