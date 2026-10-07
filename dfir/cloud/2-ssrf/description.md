# Cloud Task 2 — SSRF to IMDS

**Difficulty:** Medium
**Category:** Cloud Forensics
**Author:** 7ankalis — Securinets ENIT
**Points:** 500

## Brief

A SaaS company runs a "URL preview" feature on their web app. Users
submit a URL, the backend fetches it, and the response is returned.

The app runs on EC2 with an IAM role attached. The developer thought
blocking `file://` was enough.

An attacker found the app. Logs were pulled. Your job: reconstruct what
happened.

## Evidence

- `evidence/nginx-access.log` — web access log
- `evidence/cloudtrail.json` — CloudTrail events

## Interaction

    nc askers.ecs-github-actions.xyz 9994

You have 3 attempts per question. On success the asker prints the flag.

## Tools

- jq
- grep
- Any text editor

## Hints

- The web log shows every request
- IMDS runs on a link-local address
- Temporary AWS credentials start with `ASIA`
- The CloudTrail log is filtered to a specific role
