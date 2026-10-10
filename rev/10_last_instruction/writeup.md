# The Last Instruction

**Difficulty:** intermediate  
**Artifact:** ELF  
**Concept:** Track a rotating state machine at runtime.

## Tools

Use: **file, readelf, objdump, GDB, Python 3**

## Exact solve path

```sh
gdb -q -x debug.gdb --args attachments/10_last_instruction
```

Run the attachment, apply the GDB observation described above, then execute `python3 solver/solve.py`. The solver replays the task-specific transformation and prints `SecurinetsENIT{the_last_state_is_the_key}`.

Do not brute-force the flag. The intended solution is to observe one runtime
value or repair one file-format invariant, then reproduce the operation.

## Flag

```text
SecurinetsENIT{the_last_state_is_the_key}
```
