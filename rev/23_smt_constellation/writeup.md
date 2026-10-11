# SMT Constellation â€” Complete Walkthrough

## 1. Challenge goal

The attachment is `attachments/checker.py`. It validates a candidate flag with
many arithmetic constraints. The flag is not written as a plaintext constant,
so searching the file for the complete flag will not work.

The intended technique is to model the checker as a system of byte
constraints. An SMT solver such as Z3 can then recover the satisfying string.

## 2. Inspect the checker

The checker creates a byte list and rejects candidates with the wrong length.
It also checks printable values and the known prefix:

```python
if len(b) != 46:
    return False
if not all(32 <= x <= 126 for x in b):
    return False
```

The prefix is:

```text
SecurinetsENIT{
```

The final byte is the closing brace:

```text
}
```

The useful checks have the form:

```python
((b[i] ^ key) + b[i + 1]) & 255 == target
```

Each equation links two adjacent bytes. Together, the equations form a chain
through the candidate.

## 3. Translate one equation

For an equation such as:

```python
((b[9] ^ 58) + b[10]) & 255 == 142
```

the mathematical form is:

```text
(b[9] XOR 58 + b[10]) mod 256 = 142
```

The `& 255` operation keeps the result in the range 0â€“255, matching an
8-bit byte.

Do not accidentally interpret this as string concatenation or unrestricted
integer arithmetic. Every `b[i]` is a byte, and wraparound is part of the
constraint.

## 4. Build a Z3 model

Install Z3 if needed:

```powershell
python -m pip install z3-solver
```

Create one 8-bit symbolic variable per character:

```python
from z3 import BitVec, Solver

n = 46
b = [BitVec(f"b{i}", 8) for i in range(n)]
s = Solver()

for value in b:
    s.add(value >= 32, value <= 126)
```

Add the known wrapper:

```python
prefix = b"SecurinetsENIT{"
for index, value in enumerate(prefix):
    s.add(b[index] == value)
s.add(b[-1] == ord("}"))
```

Now parse or copy every checker equation into the model. A generic equation
builder is:

```python
s.add(((b[i] ^ key) + b[i + 1]) & 255 == target)
```

The included `src/solve.py` extracts the equations automatically, so manual
copying is not necessary for this challenge.

## 5. Solve the chain

Call the solver:

```python
if s.check() != sat:
    raise ValueError("no satisfying candidate")

model = s.model()
answer = bytes(model.evaluate(value).as_long() for value in b)
print(answer.decode("ascii"))
```

The recovered flag is:

```text
SecurinetsENIT{z3_finds_the_hidden_constellation}
```

## 6. Why the included solver can work without Z3

The reference solver starts from the known closing brace and walks the
adjacent equations backwards. For each equation, it tries all 256 possible
values for the unknown left byte, keeps printable candidates, and expects one
unique result.

That is equivalent to solving the same constraint system by exhaustive
enumeration over one byte at a time. Z3 is the more general approach and is
preferable when the checker contains branches, multiple variables, or
non-linear relationships.

Run the supplied solver with:

```powershell
python src\solve.py attachment\checker.py
```

## 7. Main lesson

When a validator is written as arithmetic over bytes, treat it as a formal
constraint problem instead of tracing it as ordinary application logic.
Bit-vector semantics, modular arithmetic, and known prefix/suffix bytes are
usually enough to turn a difficult-looking checker into a compact SMT model.

