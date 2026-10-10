# The Reflectionist's Mirror

**Difficulty:** intermediate  
**Artifact:** .NET DLL  
**Concept:** Trace a method invoked through reflection.

## Tools

Use: **file, readelf, objdump, GDB, Python 3**

## Exact solve path

```sh
gdb -q -x debug.gdb --args attachments/09_reflectionists_mirror
```

Run the attachment, apply the GDB observation described above, then execute `python3 solver/solve.py`. The solver replays the task-specific transformation and prints `SecurinetsENIT{reflection_only_changes_the_route}`.

Do not brute-force the flag. The intended solution is to observe one runtime
value or repair one file-format invariant, then reproduce the operation.

## Flag

```text
SecurinetsENIT{reflection_only_changes_the_route}
```
