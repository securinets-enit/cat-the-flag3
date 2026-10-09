# Task 5 — The Beacon

Difficulty: Hard
Category: Network Forensics
Flag: SecurinetsENIT{4b094f5e62c3ca3257c2571d8ab1d059}

## Scenario

The SOC flagged workstation-04 for unusual outbound traffic. Analysts
captured 60 seconds at the victim's home gateway. The capture contains
normal developer traffic mixed with the activity under investigation.

## Evidence

    https://cdnjs-mirror.net/evidence/beacon.pcapng

## Interface

    nc <ctf-host> 9996

39 questions, 3 attempts each.

## Walkthrough

### Triage (Q1–6)

    tshark -r beacon.pcapng -q -z endpoints,ip | grep -cE '^[0-9]'
    # 50

    tshark -r beacon.pcapng -q -z io,phs
    # tcp dominates

    tshark -r beacon.pcapng -Y 'tls.handshake.extensions_server_name' -T fields -e tls.handshake.extensions_server_name | sort | uniq -c | sort -rn

Top SNI:

    9  gh-actions-runner.xyz
    4  chrome.cloudflare-dns.com
    2  e2c3.gcp.gvt2.com

gh-actions-runner.xyz is the anomaly. Nine hits in sixty seconds.

### Beacon identification (Q7–11)

    tshark -r beacon.pcapng -Y 'tls.handshake.type == 1 and tls.handshake.extensions_server_name == "gh-actions-runner.xyz"' -T fields -e frame.time_relative

    8.849
    9.211
    9.745
    20.110
    31.357
    40.836
    51.087
    61.357
    72.620

Intervals of about ten seconds.

### TLS deep dive (Q17–21)

    tshark -r beacon.pcapng -Y 'tls.handshake.type == 2' -T fields -e tls.handshake.ciphersuite | sort -u
    # 0x1301, 0x1302, 0xc02b
    # 0x1301 = TLS_AES_128_GCM_SHA256

    tshark -r beacon.pcapng -Y 'tls.handshake.type == 1 and tls.handshake.extensions_server_name == "gh-actions-runner.xyz"' -T fields -e tls.handshake.ja3 | sort -u
    # 20b279993ae2e137e62b9647c6d768fb

    tshark -r beacon.pcapng -Y 'tls.handshake.type == 11' -V 2>/dev/null | grep -E "commonName|organizationName" | sort -u
    # CN=gh-actions-runner.xyz
    # CN=WE1, O=Google Trust Services

### Attribution (Q22–27)

    tshark -r beacon.pcapng -q -z endpoints,ip

34.170.160.245 dominates. That is Cloudflare. Cloudflare terminates TLS
with a legitimate certificate for any domain. The certificate proves
Cloudflare is in the path, not that the domain is trustworthy.

## Answers

    1.  50
    2.  192.168.1.141
    3.  34.170.160.245
    4.  tcp
    5.  admin
    6.  gh-actions-runner.xyz
    7.  gh-actions-runner.xyz
    8.  443
    9.  tcp
    10. 9
    11. 10
    12. automated
    13. heartbeat
    14. 12
    15. gh-actions-runner.xyz
    16. yes
    17. TLS1.3
    18. 20b279993ae2e137e62b9647c6d768fb
    19. TLS_AES_128_GCM_SHA256
    20. gh-actions-runner.xyz
    21. WE1
    22. .xyz
    23. no
    24. cloudflare
    25. google trust services
    26. anyone can get one
    27. 20
    28. 73
    29. 13
    30. 9
    31. smb
    32. telegram
    33. no
    34. 320
    35. 188.114.96.6
    36. T1071.001
    37. TA0011
    38. T1071.004
    39. T1573

## Flag

SecurinetsENIT{4b094f5e62c3ca3257c2571d8ab1d059}

## MITRE

T1071.001 — Application Layer Protocol: Web Protocols
T1573 — Encrypted Channel
T1071.004 — Application Layer Protocol: DNS
T1016 — System Network Configuration Discovery
