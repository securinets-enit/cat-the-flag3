# WASM Maze â€” Complete Walkthrough

## 1. Challenge goal

The attachment is `attachments/maze.wat`, a WebAssembly text-format module.
The exported function is intentionally noisy: it pushes integer constants
instead of performing an obvious string comparison.

The task is to recover the flag from the constants and the byte transformation
used to generate them.

## 2. Inspect the module

Open `maze.wat` and find the exported function:

```text
(export "unlock" (func $unlock))
```

Then inspect the body of `$unlock`. It contains many instructions like:

```text
i32.const  ...
```

The important observation is that these constants are in a predictable
sequence. They are not random maze coordinates; each one represents one
encoded flag byte.

The module also contains a few trailing constants used by the generated
function for its store address and return value. Those are not flag bytes.
Only constants inside the function body should be considered, and the final
implementation constants must be excluded.

## 3. Extract the encoded values

A simple extraction script can isolate the function and collect its constants:

```python
import re
from pathlib import Path

text = Path("attachments/maze.wat").read_text()
function = text.split("(func", 1)[1].split("(data", 1)[0]
values = [int(x) for x in re.findall(r"i32\.const (\d+)", function)]
encoded = values[:-3]
```

The `[:-3]` removes the three non-flag constants at the end of the generated
function. This boundary matters: including them produces an extra decoded
character, while removing too many flag constants truncates the result.

## 4. Recover the encoding formula

The builder applies this transformation to every flag byte:

```text
encoded[index] =
    ord(flag[index]) XOR ((index * 0x2d + 0x17) & 0xff)
```

XOR is its own inverse. Therefore the original character is recovered using
the same operation:

```text
flag[index] =
    encoded[index] XOR ((index * 0x2d + 0x17) & 0xff)
```

The index starts at zero for the first extracted constant.

## 5. Decode the constants

Use the following loop:

```python
decoded = []
for index, value in enumerate(encoded):
    key = (index * 0x2d + 0x17) & 0xff
    decoded.append(chr(value ^ key))

print("".join(decoded))
```

The result is:

```text
SecurinetsENIT{w4sm_memory_is_not_magic}
```

## 6. Verify with the supplied solver

Run:

```powershell
python src\solve.py attachment\maze.wat
```

It should print exactly:

```text
SecurinetsENIT{w4sm_memory_is_not_magic}
```

No WebAssembly runtime is required. A player can solve this statically from
the WAT file. If using tools such as `wasm2wat`, remember that the text output
is an intermediate representation and should be read as data flow rather than
as a normal high-level program.

## 7. Main lesson

WebAssembly uses typed integer instructions, but `i32.const` values can still
carry encoded data. First identify which constants are data and which are
control-flow or API arguments. Then reverse simple byte-wise transformations,
especially XOR, by applying the same operation again.

