# Silent Beacon - Writeup

## Analysis

The capture is framed by the CCSDS Attached Synchronization Marker (ASM):

```text
1a cf fc 1d
```

Immediately after an ASM is a six-byte CCSDS primary header made of three
big-endian 16-bit words. The APID is the low 11 bits of the first word, the
sequence count is the low 14 bits of the second word, and the packet data
length is the third word plus one.

The dictionary says that APID 100 is `HK_NOMINAL`. Its first payload byte is
the mode field, which must be in the range 0 through 7. Values outside this
range are suspicious, especially when they are printable ASCII.

## Extraction

1. Search for every ASM in `capture.bin`.
2. Parse the six bytes after each ASM as three big-endian words.
3. Keep only packets whose APID is 100.
4. Sort those packets by their 14-bit packet sequence count.
5. Read payload byte 0 from each packet.
6. Keep bytes greater than 7 and decode the printable bytes as ASCII.

The extracted covert message is:

```text
h0us3k33p1ng_4n0m4ly
```

Prepend the challenge flag wrapper:

```text
SecurinetsENIT{h0us3k33p1ng_4n0m4ly}
```

## Reference solver

Run:

```text
python solver.py
```

The solver should print the full flag. The capture includes decoy APIDs,
in-range housekeeping modes, and noise between packets, so searching for
printable strings alone is not sufficient.
