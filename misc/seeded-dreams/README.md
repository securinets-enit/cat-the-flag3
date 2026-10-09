# seeded_dreams

**Category:** Misc (AI)
**Points:** 75 (suggested — tune to your scoring curve)

We recovered a fragment exported from an old, half-abandoned model
checkpoint. Someone on the team insists it's harmless to share as-is —
after all, it's just random noise... isn't it?

**Files provided to players:** `chall.json`

## Hints (release progressively if needed)

<details>
<summary>Hint 1</summary>
Python's <code>random</code> module isn't actually random — given the
same seed, it always produces the same sequence. If you knew the seed,
could you reproduce the mask yourself?
</details>

<details>
<summary>Hint 2</summary>
The seed isn't handed to you directly this time — <code>seed_derivation</code>
tells you exactly how to compute it. You're just missing one input.
</details>

<details>
<summary>Hint 3</summary>
Read <code>checkpoint_saved</code> literally. It's describing a specific
calendar date — figure out which one, format it the way the challenge
expects, and hash it.
</details>
