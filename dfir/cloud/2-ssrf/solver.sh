#!/bin/bash
set -e

PORT=9994
DIR="$(cd "$(dirname "$0")" && pwd)"

docker rm -f ssrf-asker >/dev/null 2>&1 || true

cd "$DIR/asker"
docker build -t ssrf-asker:1.0 .
docker run -d --name ssrf-asker -p $PORT:9994 ssrf-asker:1.0
sleep 2

printf '98.87.168.89\n/preview\nurl\n154.108.154.113\ncurl/8.5.0\nfile\n169.254.169.254\nwebapp-preview-role\nASIAVQRHQHH5IDT6H2UK\nv1\nGetCallerIdentity\nListBuckets\narn:aws:sts::379113716218:assumed-role/webapp-preview-role/i-0a00ce44211fc98ae\ni-0a00ce44211fc98ae\n2\n' | nc localhost $PORT

echo
echo "[*] Stopping asker"
docker rm -f ssrf-asker >/dev/null 2>&1 || true
