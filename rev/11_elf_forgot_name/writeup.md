# The ELF That Forgot Its Name

**Difficulty:** beginner  
**Artifact:** Damaged ELF  
**Concept:** Repair the ELF magic bytes.

## Tools

Use: **file, xxd, a hex editor, Python 3**

## Exact solve path

```sh
xxd -l 32 attachments/challenge.bin
```

Restore the first four bytes to `7f 45 4c 46`, confirm with `file`, and then run `python3 solver/solve.py`.

Do not brute-force the flag. The intended solution is to observe one runtime
value or repair one file-format invariant, then reproduce the operation.

## Flag

```text
SecurinetsENIT{a_name_is_only_four_bytes}
```
