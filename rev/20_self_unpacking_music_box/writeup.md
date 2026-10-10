# The Self-Unpacking Music Box

**Difficulty:** intermediate  
**Artifact:** Self-unpacking ELF  
**Concept:** Trace mmap/mprotect and dump decoded bytes.

## Tools

Use: **GDB, catch syscall, mmap/mprotect knowledge, Python 3**

## Exact solve path

```sh
gdb -q -x debug.gdb --args attachments/challenge.bin
```

Trace the payload mapping and permission change, dump the decoded bytes, and run `python3 solver/solve.py`.

Do not brute-force the flag. The intended solution is to observe one runtime
value or repair one file-format invariant, then reproduce the operation.

## Flag

```text
SecurinetsENIT{follow_the_music_box}
```
