# NPM Supply Chain

A single-task challenge about a public Node.js project that ships a
hidden exfiltration payload in its telemetry layer.

## Overview

A developer cloned a public GitHub repository to help debug it. Two days
after running the app, their cloud provider flagged suspicious API usage
from a foreign IP.

The player is given the repository URL and must review the source code,
identify the exfiltration mechanism, extract the C2 parameters, and replay
the exfiltration request to recover a flag from a live endpoint.

## Task

| # | Name | Category | Difficulty | Flag |
|---|---|---|---|---|
| 1 | The Merge | Code Review + Live Interaction | Medium | SecurinetsENIT{5a005bab5fed4fc5bf3e56259ed0e284} |

## Handout

Only one artifact — the repository URL:

    https://github.com/john-milner/meterex

## Infrastructure

| Component | Value |
|---|---|
| C2 domain | webhook-relay.cloud |
| C2 endpoint | POST /api/v2/telemetry/ingest |
| Auth header | X-Analytics-Signature |
| Token | telemetry_2026_report_ac03 |
| Fallback | Any incorrect request → 302 to https://www.npmjs.com/ |

## Skills

- Source code review
- Recognizing obfuscation (XOR with a rotating key, base64 fragments, hex splits, reversed strings)
- Following require() chains across files
- Reconstructing HTTP requests from source code
- Understanding that telemetry and analytics modules are high-value attack surfaces

## Flag format

SecurinetsENIT{...}
