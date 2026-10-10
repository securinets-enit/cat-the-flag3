# The Clockmaker's Backward Ledger

**Difficulty:** beginner  
**Artifact:** ELF  
**Concept:** Undo a reverse loop and per-byte shift.

## Tools

Use: **file, readelf, objdump, GDB, Python 3**

## Exact solve path

```sh
gdb -q -x debug.gdb --args attachments/03_clockmakers_backward_ledger
```

Run the attachment, apply the GDB observation described above, then execute `python3 solver/solve.py`. The solver replays the task-specific transformation and prints `SecurinetsENIT{the_clock_runs_backward}`.

Do not brute-force the flag. The intended solution is to observe one runtime
value or repair one file-format invariant, then reproduce the operation.

## Flag

```text
SecurinetsENIT{the_clock_runs_backward}
```
