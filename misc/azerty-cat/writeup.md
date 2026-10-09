# AZERTY Cat - Writeup

**Flag:** `SecurinetsENIT{4ZERTY_m4k3s_m3_w4nn4_qu1t_m30w}`

## What we get

```text
Sqlq; / J4qi lqisse ;on PC qllu;e et ;q chqtte :i;i q ;qrche sur le clqvier<<< ...
SecurinetsENIT{$WERTY8;$k#s8;#8z$nn$8au!t8;#)z}
```

The text is almost French, but some letters are swapped: `a` and `q`,
`m` shows up as `;`, apostrophes became `4`.

## The idea

The person pressed keys as they are labelled on a **French AZERTY** keyboard,
but the computer was set to **US QWERTY**. Each physical key therefore
produced its QWERTY meaning instead of its AZERTY one.

So for every character on screen, look up the same physical key on an AZERTY
keyboard:

| Screen (QWERTY) | Meant (AZERTY) | Why |
|---|---|---|
| `q` / `a` | `a` / `q` | swapped letters |
| `w` / `z` | `z` / `w` | swapped letters |
| `;` | `m` | `m` sits where QWERTY has `;` |
| `m` | `,` | |
| `8` | `_` | `_` is the unshifted 8 key on AZERTY |
| `$` `#` `!` `)` | `4` `3` `1` `0` | AZERTY digits need Shift, Shift+4 on QWERTY is `$` |

The surrounding French message ("J'ai laissé mon PC allumé...") is a free
crib: it lets you confirm each mapping before applying it to the flag.

## Decode

```text
$WERTY8;$k#s8;#8z$nn$8au!t8;#)z
4ZERTY_m4k3s_m3_w4nn4_qu1t_m30w
```

`solve.py` does it with a lookup table.

## Takeaway

Keyboard layouts map **physical keys** to characters. Mixing them up is
a real-world way passwords get "mistyped", and a classic CTF misc trick.
