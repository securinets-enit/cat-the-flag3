# Thermal Tumble — Complete Walkthrough

## 1. Challenge overview

Open `attachments/index.html` in a Chromium-based browser. The page renders a
small thermal animation and offers two controls:

```text
cycle:       0 through 7
temperature: 30 through 90
```

Most parameter combinations produce deterministic noise. One combination
causes the page to write a hidden recovery stream into its pixel buffer.

The visible animation is a distraction. The intended solution is static
analysis followed by a small brute-force search.

This is an original challenge. It does not reuse the source, assets, flag, or
writeup of the referenced task.

## 2. Inspect the page

The relevant code is in the script near the end of the HTML document. The
controls eventually call:

```javascript
render(cycle, temperature);
```

The canvas dimensions are:

```text
width  = 86
height = 1
```

The page first fills the canvas with noise. It then computes a seed from the
two user-controlled values and chooses whether to write the recovery stream.

Do not spend time understanding the animation loop. The useful data path is
the code that calls `putImageData` and the code that fills the `Uint8ClampedArray`.

## 3. Recover the parameter ranges

The HTML restricts the search space to:

```text
cycle:       0 <= cycle <= 7
temperature: 30 <= temperature <= 90
```

That is only:

```text
8 * 61 = 488
```

combinations. Brute force is practical and is preferable to guessing from
the visual output.

## 4. Understand the acceptance predicate

The page derives a 12-bit selector:

```javascript
const selector =
  ((cycle * 0x31 + temperature * 0x17 + 0x29) ^
   ((cycle + 3) * temperature)) & 0xfff;
```

It also calculates a small temperature check:

```javascript
const band = (cycle * 13 + temperature * 5) % 17;
```

The recovery path is selected only when both values match the constants in the
script:

```text
selector == 0x54f
band == 1
```

Do not assume that the first selector alone is unique. In this range it also
matches several distractor temperatures. The second condition reduces the
result to one pair:

```text
cycle = 6
temperature = 73
```

## 5. Find the hidden pixel layout

For the correct pair, the script does not put the flag text on the page.
Instead, it writes one encoded byte into the red channel of each pixel:

```text
pixel[i].R = encoded[i]
pixel[i].G = (i * 7 + 0x42) & 0xff
pixel[i].B = cycle
pixel[i].A = 0xff
```

The canvas has 86 pixels, but only the first 43 red-channel values are
meaningful. The remaining pixels are padding/noise.

In a browser console, the extraction is:

```javascript
const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");
const pixels = ctx.getImageData(0, 0, 86, 1).data;
const encoded = [];
for (let i = 0; i < 43; i++) {
  encoded.push(pixels[i * 4]);
}
console.log(encoded);
```

The green channel is a consistency check. For every extracted pixel, verify:

```text
G == (i * 7 + 0x42) & 0xff
B == 6
A == 255
```

This prevents accidentally extracting the pre-existing noise buffer.

## 6. Decode the red channel

The builder encoded each flag byte using:

```text
encoded[i] = flag[i] XOR ((i * 0x1d + 0x53) & 0xff)
```

XOR is self-inverse, so the decoder uses the same operation:

```python
flag[i] = encoded[i] ^ ((i * 0x1d + 0x53) & 0xff)
```

The index starts at zero for the first pixel. Do not include the green, blue,
or alpha channels in the XOR operation.

## 7. Reproduce the search in Python

A minimal parameter search is:

```python
for cycle in range(8):
    for temperature in range(30, 91):
        selector = (
            (cycle * 0x31 + temperature * 0x17 + 0x29)
            ^ ((cycle + 3) * temperature)
        ) & 0xfff
        band = (cycle * 13 + temperature * 5) % 17
        if selector == 0x54f and band == 1:
            print(cycle, temperature)
```

This prints:

```text
6 73
```

The supplied solver reproduces the page's pixel generation and decoding:

```powershell
python solver\solve.py
```

It prints the candidate pair, validates the channel metadata, and recovers:

```text
SecurinetsENIT{heat_cycles_hide_the_answer}
```

## 8. Verify in the browser

Open the attachment and set:

```text
cycle       6
temperature 73
```

Use the browser console extraction from Section 5. The decoded red channel
must begin with the CTF prefix and end with `}`. If it does not, check that
the canvas was read after the render completed and that the pixel index is
multiplied by four when accessing the RGBA array.

## 9. Why common approaches fail

### Reading the page text

The flag is never inserted into the DOM. The visible canvas is only a
presentation layer.

### Looking at one pixel

The correct parameter pair is identified by the full selector and band checks.
A single pixel is not sufficient evidence.

### Treating the RGBA array as a byte-per-pixel array

Canvas data is four bytes per pixel. Pixel `i` starts at array offset `i * 4`.

### Decoding every channel

Only the red channel contains the encoded stream. Green, blue, and alpha are
metadata and padding checks.

### Using only the selector condition

The selector has distractor matches in the allowed range. The second
temperature-band condition is required for uniqueness.

## 10. Main lessons

- GPU and canvas challenges often hide data in render outputs rather than
  ordinary strings.
- Small parameter spaces should be searched systematically.
- Reconstructing the exact buffer dimensions and channel layout matters.
- A rendered result can be treated as a structured binary format.
- Separate parameter discovery, buffer extraction, and byte decoding into
  independent steps.
