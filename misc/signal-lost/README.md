# Signal Lost

**Category:** Misc  
**Difficulty:** Medium  
**Runtime:** GNU Octave or MATLAB

## Story

A satellite transmitted a message as a sampled waveform. The receiver kept the
processed signal, but the original text was discarded. Recover the message and
submit it as the flag.

## Files

- `challenge.m` - local verifier and signal encoder
- `target_signal.m` - captured waveform
- `flag.txt` - organizer flag; remove it from the player bundle
- `Dockerfile` - optional GNU Octave environment
- `docker-compose.yml` - optional container runner

## Running locally

With GNU Octave:

```text
octave --quiet challenge.m
```

The program asks for a candidate flag and prints its distance from the target
waveform. A correct candidate produces a distance close to zero.

The source is intentionally available: the intended solve is to understand the
signal representation, inspect the target, and reverse the encoding. Do not
brute-force the flag.

The checker accepts the complete flag, including the prefix and braces.
