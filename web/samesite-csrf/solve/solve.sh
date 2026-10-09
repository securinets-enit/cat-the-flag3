#!/usr/bin/env bash
# Reference solver wrapper for samesite-csrf.
# Usage: ./solve.sh http://HOST:8007
# Delegates to solve.py (pure HTTP client; the admin bot runs server-side).
set -euo pipefail
BASE="${1:?usage: solve.sh http://HOST:8007}"
exec python3 "$(cd "$(dirname "$0")" && pwd)/solve.py" "$BASE"
