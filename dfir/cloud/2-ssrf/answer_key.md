# Cloud Task 2 — Answer Key

**Flag:** SecurinetsENIT{cacea9745843ea2d6823e118a564146c}

## Answers

| # | Question | Answer |
|---|---|---|
| 1 | Public IP of the webapp | 98.87.168.89 |
| 2 | Vulnerable endpoint | /preview |
| 3 | Query parameter | url |
| 4 | Attacker source IP | 154.108.154.113 |
| 5 | Attacker User-Agent | curl/8.5.0 |
| 6 | Blocked URL scheme | file |
| 7 | SSRF target IP | 169.254.169.254 |
| 8 | IAM role name | webapp-preview-role |
| 9 | AccessKeyId from IMDS | ASIAVQRHQHH5IDT6H2UK |
| 10 | IMDS version | v1 |
| 11 | First API call with stolen creds | GetCallerIdentity |
| 12 | Second API call with stolen creds | ListBuckets |
| 13 | Assumed role session ARN | arn:aws:sts::379113716218:assumed-role/webapp-preview-role/i-0a00ce44211fc98ae |
| 14 | EC2 instance ID | i-0a00ce44211fc98ae |
| 15 | Number of CloudTrail events | 2 |

## Flag location

`asker/flag.txt` — read by the asker after all 15 questions pass.

## MITRE ATT&CK mapping

| Tactic | Technique | ID |
|---|---|---|
| Initial Access | Exploit Public-Facing Application | T1190 |
| Credential Access | Unsecured Credentials: Cloud Instance Metadata API | T1552.005 |
| Discovery | Cloud Service Discovery | T1526 |
| Discovery | Cloud Infrastructure Discovery | T1580 |
| Command and Control | Application Layer Protocol: Web Protocols | T1071.001 |

## Regeneration notes

If the challenge is rebuilt:
- Regenerate the EC2 instance (new instance ID)
- Re-run the SSRF attack (new AccessKeyId and session ID)
- Update answers 9, 13, 14 in `asker/asker.go` and `answer_key.md`
- Answers 1, 4, 5, 7, 8, 10, 11, 12 are stable across runs
- Answer 6 is always `file` (the app's blocklist)
- Answer 15 depends on the CloudTrail filter window
