# Signal Lost - Writeup

## Observation

`challenge.m` loads `target_signal.m`, asks for a string, and compares the
candidate waveform with the target. The encoder is:

```matlab
encoded = bitxor(uint8(message), uint8(42));
amplitudes = double(encoded) / 255;
```

Every character is repeated for `samples_per_symbol` samples. Therefore the
target is a sequence of constant-valued blocks. The block length can be read
from `target_signal.m` or detected by looking for changes between adjacent
samples.

## Decode

1. Load `target_signal.m` in Octave/MATLAB.
2. Reshape the vector into one row per symbol.
3. Read one value from each row and multiply it by `255`.
4. Convert the result to integers.
5. Undo the whitening step with XOR `42`.
6. Convert the resulting byte values to ASCII.

A compact Octave decoder is:

```matlab
target_signal;
blocks = reshape(target_signal, samples_per_symbol, []);
encoded = uint8(round(blocks(1, :) * 255));
message = char(bitxor(encoded, uint8(42)));
disp(message);
```

The recovered flag is:

```text
SecurinetsENIT{fft_reveals_the_message}
```

## Verification

Run `octave --quiet challenge.m` and submit the recovered flag. The waveform
distance should be zero (up to floating-point formatting), and the checker
prints `Accepted`.
