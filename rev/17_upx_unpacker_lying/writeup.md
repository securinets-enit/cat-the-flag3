# UPX, But the Unpacker Is Lying

**Difficulty:** intermediate  
**Artifact:** Obscured UPX ELF  
**Concept:** Find packing evidence after section names are changed.

## Tools

Use: **file, strings, upx, Python 3, GDB**

## Exact solve path

```sh
upx -t attachments/challenge.bin
```

Identify the UPX marker, unpack or decode the payload, then run `python3 solver/solve.py` to print the flag.

Do not brute-force the flag. The intended solution is to observe one runtime
value or repair one file-format invariant, then reproduce the operation.

## Flag

```text
SecurinetsENIT{section_names_can_lie}
```
