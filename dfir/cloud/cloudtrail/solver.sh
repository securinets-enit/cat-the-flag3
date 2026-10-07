#!/bin/bash
# solver.sh — test the cloud asker end-to-end
# Author: 7ankalis — Securinets ENIT

set -e

PORT=9995

docker rm -f cloud-asker >/dev/null 2>&1 || true

echo "[*] Building and starting the asker"
cd "$(dirname "$0")/asker"
docker build -t cloud-asker:1.0 .
docker run -d --name cloud-asker -p $PORT:9995 cloud-asker:1.0
sleep 2

echo "[*] Connecting to asker on port $PORT"
echo

printf '379113716218\nsamir.benali\nAKIAVQRHQHH5BBB7WXZ6\n196.203.130.8\n2026-10-07T10:27:22Z\nGetCallerIdentity\nOrganizationAccountAccessRole\narn:aws:sts::379113716218:assumed-role/OrganizationAccountAccessRole/attacker-session-2026\nattacker-session-2026\narn:aws:iam::379113716218:role/OrganizationAccountAccessRole\nStopLogging\nmanagement-events\nCreateAccessKey\nbackup-service\nAKIAVQRHQHH5G2ZCYGFC\n56\n2026-10-07T10:28:18Z\n' | nc localhost $PORT

echo
echo "[*] Stopping asker"
docker rm -f cloud-asker >/dev/null 2>&1 || true
