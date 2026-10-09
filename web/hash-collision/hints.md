# Hints · 09 hash-collision

**Hint 1 (free):** The page prints the exact check. You need two **different**
alphanumeric keys whose MD5 hashes are treated as equal by PHP's `==`. Note it's
`==`, not `===`.

**Hint 2:** PHP's loose `==` compares two numeric-looking strings as numbers. An
MD5 that looks like `0e123456…` (a `0`, an `e`, then only digits) is read as
scientific notation: `0 × 10^n = 0`. Two such hashes both equal `0`.

**Hint 3:** So you don't need a real cryptographic collision — you need two
inputs whose MD5 digests are each `0e` followed by *only digits* ("magic
hashes"). These are well documented.

**Hint 4:** Classic pair:
```
a=240610708   md5 = 0e462097431906509019562988736854
b=QNKCDZO     md5 = 0e830400451993494058024219903391
```
Submit both; `md5($a) == md5($b)` is `0 == 0` → true, and `$a !== $b`.
