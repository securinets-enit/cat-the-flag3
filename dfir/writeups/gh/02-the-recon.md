# Task 2 — The Recon

Difficulty: Medium
Category: Domain Intelligence
Flag: SecurinetsENIT{9b6d946fc44eb755d906b366c7c794f1}

## Scenario

Passive reconnaissance on the delivery domain before touching the malicious file.

## Interface

    nc <ctf-host> 9999

14 questions, 3 attempts each.

## Walkthrough

Answers in order:

    1.  2026-04-30
    2.  godaddy
    3.  carl.ns.cloudflare.com,ivy.ns.cloudflare.com
    4.  104.21.95.116,172.67.144.188
    5.  cloudflare
    6.  ye1
    7.  letsencrypt
    8.  2026-09-16
    9.  2026-12-15
    10. 90
    11. *.cdnjs-mirror.net,cdnjs-mirror.net
    12. a3f54b3a3cf50036d8448e6b26c6ef71f14bae603e5f7f7d6bd318f3cf89d8dd
    13. technology / web & hosting
    14. suspicious

## Tools

    whois cdnjs-mirror.net
    dig A cdnjs-mirror.net +short
    dig NS cdnjs-mirror.net +short
    whois <ip>
    openssl s_client -connect cdnjs-mirror.net:443 -servername cdnjs-mirror.net

## Why it's suspicious

A six-month-old .net domain, fronted by Cloudflare, with a short-lived
Let's Encrypt certificate. That combination mimics a legitimate CDN but is
not verified by any tier-1 vendor.

## Flag

SecurinetsENIT{9b6d946fc44eb755d906b366c7c794f1}

## MITRE

T1583.001 — Acquire Infrastructure: Domains
T1595 — Active Scanning
