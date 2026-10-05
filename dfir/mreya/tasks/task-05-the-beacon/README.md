# Task 5 — The Beacon

**Difficulty:** Hard

## Brief

The SOC flagged `workstation-04` for unusual outbound traffic. Analysts
captured 60 seconds of traffic at the victim's home gateway.

The capture contains a mix of normal developer workstation activity and the
traffic under investigation. Filter the noise, identify the beacon, and
characterize the C2 infrastructure.

## Evidence

Download the capture from the CTF host:

    https://cdnjs-mirror.net/evidence/beacon.pcapng

## Running

    nc <ctf-host> 9996

Answer the 39 questions. You have 3 attempts per question.

Tools: `tshark`, `Wireshark`, `tcpdump`.

## Flag format

`SecurinetsENIT{...}`
