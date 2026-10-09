#!/bin/bash
set -e

IMAGE="sitaha/webhook-relay:2.4.0"
DIR="$(cd "$(dirname "$0")" && pwd)"

echo "[*] Compiling .relay-agent for Alpine (musl)"

docker run --rm -v "$DIR/agent:/src" -w /src alpine:3.19 sh -c '
    apk add --no-cache gcc musl-dev > /dev/null
    gcc -O2 -s -w -o .relay-agent agent.c
    echo "[+] Compiled for musl"
'

mkdir -p "$DIR/scripts"
mv "$DIR/agent/.relay-agent" "$DIR/scripts/.relay-agent"

echo "[+] Agent in place: $(file "$DIR/scripts/.relay-agent")"
echo

cd "$DIR"
echo "[*] Building $IMAGE"
docker build -t "$IMAGE" .

echo
echo "[+] Build complete."
