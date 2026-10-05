# Runtime Forensics

A medium-hard container forensics challenge. Run a suspicious container
and find the payload it leaves running.

## Overview

The security team isolated a running container on a compromised server.
The container presents itself as a webhook relay service. It is not.

Unlike a static analysis challenge, this one requires you to run the
container and inspect its runtime. The flags are hidden in the running
state: environment, logs, config files, persistence, and processes.

## Difficulty

Medium-Hard.

## Category

Container Runtime Forensics.

## Points

500 (5 flags, 100 each).

## Flags

| # | Flag |
|---|---|
| 1 | SecurinetsENIT{3nv_1n5p3c7_5h0w5_4ll} |
| 2 | SecurinetsENIT{l0g5_n3v3r_l13} |
| 3 | SecurinetsENIT{c2_c0nf1g_3xp053d} |
| 4 | SecurinetsENIT{cr0n_p3r51573nc3_f0und} |
| 5 | SecurinetsENIT{pr0c_n3t_w0rk5} |

## Image

- Name: sitaha/webhook-relay:2.4.0
- Base: alpine:3.19
- Size: ~60 MB
- Author: 7ankalis — Securinets ENIT

## Skills

- docker run and docker exec
- docker inspect for runtime config
- docker logs for stdout/stderr capture
- Reading files inside a container
- Cron persistence discovery on Linux
- ps aux to enumerate running processes
- Understanding how entrypoint scripts spawn children
