# Runtime Forensics

**Difficulty:** Medium-Hard
**Category:** Container Runtime Forensics
**Author:** 7ankalis — Securinets ENIT
**Points:** 500

## Brief

The security team isolated a running container on a compromised server:

    sitaha/webhook-relay:2.4.0

The container presents itself as a webhook relay service. It is not.

Unlike a static analysis challenge, this one requires you to run the
container and inspect its runtime. Five flags are hidden in:

- The container's environment
- The container's logs
- A hidden config file
- A persistence mechanism
- A running process

## Prerequisites

- Docker installed

## Flag format

    SecurinetsENIT{...}

## Hints

- The container config is visible from the host
- Logs are captured by Docker
- Real services leave a trail
- Persistence on Linux is often done via cron
- Arguments passed to running processes are visible
