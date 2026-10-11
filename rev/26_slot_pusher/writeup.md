# Slot Pusher — Complete Walkthrough

## 1. Overview

The attachment is `attachments/slot_pusher.py`. It looks like a small menu
program, but its useful behavior is hidden behind a rotating 42-slot ring.
The challenge is not solved by guessing a flag or by sending decimal ASCII
values. The important input types are different:

```text
menu command -> decimal integer
push value   -> one literal character
```

The intended solution is to reverse the cursor transition, generate a
repeating input cycle, and then decode the accepted byte sequence.

This is an original challenge. It uses a different state layout, stride,
encoding, and flag from the public challenge that inspired the general
technique.

## 2. Read the visible interface

Run the attachment:

```powershell
python attachments\slot_pusher.py
```

The program repeatedly asks for:

```text
1) push byte
2) rewind slot
3) inspect
4) verify
```

The output is deliberately cluttered with state information. Search the
dispatcher and the implementations of commands `1`, `2`, and `4` instead of
trying random input.

## 3. Recover the state representation

The important state is:

```python
slots = [None] * 42
cursor = 0
epoch = 0
```

A push writes at the current cursor, advances by one, and reads exactly one
literal character from standard input:

```text
slots[cursor] = ord(input_character)
cursor = (cursor + 1) mod 42
```

Rewind does not clear the ring. It changes only the cursor and increments the
epoch:

```text
cursor = (cursor + 4) mod 42
epoch = epoch + 1
```

The old slot contents remain in place. That is the key state-machine behavior.

## 4. Distinguish commands from pushed bytes

The menu command is parsed as an integer. The byte after command `1` is read
with a one-character read.

To push the character `A`, send:

```text
1
A
```

Do not send `65`. The program would store the first literal character, `6`.
The solver therefore emits command lines followed by raw one-byte characters.

## 5. Derive the slot stride

One push followed by one rewind has this net movement:

```text
push:   +1
rewind: +4
total:  +5 modulo 42
```

The first few cycles are:

| Cycle | Push position | Cursor after rewind |
|---:|---:|---:|
| 0 | 0 | 5 |
| 1 | 5 | 10 |
| 2 | 10 | 15 |
| 3 | 15 | 20 |
| 4 | 20 | 25 |

The stride is useful because:

```text
gcd(5, 42) == 1
```

Therefore 42 cycles visit every ring slot exactly once. No slot is overwritten
before the full token has been placed.

The state machine looks unlike a normal linear stack: the cursor jumps around,
but the repeated cycle gives a deterministic write order.

## 6. Find the verifier condition

The `verify` command checks:

```text
epoch >= 42
cursor == 12
```

After 42 push/rewind cycles, the cursor returns to zero because
`42 * 5 mod 42 == 0`. Three additional rewinds move it to 12:

```text
0 + 3 * 4 == 12 mod 42
```

The supplied solver emits those final rewinds before command `4`.

## 7. Recover the byte transform

The verifier stores the expected token as encoded bytes. Byte `i` is generated
from the visible flag character with:

```text
stored[i] = decoded[i] XOR ((i * 0x29 + 0x61) & 0xff)
```

XOR is self-inverse, so decoding uses the same operation:

```text
decoded[i] = stored[i] XOR ((i * 0x29 + 0x61) & 0xff)
```

The index starts at zero at the first ring position in verifier order.

## 8. Generate the payload

The solver follows this procedure:

1. Define the organizer token.
2. Encode each character using the index-dependent XOR.
3. Emit `1`, then one literal encoded byte.
4. Emit `2` to advance the cursor by four more positions.
5. Repeat for all 42 bytes.
6. Emit three extra rewinds to reach cursor 12.
7. Emit `4`.

Run the generator:

```powershell
python solver\solve.py > payload.txt
```

The payload contains both newline-delimited commands and literal byte
characters. It must not be rewritten as a list of decimal integers.

## 9. Verify locally

Pipe the generated payload into the attachment:

```powershell
python solver\solve.py | python attachments\slot_pusher.py
```

The final verifier prints:

```text
accepted
```

The accepted encoded bytes decode to:

```text
SecurinetsENIT{slot_cycles_keep_old_truth}
```

## 10. Why common approaches fail

### Sending decimal byte values

The push path reads one character, so `65` stores `6`, not `A`.

### Treating rewind as a clear

Rewind changes only the cursor. Clearing the ring destroys the data written by
earlier cycles.

### Using a constant XOR key

The XOR key changes with the index. A one-byte key cannot decode the entire
token.

### Stopping after 42 writes

The ring may contain the right bytes, but the verifier also requires the
correct epoch and cursor. The final three rewinds establish the required
control state.

## 11. Main lessons

- Menu-driven programs may use different parsers for commands and payloads.
- A cursor-moving ring can preserve a long token without a conventional stack.
- Write down state transitions and calculate the net stride.
- Check coprimality to determine whether a repeated cycle covers every slot.
- Separate control-flow reconstruction from post-processing such as XOR
  decoding.
