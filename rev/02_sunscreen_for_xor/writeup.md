# Sunscreen for XOR

**Difficulty:** beginner  
**Artifact:** ELF  
**Concept:** Recover a single-byte XOR key from a decoder loop.

## Tools

Use: **file, readelf, objdump, GDB, Python 3**

## Exact solve path

```sh
gdb -q -x debug.gdb --args attachments/02_sunscreen_for_xor
```

Run the attachment, apply the GDB observation described above, then execute `python3 solver/solve.py`. The solver replays the task-specific transformation and prints `SecurinetsENIT{sunlight_cannot_hide_xor}`.

Do not brute-force the flag. The intended solution is to observe one runtime
value or repair one file-format invariant, then reproduce the operation.

## Flag

```text
SecurinetsENIT{sunlight_cannot_hide_xor}
```
