# The Debugger's Missing Blink

**Difficulty:** intermediate  
**Artifact:** ELF  
**Concept:** Compare normal and watched execution paths.

## Tools

Use: **file, readelf, objdump, GDB, Python 3**

## Exact solve path

```sh
gdb -q -x debug.gdb --args attachments/07_debugger_missing_blink
```

Run the attachment, apply the GDB observation described above, then execute `python3 solver/solve.py`. The solver replays the task-specific transformation and prints `SecurinetsENIT{watch_the_branch_not_the_banner}`.

Do not brute-force the flag. The intended solution is to observe one runtime
value or repair one file-format invariant, then reproduce the operation.

## Flag

```text
SecurinetsENIT{watch_the_branch_not_the_banner}
```
