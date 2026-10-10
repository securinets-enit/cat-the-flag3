# The Header Is in the Attic

**Difficulty:** intermediate  
**Artifact:** Runtime-unpacked ELF  
**Concept:** Find a restored ELF header in memory.

## Tools

Use: **GDB, readelf, info proc mappings**

## Exact solve path

```sh
gdb -q -x debug.gdb --args attachments/challenge.bin
```

Search the runtime mapping for the restored ELF header, dump the payload, and run `python3 solver/solve.py`.

Do not brute-force the flag. The intended solution is to observe one runtime
value or repair one file-format invariant, then reproduce the operation.

## Flag

```text
SecurinetsENIT{the_header_waits_in_memory}
```
