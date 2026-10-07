# Cloud Task 2 — SSRF to IMDS

A cloud forensics challenge about a Server-Side Request Forgery
vulnerability that leads to EC2 Instance Metadata Service credential
theft.

## Overview

A SaaS web app runs a URL preview feature. When a user submits a URL,
the backend fetches it and returns the response. The feature doesn't
validate HTTP destinations, allowing access to internal endpoints.

An attacker used the feature to reach the EC2 Instance Metadata Service
(169.254.169.254), extracted the instance role's temporary credentials,
and used them to interact with S3.

## Difficulty

Medium.

## Category

Cloud Forensics.

## Points

500.

## Evidence

- `evidence/nginx-access.log` — web access log (3 SSRF requests)
- `evidence/cloudtrail.json` — CloudTrail events from the abused role

## Interface

    nc askers.ecs-github-actions.xyz 9994

15 questions. 3 attempts each.

## Skills

- Recognizing SSRF payloads in web logs
- Understanding the EC2 Instance Metadata Service
- Distinguishing temporary (`ASIA`) from long-lived (`AKIA`) credentials
- Correlating web logs with CloudTrail events by timestamp
- Identifying EC2 role session ARNs

## Author

7ankalis — Securinets ENIT
