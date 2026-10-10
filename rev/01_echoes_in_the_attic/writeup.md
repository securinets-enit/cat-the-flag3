# Echoes in the Attic

**Difficulty:** beginner  
**Artifact:** ELF  
**Concept:** Find the live `puts` argument among decoys.

## Tools

Use: **file, readelf, objdump, GDB, Python 3**

## Exact solve path

```sh
gdb -q -x debug.gdb --args attachments/01_echoes_in_the_attic
```

Run the attachment, apply the GDB observation described above, then execute `python3 solver/solve.py`. The solver replays the task-specific transformation and prints `SecurinetsENIT{the_attic_echo_is_live}`.

Do not brute-force the flag. The intended solution is to observe one runtime
value or repair one file-format invariant, then reproduce the operation.

## Flag

```text
SecurinetsENIT{the_attic_echo_is_live}
```
