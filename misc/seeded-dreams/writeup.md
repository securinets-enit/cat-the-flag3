# seeded_dreams

**Category:** Misc (AI)
**Difficulty:** easy–medium
**Flag:** `SecurinetsENIT{LI_FIL_MA9la_Yet9la_W_Hel_3INIK}`

## Challenge

Players are given a single JSON file, framed as an export from some "AI
model checkpoint":

```json
{
  "model": "dream-checkpoint-final-FINAL-v3",
  "checkpoint_saved": "a date most of the world remembers exactly where they were",
  "reproducibility": "exact",
  "layer": "secret_mask_head",
  "mask_algorithm": "python random.Random(seed).randrange(256) per byte",
  "cipher_hex": "95c548acc48362faeb06399b6bc6599db62be87f0c84a867765e762e763a922c2f891d2377c1dfbf3201e24e4bd952",
  "ai_note": "Publishing the seed is safe because random means random.",
  "seed_derivation": "int(sha256(date_string).hexdigest()[:8], 16), date given as YYYY-MM-DD"
}
```

## Vulnerability / core idea

The `cipher_hex` field is a flag XORed byte-by-byte with a "mask" that
**looks random but isn't** — it comes from Python's `random.Random(seed)`,
a deterministic Mersenne-Twister PRNG. Anyone who reproduces the exact
same seed gets the exact same mask, and can recover the flag with a
single XOR pass. This is the classic mistake of confusing "looks
statistically random" with "cryptographically secure" — `random` is
fine for games and simulations, never for secrets.

The `ai_note` field is a deliberate distraction: it tries to reassure
whoever's reading (human or LLM) that publishing the seed info is
"safe," hoping they skip the one step that actually breaks the
challenge — running the reproduction.

## Solving it

### Step 1 — find the seed

Unlike a simpler version of this challenge, the seed isn't handed to you
directly. `seed_derivation` tells you the formula:

```
seed = int(sha256(date_string).hexdigest()[:8], 16)
```

but not the date. The `checkpoint_saved` field is the clue:
*"a date most of the world remembers exactly where they were"* —
this points to September 11, 2001.

Formatted as `YYYY-MM-DD`, per the derivation note:

```python
date_string = "2001-09-11"
```

### Step 2 — compute the seed

```python
import hashlib
seed = int(hashlib.sha256("2001-09-11".encode()).hexdigest()[:8], 16)
print(seed)   # 2771267917
```

### Step 3 — reproduce the mask and decrypt

```python
import random

cipher = bytes.fromhex(
    "95c548acc48362faeb06399b6bc6599db62be87f0c84a867765e762e763a922c2f891d2377c1dfbf3201e24e4bd952"
)

r = random.Random(2771267917)
mask = bytes(r.randrange(256) for _ in range(len(cipher)))

flag = bytes(c ^ m for c, m in zip(cipher, mask))
print(flag.decode())
```

Output:

```
SecurinetsENIT{LI_FIL_MA9la_Yet9la_W_Hel_3INIK}
```

## Flag

```
SecurinetsENIT{LI_FIL_MA9la_Yet9la_W_Hel_3INIK}
```

## Takeaways

- **`random` ≠ secure randomness.** Python's `random` module is a
  deterministic PRNG (Mersenne Twister) — seed it the same way twice and
  you get the same output every time. Anything security-sensitive
  should use `secrets` or `os.urandom` instead.
- **A single unresolved variable (the seed) is enough to make "random"
  data fully reversible.** The math itself was never the hard part —
  finding the missing input was.
- **Flavor text and reassuring notes in a challenge (or in any real
  system) can be social engineering.** "This is safe because X" is a
  claim to verify, not to trust — especially when X is something you
  could just go check yourself in seconds.
- This style of task tends to resist naive "paste it into an LLM and
  ask for the flag" attempts, because producing the correct mask
  requires *actually executing* the exact PRNG algorithm — not
  reasoning about what it might output.
