# Cloud Forensics — Leaked AWS Key

A cloud forensics challenge about a leaked AWS access key, IAM abuse, and
S3 exfiltration.

## Overview

A developer accidentally committed a `.env` file to a public GitHub
repository. The file contained an AWS access key. Within minutes, an
attacker found it and began interacting with the AWS account.

The security team captured 60 minutes of CloudTrail events from the
compromised account. The player must read the logs, reconstruct the
attack, and answer questions via a TCP asker.

## Difficulty

Medium.

## Category

Cloud Forensics.

## Points

500.

## Evidence

- `evidence/cloudtrail.json` — real CloudTrail capture

## Interface

    nc askers.ecs-github-actions.xyz 9995

17 questions. 3 attempts per question.

## Skills

- Reading CloudTrail JSON structure
- Filtering events by access key or role
- Recognizing AssumeRole as privilege escalation
- Detecting cover-up attempts (StopLogging)
- Identifying persistence (CreateAccessKey)
- Building attack timelines from eventTime fields

## Author

7ankalis — Securinets ENIT
