#!/bin/bash
# Build and push the Securinets ENIT Docker Basics image
# Author: 7ankalis

set -e

IMAGE="securinets-enit/docker-basics:1.0"

echo "[*] Building $IMAGE"
docker build -t "$IMAGE" .

echo
echo "[*] Verifying the image"
docker image inspect "$IMAGE" --format '{{.Config.Labels}}'
echo

echo "[*] Testing the container"
docker run --rm "$IMAGE" </dev/null || true

echo
echo "[+] Build complete."
echo
echo "To push:"
echo "    docker login"
echo "    docker push $IMAGE"
echo
echo "To run locally:"
echo "    docker run -it $IMAGE"
