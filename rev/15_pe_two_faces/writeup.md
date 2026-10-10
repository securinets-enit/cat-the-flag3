# The PE with Two Faces

**Difficulty:** beginner  
**Artifact:** Damaged PE  
**Concept:** Repair a PE signature offset.

## Tools

Use: **Format-Hex, xxd, PE-bear or CFF Explorer, Python 3**

## Exact solve path

```sh
Format-Hex attachments/challenge.bin -Count 96
```

Read the PE pointer at offset `0x3c`, confirm the `PE\0\0` signature, and run `python3 solver/solve.py`.

Do not brute-force the flag. The intended solution is to observe one runtime
value or repair one file-format invariant, then reproduce the operation.

## Flag

```text
SecurinetsENIT{the_pe_points_to_itself}
```
