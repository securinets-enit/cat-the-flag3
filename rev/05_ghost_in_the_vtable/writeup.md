# Ghost in the Vtable

**Difficulty:** intermediate  
**Artifact:** C++ ELF  
**Concept:** Follow a virtual call to the real decoder.

## Tools

Use: **file, readelf, objdump, GDB, Python 3**

## Exact solve path

```sh
gdb -q -x debug.gdb --args attachments/05_ghost_in_the_vtable
```

Run the attachment, apply the GDB observation described above, then execute `python3 solver/solve.py`. The solver replays the task-specific transformation and prints `SecurinetsENIT{ghosts_can_call_virtual_methods}`.

Do not brute-force the flag. The intended solution is to observe one runtime
value or repair one file-format invariant, then reproduce the operation.

## Flag

```text
SecurinetsENIT{ghosts_can_call_virtual_methods}
```
