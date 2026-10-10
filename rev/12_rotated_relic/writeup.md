# The Rotated Relic

**Difficulty:** beginner  
**Artifact:** Rotated ELF  
**Concept:** Infer and reverse a whole-file byte rotation.

## Tools

Use: **xxd, Python 3, file**

## Exact solve path

```sh
xxd -l 16 attachments/challenge.bin
```

Infer the byte rotation from the expected ELF magic, reverse it across the file, and run `python3 solver/solve.py`.

Do not brute-force the flag. The intended solution is to observe one runtime
value or repair one file-format invariant, then reproduce the operation.

## Flag

```text
SecurinetsENIT{rotate_the_relic_back}
```
