# DNS series

Two linked tasks (the second domain is found while investigating the first).

| # | Task | Flags | Infra |
|---|---|---|---|
| 1 | `01-enitt-impersonation` — record enumeration on `enitt.online` | 9 | Cloudflare DNS only |
| 2 | `02-dns-revenge` — delegation + AXFR on `login-aws-amazon.cloud` | 6 | BIND on `dns-ns` VM |

No containers; see `docs/INFRASTRUCTURE.md` for the BIND/Cloudflare setup.
Each task has `solver.sh` to verify the live records.
