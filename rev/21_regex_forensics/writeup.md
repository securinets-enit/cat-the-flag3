# Regex Forensics â€” Complete Walkthrough

## 1. Challenge goal

The attachment is `attachments/validator.py`. It appears to be a normal
Python flag checker, but the flag is not stored in one direct comparison.
Instead, the checker builds one large regular expression named `PATTERN`.

The objective is to recover the string accepted by that regular expression.
This can be solved statically; no brute force or remote service is needed.

## 2. Read the validator

Open the attachment and locate `PATTERN`:

```python
PATTERN = (
    r"^(?=^.{42}$)(?=^SecurinetsENIT\\{)(?=.*\\}$)"
    r"(?=^.{15}r3g3x) ..."
)
```

The abbreviated portion represents the remaining constraints. In the actual
file, each positional constraint has the form `^.{N}literal`.

The final line restricts the alphabet:

```text
[A-Za-z0-9_{}]+$
```

Therefore every character must be alphanumeric, an underscore, or a brace.

## 3. Recover the length and fixed wrapper

The first lookahead is:

```text
(?=^.{42}$)
```

The candidate must contain exactly 42 characters.

Two other lookaheads reveal the wrapper:

```text
(?=^SecurinetsENIT\{)
(?=.*\}$)
```

So the candidate starts with:

```text
SecurinetsENIT{
```

and ends with `}`.

## 4. Understand the positional lookaheads

The remaining constraints are:

```text
(?=^.{15}r3g3x)
(?=^.{20}_)
(?=^.{21}constraints)
(?=^.{32}_are_)
(?=^.{36}_)
(?=^.{37}code$)
```

`.{N}` means â€œskip exactly N characters from the beginning.â€ The literal
that follows starts at zero-based offset `N`.

For example:

```text
^.{15}r3g3x
```

means:

```text
candidate[15:20] == "r3g3x"
```

The extracted assignments are:

| Offset | Bytes |
|---:|---|
| 0â€“14 | `SecurinetsENIT{` |
| 15â€“19 | `r3g3x` |
| 20 | `_` |
| 21â€“30 | `constraints` |
| 32â€“36 | `_are_` |
| 36 | `_` |
| 37â€“40 | `code` |
| 41 | `}` |

The overlapping `_are_` and `_` constraints are consistent: the underscore
at offset 36 is the separator before `code`.

## 5. Reconstruct the candidate

Placing the pieces in order gives:

```text
SecurinetsENIT{r3g3x_constraints_are_code}
```

The length is 42 characters, so the reconstruction is complete.

## 6. Verify against the checker

Run the validator with the recovered candidate:

```powershell
python attachment\validator.py "SecurinetsENIT{r3g3x_constraints_are_code}"
```

The checker should accept it. The included solver automates the same process:

```powershell
python src\solve.py attachment\validator.py
```

## 7. Main lesson

Regular expressions can contain a complete constraint system. Lookaheads do
not consume input, so several of them can independently constrain the same
candidate. When reversing such a checker, translate every `^.{N}literal`
constraint into an offset assignment before attempting to execute or fuzz it.
