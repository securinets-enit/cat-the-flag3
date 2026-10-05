# Task 4 — The Implant

Difficulty: Hard
Category: Binary + Network Forensics
Flag: SecurinetsENIT{5398f82818903750fc0d72e94c5f3304}

## Scenario

The IR team recovered the second-stage binary, a network capture of the
beaconing, and host-side telemetry. Correlate all three to answer 30
questions.

## Evidence

- gh-completion — ELF implant
- traffic.pcapng — network capture
- filesystem/ — hash, size, permissions, cron
- process/ — PID, PPID, cwd, exe path, status
- network/ — sockets, FDs, DNS

## Interface

    nc <ctf-host> 9997

## Walkthrough

### Static binary (Q1–8)

    file evidence/gh-completion
    # ELF 64-bit LSB executable, x86-64, stripped

    ls -la evidence/gh-completion
    # 19969992 bytes

    cat evidence/filesystem/md5.txt
    # afad825988139b2ab9a72611d4717ce5

    cat evidence/filesystem/sha256.txt
    # 13352c0c87c485a1616d6bde5037005cd4f68249f5061d51273a2f8af5403f93

    cat evidence/filesystem/stat.txt
    # owner root, mode 0755

### Process telemetry (Q9–15)

    cat evidence/process/ps-target.txt
    # PID 2552, PPID 1, root

    cat evidence/process/proc-cwd.txt
    # /tmp/gh-extract/gh_2.42.1_linux_amd64

    cat evidence/process/proc-exe.txt
    # /root/.local/share/gh-cli/gh-completion

    cat evidence/filesystem/crontab-after.txt
    # 2 entries

### Network (Q16–22)

    tshark -r evidence/traffic.pcapng -Y 'tls.handshake.extensions_server_name' -T fields -e tls.handshake.extensions_server_name | sort -u

Two SNIs: cdnjs-mirror.net and gh-actions-runner.xyz

### Advanced (Q23–30)

    # JA3
    tshark -r evidence/traffic.pcapng -Y 'tls.handshake.extensions_server_name == "gh-actions-runner.xyz"' -T fields -e tls.handshake.ja3 | sort -u
    # 20b279993ae2e137e62b9647c6d768fb

    # TLS version
    tshark -r evidence/traffic.pcapng -Y 'tls.handshake.type == 2' -T fields -e tls.handshake.version | sort -u
    # TLS 1.2

    # Beacon count
    tshark -r evidence/traffic.pcapng -Y 'tls.handshake.type == 1 && tls.handshake.extensions_server_name == "gh-actions-runner.xyz"' -T fields -e frame.time_relative | wc -l
    # 11

## Answers

    1.  elf
    2.  x86-64
    3.  yes
    4.  19969992
    5.  afad825988139b2ab9a72611d4717ce5
    6.  13352c0c87c485a1616d6bde5037005cd4f68249f5061d51273a2f8af5403f93
    7.  root
    8.  0755
    9.  2552
    10. 1
    11. /tmp/gh-extract/gh_2.42.1_linux_amd64
    12. /root/.local/share/gh-cli/gh-completion
    13. 2
    14. */30 * * * *
    15. @reboot
    16. cdnjs-mirror.net
    17. gh-actions-runner.xyz
    18. 443
    19. 10
    20. cloudflare
    21. T1071.001
    22. T1053.003
    23. TLS1.2
    24. 20b279993ae2e137e62b9647c6d768fb
    25. 11
    26. 3
    27. h2
    28. 10
    29. yes
    30. 5

## Flag

SecurinetsENIT{5398f82818903750fc0d72e94c5f3304}

## MITRE

T1071.001 — Application Layer Protocol: Web Protocols
T1573 — Encrypted Channel
T1053.003 — Scheduled Task/Job: Cron
T1027 — Obfuscated Files or Information
