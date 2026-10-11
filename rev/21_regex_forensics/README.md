# Regex Forensics

**Category:** Reverse engineering  
**Difficulty:** Intermediateâ€“Hard  
**Technique:** Constraint extraction from a generated regular expression

Players receive `attachments/validator.py`. The validator builds one large
regular expression and checks a candidate flag. The goal is to recover the
only string accepted by the expression, not to guess it.

```text
python attachments/validator.py 'candidate'
```

This challenge is offline and needs Python 3.8+. No Docker or remote service
is required.

Keep `flag/`, `src/`, and `writeup.md` private during the event.
