# Cloud Forensics — Answer Key

**Flag:** SecurinetsENIT{691eb9f6060e582dddefdd3f27070552}

## Full answer list

| # | Question | Answer |
|---|---|---|
| 1 | What is the AWS account ID in the logs? | 379113716218 |
| 2 | What is the username of the compromised IAM user? | samir.benali |
| 3 | What is the access key ID used by the attacker? | AKIAVQRHQHH5BBB7WXZ6 |
| 4 | What is the source IP of the attacker's requests? | 196.203.130.8 |
| 5 | At what UTC time did the first malicious API call occur? | 2026-10-07T10:27:22Z |
| 6 | What is the first API call made by the attacker? | GetCallerIdentity |
| 7 | What role did the attacker assume? (name only) | OrganizationAccountAccessRole |
| 8 | What is the ARN of the assumed role session? | arn:aws:sts::379113716218:assumed-role/OrganizationAccountAccessRole/attacker-session-2026 |
| 9 | What role session name did the attacker use? | attacker-session-2026 |
| 10 | What role did the attacker use to escalate privileges? (full ARN) | arn:aws:iam::379113716218:role/OrganizationAccountAccessRole |
| 11 | What API call did the attacker use to attempt to hide their tracks? | StopLogging |
| 12 | What is the name of the trail the attacker tried to disable? | management-events |
| 13 | What API call did the attacker use to create a backdoor key? | CreateAccessKey |
| 14 | What is the name of the user the attacker backdoored? | backup-service |
| 15 | What is the access key ID created for the backdoor user? | AKIAVQRHQHH5G2ZCYGFC |
| 16 | How many seconds elapsed between the first and last attack event? | 56 |
| 17 | What is the last event timestamp of the attack? | 2026-10-07T10:28:18Z |

## Notes

- Timestamps are the real values from the capture on 2026-10-07
- If the challenge is regenerated, update answers 5, 16, 17 with new
  timestamps
- Answers 8, 9, 15 reference IDs generated during the attack simulation
- The flag lives in `asker/flag.txt` and is printed by the asker on
  successful completion

## MITRE ATT&CK mapping

| Tactic | Technique | ID |
|---|---|---|
| Initial Access | Valid Accounts: Cloud Accounts | T1078.004 |
| Discovery | Cloud Service Discovery | T1526 |
| Persistence | Account Manipulation: Additional Cloud Credentials | T1098.001 |
| Defense Evasion | Impair Defenses: Disable Cloud Logs | T1562.008 |
| Privilege Escalation | Additional Cloud Roles | T1098.003 |
| Exfiltration | Transfer Data to Cloud Account | T1537 |
