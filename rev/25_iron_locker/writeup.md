# Iron Locker — Complete Walkthrough

## 1. Challenge overview

Iron Locker is an Android application with a WebView and a native JNI
library. The player receives the source tree under
`attachments/iron_locker_source/` and must recover the flag from the
application logic.

The intended path is:

```text
JavaScript -> WebView bridge -> Java wrapper -> JNI -> stale native handle
         -> allocator reuse -> leaked recovery record -> byte decoding
```

This is an original challenge with a new application name, API, data format,
encoding, and flag. It is inspired only by the broad educational theme of
combining WebView analysis, JNI reversing, memory lifetime bugs, and a
cryptographic post-processing step.

## 2. Start with the Java layer

Open `MainActivity.java`. The WebView enables JavaScript and registers an
object similar to:

```java
webView.addJavascriptInterface(new LockerBridge(), "IronLocker");
```

The bridge exposes methods for creating, deleting, and reading entries. The
important observation is that the JavaScript-visible handle is a `long`, not
an ordinary Java object. That suggests the value is an opaque native pointer
or native identifier.

The bridge also loads the native library:

```java
static {
    System.loadLibrary("ironlocker");
}
```

Follow each `native` declaration to the matching C implementation.

## 3. Trace the JNI implementation

The native source is under `native/ironlocker.c`. The relevant operations are:

```text
locker_create(data) -> handle
locker_delete(handle)
locker_read(handle) -> byte array
```

`locker_create` allocates a small `LockerEntry`, copies the supplied bytes,
and returns its address as a `jlong`.

`locker_delete` frees the entry but does not clear the JavaScript-visible
handle. The native side therefore has no protection against:

```text
handle = create(...)
delete(handle)
read(handle)
```

The read operation dereferences the old address. This is a use-after-free
(UAF), specifically a stale native handle exposed across the Java/JNI
boundary.

## 4. Understand the allocator reuse

The native code uses a fixed-size pool for entries. A freed slot is returned
to the pool's free list. The next allocation of the same size receives the
same slot.

That makes the following sequence deterministic:

```text
old = locker_create("AAAA....")
locker_delete(old)
new = locker_create(controlled bytes)
locker_read(old)
```

The stale `old` handle points to the storage now occupied by `new`.

This is not a random heap spray. The challenge is designed so that one
same-sized allocation immediately reuses the freed slot. The JavaScript
exploit should therefore avoid unnecessary allocations.

## 5. Inspect the record layout

The replacement allocation is a structured record. Its native layout is:

```text
offset  size  field
0       4     magic: ILKR
4       1     version
5       1     record type
6       2     encoded length, little-endian
8       N     encoded recovery blob
```

The leaked bytes returned through the stale handle begin with `ILKR`. This
magic is the confirmation that the allocator reuse worked.

Do not decode every byte returned by the read function blindly. First parse
the header and use the declared length. Any remaining bytes belong to the
native slot's padding.

## 6. Trigger the bug from JavaScript

The supplied exploit is `solver/exploit.html`. Its core sequence is:

```javascript
const stale = IronLocker.create("A".repeat(32));
IronLocker.remove(stale);

const replacement = buildRecoveryRecord();
IronLocker.createBytes(replacement);

const leak = IronLocker.read(stale);
console.log(leak);
```

The replacement handle is deliberately ignored. The stale handle is the one
that matters because it still points to the freed slot.

When the application returns the bytes beginning with `ILKR`, save the
record to a file for offline analysis. A failed magic check usually means the
allocation size did not match or an extra bridge call disturbed the free-list
order.

## 7. Recover the byte transform

The native builder encodes each flag byte with:

```text
encoded[i] = flag[i] XOR ((i * 0x37 + 0x5d) & 0xff)
```

The transform is index-dependent, so using one constant XOR key will not
work. XOR is self-inverse, which means decoding uses exactly the same
operation:

```python
decoded[i] = encoded[i] ^ ((i * 0x37 + 0x5d) & 0xff)
```

Use the first byte of the recovery blob as index zero. Do not include the
`ILKR` header in the index.

## 8. Decode with Python

A minimal decoder is:

```python
def decode(encoded: bytes) -> str:
    plain = bytes(
        value ^ ((index * 0x37 + 0x5d) & 0xff)
        for index, value in enumerate(encoded)
    )
    return plain.decode("ascii")
```

The included solver performs the same parsing and decoding after reading the
captured leak:

```powershell
python solver\solve.py solver\leak.bin
```

The recovered flag is:

```text
SecurinetsENIT{jni_handles_need_lifetimes}
```

## 9. Verify the result

The expected validation order is:

1. The leaked record starts with `ILKR`.
2. The version and record type are accepted.
3. The declared blob length fits inside the leak.
4. The decoded bytes are printable ASCII.
5. The result has the expected CTF flag wrapper.

This sequence distinguishes a real stale-slot leak from arbitrary heap
noise.

## 10. What to learn

### WebView bridge review

Methods exposed through `addJavascriptInterface` become an attack surface.
Treat every JavaScript argument as attacker-controlled, even when the
application appears to be a local utility.

### JNI lifetime review

A pointer converted to `jlong` is not made safe by crossing into Java. Native
allocation ownership, deletion, and handle invalidation still need explicit
management.

### Deterministic allocator reuse

Same-size free-then-allocate sequences can make a UAF reproducible. Before
attempting a complicated heap spray, inspect the allocator's size classes and
free-list behavior.

### Layered reversing

The memory bug only exposes an encoded record. Exploitation and decoding are
separate phases: first prove that the stale handle reaches the replacement
object, then parse and reverse the byte transform.
