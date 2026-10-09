# 09 · hash-collision (medium)

A verifier grants a token when two different API keys share an MD5 signature, and
it shows its own check:
```php
if ($a !== $b && md5($a) == md5($b)) {
    grant_legacy_access();
}
```
Keys must be alphanumeric, 5–40 characters. The bug is the loose `==` — you don't
need a real MD5 collision.

## Vulnerability
PHP's `==` compares two numeric strings as numbers. An MD5 digest that is `0e`
followed by only digits is a valid numeric string in scientific notation worth
`0 × 10^n = 0`. Any two inputs whose digests both match `^0e\d+$` ("magic hashes")
satisfy `md5($a) == md5($b)` — both sides are `0` — while the strings differ.
(Still true in PHP 8; only number-vs-non-numeric-string comparisons were
tightened.)

## Exploitation
Use two known magic-hash strings, both alphanumeric and within the length filter:

| input | `md5(input)` |
|---|---|
| `240610708` | `0e462097431906509019562988736854` |
| `QNKCDZO`   | `0e830400451993494058024219903391` |

```
curl --data 'a=240610708' --data 'b=QNKCDZO' http://HOST:8009/
```

## Flag
```
SecurinetsENIT{l00s3_c0mp4r3_c0ll1d3s_0e_h4sh3s}
```

## Fix
- Compare with `hash_equals()` (constant-time) or strict `===`, which never coerces
  `0e…` to a number.
- Where a signature is meant, use `hash_hmac()` with a server secret and verify with
  `hash_equals()`.
- Treat any user value flowing into `==` as a type-confusion risk.
