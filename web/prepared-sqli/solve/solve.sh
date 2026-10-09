#!/usr/bin/env bash
# Reference solver wrapper for prepared-sqli.
# Usage: ./solve.sh http://HOST:8008
set -euo pipefail
BASE="${1:?usage: solve.sh http://HOST:8008}"
exec python3 "$(cd "$(dirname "$0")" && pwd)/solve.py" "$BASE"
