# Clockwork Minotaur

**Difficulty:** intermediate  
**Artifact:** ELF  
**Concept:** Emulate a four-opcode bytecode machine.

## Tools

Use: **file, readelf, objdump, GDB, Python 3**

## Exact solve path

```sh
gdb -q -x debug.gdb --args attachments/06_clockwork_minotaur
```

Run the attachment, apply the GDB observation described above, then execute `python3 solver/solve.py`. The solver replays the task-specific transformation and prints `SecurinetsENIT{the_minotaur_has_four_opcodes}`.

Do not brute-force the flag. The intended solution is to observe one runtime
value or repair one file-format invariant, then reproduce the operation.

## Flag

```text
SecurinetsENIT{the_minotaur_has_four_opcodes}
```
