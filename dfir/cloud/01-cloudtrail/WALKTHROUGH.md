# Cloud Forensics — Walkthrough

**Author:** 7ankalis — Securinets ENIT
**Interface:** nc askers.ecs-github-actions.xyz 9995

## Overview

The evidence is a CloudTrail JSON file with 45 events. Most are from the
attacker. The player must identify the compromised credentials, trace
the attack sequence, and answer 17 questions.

## Step 1 — Get oriented

    jq '.Records | length' cloudtrail.json

    # 45

    jq -r '.Records[].eventName' cloudtrail.json | sort -u

You'll see IAM, S3, STS, and CloudTrail events. The interesting ones:
GetCallerIdentity, AssumeRole, CreateAccessKey, StopLogging.

## Step 2 — Find the attacker's access key

    jq -r '.Records[] | select(.eventName == "GetCallerIdentity") | "\(.eventTime) \(.userIdentity.accessKeyId) \(.sourceIPAddress)"' cloudtrail.json

Output:

    2026-10-07T10:27:22Z AKIAVQRHQHH5BBB7WXZ6 196.203.130.8

The compromised access key is `AKIAVQRHQHH5BBB7WXZ6`.

## Step 3 — Trace the attack

    jq -r '.Records[] | select(.userIdentity.accessKeyId == "AKIAVQRHQHH5BBB7WXZ6") | "\(.eventTime) \(.eventName) \(.errorCode // "ok")"' cloudtrail.json | sort

Sequence:

    10:27:22  GetCallerIdentity        ok
    10:27:25  ListAttachedUserPolicies AccessDenied
    10:27:29  ListBuckets              AccessDenied
    10:27:33  AssumeRole               ok

The attacker tested the key, tried to enumerate, then escalated to a
higher-privileged role.

## Step 4 — Identify the assumed role

    jq '.Records[] | select(.eventName == "AssumeRole")' cloudtrail.json

Output includes:

    roleArn: arn:aws:iam::379113716218:role/OrganizationAccountAccessRole
    roleSessionName: attacker-session-2026
    assumedRoleArn: arn:aws:sts::379113716218:assumed-role/OrganizationAccountAccessRole/attacker-session-2026

## Step 5 — Cover-up and persistence

    jq -r '.Records[] | select(.eventName == "StopLogging" or .eventName == "CreateAccessKey") | "\(.eventTime) \(.eventName)"' cloudtrail.json | sort

    10:28:10  StopLogging
    10:28:18  CreateAccessKey

The attacker disabled CloudTrail logging and created a backdoor access
key for `backup-service`.

## Step 6 — Timeline

    jq -r '[.Records[] | select(.userIdentity.accessKeyId == "AKIAVQRHQHH5BBB7WXZ6" or (.userIdentity.arn // "" | contains("OrganizationAccountAccessRole"))) | .eventTime] | sort | "\(.[0])  -->  \(.[-1])"' cloudtrail.json

    2026-10-07T10:27:22Z  -->  2026-10-07T10:28:18Z

Duration: 56 seconds.

## Full answer table

| # | Question | Answer |
|---|---|---|
| 1 | AWS account ID | 379113716218 |
| 2 | Compromised IAM user | samir.benali |
| 3 | Attacker access key | AKIAVQRHQHH5BBB7WXZ6 |
| 4 | Attacker source IP | 196.203.130.8 |
| 5 | First malicious API call time | 2026-10-07T10:27:22Z |
| 6 | First API call made | GetCallerIdentity |
| 7 | Assumed role name | OrganizationAccountAccessRole |
| 8 | Assumed role session ARN | arn:aws:sts::379113716218:assumed-role/OrganizationAccountAccessRole/attacker-session-2026 |
| 9 | Role session name | attacker-session-2026 |
| 10 | Role ARN | arn:aws:iam::379113716218:role/OrganizationAccountAccessRole |
| 11 | Cover-up API call | StopLogging |
| 12 | Trail targeted | management-events |
| 13 | Persistence API call | CreateAccessKey |
| 14 | Backdoored user | backup-service |
| 15 | Backdoor access key ID | AKIAVQRHQHH5G2ZCYGFC |
| 16 | Attack duration in seconds | 56 |
| 17 | Last attack event time | 2026-10-07T10:28:18Z |

## What the player learns

- CloudTrail structure: Records array with userIdentity, eventName,
  sourceIPAddress, eventTime
- Pivoting on access key IDs to isolate attack activity
- Recognizing AssumeRole as a privilege escalation pattern
- Spotting cover-up attempts (StopLogging)
- Identifying persistence (CreateAccessKey on a service account)
- Building accurate attack timelines from eventTime fields
