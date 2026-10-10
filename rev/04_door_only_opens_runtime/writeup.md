# The Door That Only Opens at Runtime

**Difficulty:** beginner  
**Artifact:** ELF  
**Concept:** Inspect `strcmp` arguments to recover the password.

## Tools

Use: **file, readelf, objdump, GDB, Python 3**

## Exact solve path

```sh
gdb -q -x debug.gdb --args attachments/04_door_only_opens_runtime
```

Run the attachment, apply the GDB observation described above, then execute `python3 solver/solve.py`. The solver replays the task-specific transformation and prints `SecurinetsENIT{runtime_keys_open_doors}`.

Do not brute-force the flag. The intended solution is to observe one runtime
value or repair one file-format invariant, then reproduce the operation.

## Flag

```text
SecurinetsENIT{runtime_keys_open_doors}
```
