# The Broken Entry Point

**Difficulty:** intermediate  
**Artifact:** Edited ELF  
**Concept:** Repair an entry point using program headers.

## Tools

Use: **readelf -h, readelf -l, objdump, Python 3**

## Exact solve path

```sh
readelf -h attachments/challenge.bin
```

Compare the entry point with executable program headers, repair it, and run `python3 solver/solve.py`.

Do not brute-force the flag. The intended solution is to observe one runtime
value or repair one file-format invariant, then reproduce the operation.

## Flag

```text
SecurinetsENIT{entry_points_must_land}
```
