# Cloud series — Leaked AWS Key

Two linked tasks on one compromised AWS account.

| # | Task | Port |
|---|---|---|
| 1 | `01-cloudtrail` — IAM abuse and S3 exfiltration in CloudTrail | 9995 |
| 2 | `02-ssrf` — SSRF to instance metadata | 9994 |

Each task: `README.md` (brief), `WALKTHROUGH.md`, `answer_key.md`, `asker/` (TCP asker + flag), `evidence/`, `solver.sh`.
`01-cloudtrail` also holds the AWS scripts (`1-setup.sh` … `5-cleanup.sh`, `config.env`) that generated the evidence.

## Deploy

    docker compose up -d --build      # from this directory
