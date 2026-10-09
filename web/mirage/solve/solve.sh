#!/usr/bin/env bash
# Reference solver wrapper for mirage.
# Usage: ./solve.sh http://HOST:8010
# Delegates to solve.py (pure stdlib HTTP client).
set -euo pipefail
BASE="${1:?usage: solve.sh http://HOST:8010}"
exec python3 "$(cd "$(dirname "$0")" && pwd)/solve.py" "$BASE"
