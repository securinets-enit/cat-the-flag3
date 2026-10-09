# Silent Beacon

**Category:** Misc / Space Comms / RF  
**Difficulty:** Medium  
**Points:** 492

A ground-station capture contains CCSDS Space Packets mixed with unrelated RF
noise. Recover the hidden message from the housekeeping telemetry.

## Files

- `capture.bin` - raw capture containing synchronization markers and packets
- `packet_ids.txt` - packet inventory supplied by the ground station
- `telemetry_dictionary.json` - protocol and field documentation

The expected flag is:

```text
SecurinetsENIT{h0us3k33p1ng_4n0m4ly}
```

The flag is intentionally not needed to solve the challenge; it is included
in this repository as the organizer answer key.
