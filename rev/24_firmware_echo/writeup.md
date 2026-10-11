# Firmware Echo â€” Complete Walkthrough

## 1. Challenge goal

The attachment is `attachments/router.fw`, a small custom firmware image.
It contains a header, a filesystem-like payload, and fixed-size records stored
in an unusual order.

The task is to parse the image, find the configuration record, and reverse the
byte-wise encoding used for the flag.

## 2. Validate the firmware header

Read the first 16 bytes. The layout is:

```text
offset  size  field
0       4     magic: FIRM
4       1     version
5       1     architecture
6       2     reserved
8       4     payload length, little-endian
12      4     CRC32 of the payload
```

The first check is:

```python
data[:4] == b"FIRM"
```

Then unpack the length and CRC using little-endian fields:

```python
version, arch, reserved, length = struct.unpack("<BBHI", data[4:12])
expected_crc = struct.unpack("<I", data[12:16])[0]
payload = data[16:16 + length]
```

Validate integrity before carving records:

```python
if zlib.crc32(payload) & 0xffffffff != expected_crc:
    raise ValueError("firmware CRC mismatch")
```

## 3. Locate the embedded filesystem

The payload begins with:

```text
FWS1
```

Immediately after that marker is a four-byte little-endian table length:

```python
if payload[:4] != b"FWS1":
    raise ValueError("missing filesystem marker")

table_len = struct.unpack("<I", payload[4:8])[0]
table = payload[8:8 + table_len]
```

The table is made of 96-byte records. The records were stored in reverse
order, so do not assume the first record is the interesting one. Split the
table into fixed-size blocks and inspect each block:

```python
records = [
    table[offset:offset + 96]
    for offset in range(0, len(table), 96)
]
```

## 4. Find `config.bin`

Search for the record whose beginning is the filename:

```python
config = next(
    record for record in records
    if record.startswith(b"config.bin")
)
```

The record contains padding, a model marker, and encoded bytes. The useful
marker is:

```text
MODEL=ENIT-GW\0
```

Everything after that marker is the encoded configuration data. Remove trailing
NUL padding:

```python
encoded = config.split(b"MODEL=ENIT-GW\x00", 1)[1].rstrip(b"\x00")
```

## 5. Reverse the XOR encoding

Each encoded byte was generated using:

```text
encoded[i] = flag[i] XOR ((i * 0x41 + 0x23) & 0xff)
```

Because XOR is self-inverting, decode it with the same operation:

```python
decoded = bytes(
    value ^ ((index * 0x41 + 0x23) & 0xff)
    for index, value in enumerate(encoded)
)
```

Decode the result as ASCII:

```python
print(decoded.decode("ascii"))
```

The recovered flag is:

```text
SecurinetsENIT{firmware_echoes_reveal_config}
```

## 6. Verify with the supplied solver

Run:

```powershell
python src\solve.py attachment\router.fw
```

The solver performs the magic, CRC, filesystem marker, record discovery, and
XOR checks in that order. This order is useful when adapting the technique to
real firmware: validate the container first, then carve its contents.

## 7. Main lesson

Firmware reversing often starts with format recognition rather than CPU
disassembly. A custom image may contain familiar elements such as magic bytes,
length fields, CRCs, filesystem markers, filenames, fixed-size records, and
padding. Once the correct record is identified, the final configuration
encoding can be solved independently.

