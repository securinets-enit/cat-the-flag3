# The DLL in Disguise

**Difficulty:** beginner  
**Artifact:** Managed DLL  
**Concept:** Identify and load a mislabeled assembly.

## Tools

Use: **file, strings, ILSpy or ilspycmd, dotnet**

## Exact solve path

```sh
strings attachments/challenge.bin | Select-String MANAGED
```

Recognize the managed payload despite its misleading extension, inspect it with ILSpy, and run `python3 solver/solve.py`.

Do not brute-force the flag. The intended solution is to observe one runtime
value or repair one file-format invariant, then reproduce the operation.

## Flag

```text
SecurinetsENIT{extensions_do_not_define_formats}
```
