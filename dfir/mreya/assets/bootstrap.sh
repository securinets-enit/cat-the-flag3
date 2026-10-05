#!/usr/bin/env bash
# bootstrap.sh — creates the entire gh-cli-fake project tree.
# Run this in an empty directory. Produces ./gh-cli-fake/

set -euo pipefail

ROOT="gh-cli-fake"

echo "[*] Creating $ROOT/ tree..."
mkdir -p "$ROOT"/{nginx,logs,certs}
mkdir -p "$ROOT"/site/assets
mkdir -p "$ROOT"/site/downloads

# =====================================================================
# docker-compose.yml
# =====================================================================
cat > "$ROOT/docker-compose.yml" << 'EOF'
version: "3.9"

services:
  nginx:
    image: nginx:1.25-alpine
    container_name: gh-cli-fake
    ports:
      - "80:80"
    volumes:
      - ./site:/var/www/site:ro
      - ./nginx/site.conf:/etc/nginx/conf.d/default.conf:ro
      - ./logs:/var/log/nginx
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost/cf-health"]
      interval: 30s
      timeout: 5s
      retries: 3
EOF
echo "    [+] docker-compose.yml"

# =====================================================================
# nginx/site.conf
# =====================================================================
cat > "$ROOT/nginx/site.conf" << 'EOF'
# ---- Cloudflare real IP extraction ----
set_real_ip_from 173.245.48.0/20;
set_real_ip_from 103.21.244.0/22;
set_real_ip_from 103.22.200.0/22;
set_real_ip_from 103.31.4.0/22;
set_real_ip_from 141.101.64.0/18;
set_real_ip_from 108.162.192.0/18;
set_real_ip_from 190.93.240.0/20;
set_real_ip_from 188.114.96.0/20;
set_real_ip_from 197.234.240.0/22;
set_real_ip_from 198.41.128.0/17;
set_real_ip_from 162.158.0.0/15;
set_real_ip_from 104.16.0.0/13;
set_real_ip_from 104.24.0.0/14;
set_real_ip_from 172.64.0.0/13;
set_real_ip_from 131.0.72.0/22;
set_real_ip_from 2400:cb00::/32;
set_real_ip_from 2606:4700::/32;
set_real_ip_from 2803:f800::/32;
set_real_ip_from 2405:b500::/32;
set_real_ip_from 2405:8100::/32;
set_real_ip_from 2a06:98c0::/29;
set_real_ip_from 2c0f:f248::/32;
real_ip_header CF-Connecting-IP;
real_ip_recursive on;

server {
    listen 80 default_server;
    server_name cdnjs-mirror.net www.cdnjs-mirror.net _;

    root /var/www/site;
    index index.html;

    log_format forensic '$remote_addr - $remote_user [$time_local] '
                        '"$request" $status $body_bytes_sent '
                        '"$http_referer" "$http_user_agent" '
                        'cf_ray="$http_cf_ray" cf_country="$http_cf_ipcountry" '
                        'xff="$http_x_forwarded_for" '
                        'rt=$request_time';

    access_log /var/log/nginx/access.log forensic;
    error_log  /var/log/nginx/error.log warn;

    add_header X-GitHub-Request-Id "E1A2:3F4B:5C6D:7E8F:9A0B" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "deny" always;
    add_header Referrer-Policy "origin-when-cross-origin" always;
    add_header Server-Timing "cfRequestDuration;dur=12.345" always;

    location / {
        try_files $uri $uri/ =404;
        add_header Cache-Control "no-cache";
    }

    location /downloads/ {
        types {
            application/gzip                     tar.gz;
            application/vnd.debian.binary-package deb;
            application/zip                      zip;
        }
        default_type application/octet-stream;
        add_header Content-Disposition "attachment" always;
        add_header cf-cache-status "HIT" always;
    }

    location = /cf-health {
        return 200 "ok\n";
        access_log off;
    }

    location ~ /\. { deny all; }
}
EOF
echo "    [+] nginx/site.conf"

# =====================================================================
# site/index.html
# =====================================================================
cat > "$ROOT/site/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GitHub CLI</title>
  <link rel="stylesheet" href="/assets/style.css">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
</head>
<body>
  <header class="site-header">
    <div class="container header-inner">
      <a href="/" class="brand">
        <img src="/assets/gh-logo.svg" alt="GitHub CLI" width="32" height="32">
        <span>GitHub CLI</span>
      </a>
      <nav class="site-nav">
        <a href="/manual/">Manual</a>
        <a href="/releases/">Releases</a>
        <a href="https://github.com/cli/cli">Source</a>
      </nav>
    </div>
  </header>

  <main>
    <section class="hero">
      <div class="container">
        <h1>Take GitHub to the command line</h1>
        <p class="lede">GitHub CLI brings GitHub to your terminal. It reduces context switching, helps you focus, and helps you script and customize your GitHub workflow.</p>
        <div class="cta-group">
          <a href="/downloads/gh_2.42.1_linux_amd64.tar.gz" class="btn btn-primary" id="download-linux">
            <span class="os-label">Download for Linux</span>
          </a>
          <a href="/downloads/gh_2.42.1_windows_amd64.zip" class="btn btn-secondary">Windows</a>
          <a href="/downloads/gh_2.42.1_darwin_amd64.tar.gz" class="btn btn-secondary">macOS</a>
        </div>
        <p class="version-note">Latest release: <strong>v2.42.1</strong> &middot; Published 3 days ago</p>
      </div>
    </section>

    <section class="install">
      <div class="container">
        <h2>Installation</h2>
        <p>Extract the archive and run the bundled install script:</p>
        <pre class="code-block"><code>tar -xzf gh_2.42.1_linux_amd64.tar.gz
cd gh_2.42.1_linux_amd64
sudo ./install.sh</code></pre>
        <p class="muted">Or install via your package manager:</p>
        <pre class="code-block"><code>sudo apt install ./gh_2.42.1_linux_amd64.deb</code></pre>
      </div>
    </section>

    <section class="release-notes">
      <div class="container">
        <h2>What's new in v2.42.1</h2>
        <ul>
          <li>Improved <code>gh pr create</code> draft handling</li>
          <li>Faster <code>gh repo clone</code> for large repositories</li>
          <li>Fixed authentication refresh edge case on Windows</li>
          <li>Updated bundled dependencies for security patches</li>
        </ul>
        <p class="muted">See the <a href="/releases/">full changelog</a> for details.</p>
      </div>
    </section>

    <section class="checksums">
      <div class="container">
        <h2>Checksums</h2>
        <pre class="code-block"><code>a3f5c8d9e1b2f4a6c7d8e9f0a1b2c3d4  gh_2.42.1_linux_amd64.tar.gz
b4e6d9eae2c3a5b7d8e9f0a1b2c3d4e5  gh_2.42.1_windows_amd64.zip
c5f7eafbf3d4b6c8e9f0a1b2c3d4e5f6  gh_2.42.1_darwin_amd64.tar.gz</code></pre>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container">
      <p>&copy; 2024 GitHub, Inc. &middot; <a href="/terms/">Terms</a> &middot; <a href="/privacy/">Privacy</a></p>
    </div>
  </footer>

  <script>
    (function () {
      const ua = navigator.userAgent;
      const btn = document.getElementById('download-linux');
      if (/Mac/i.test(ua)) {
        btn.href = '/downloads/gh_2.42.1_darwin_amd64.tar.gz';
        btn.querySelector('.os-label').textContent = 'Download for macOS';
      } else if (/Win/i.test(ua)) {
        btn.href = '/downloads/gh_2.42.1_windows_amd64.zip';
        btn.querySelector('.os-label').textContent = 'Download for Windows';
      }
    })();
  </script>
</body>
</html>
EOF
echo "    [+] site/index.html"

# =====================================================================
# site/assets/style.css
# =====================================================================
cat > "$ROOT/site/assets/style.css" << 'EOF'
* { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg: #ffffff;
  --fg: #1f2328;
  --muted: #59636e;
  --border: #d1d9e0;
  --accent: #0969da;
  --btn-primary-bg: #1f883d;
  --btn-primary-hover: #1a7f37;
  --code-bg: #f6f8fa;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans",
    Helvetica, Arial, sans-serif;
  color: var(--fg);
  background: var(--bg);
  line-height: 1.5;
  font-size: 16px;
}

.container { max-width: 1012px; margin: 0 auto; padding: 0 24px; }

.site-header { border-bottom: 1px solid var(--border); padding: 16px 0; }
.header-inner { display: flex; align-items: center; justify-content: space-between; }
.brand {
  display: flex; align-items: center; gap: 8px;
  font-weight: 600; font-size: 16px; color: var(--fg); text-decoration: none;
}
.site-nav a { margin-left: 24px; color: var(--fg); text-decoration: none; font-size: 14px; }
.site-nav a:hover { color: var(--accent); }

.hero { padding: 64px 0; text-align: center; border-bottom: 1px solid var(--border); }
.hero h1 { font-size: 40px; font-weight: 600; margin-bottom: 16px; letter-spacing: -0.02em; }
.lede { color: var(--muted); font-size: 18px; max-width: 640px; margin: 0 auto 32px; }

.cta-group { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-bottom: 16px; }
.btn {
  display: inline-block; padding: 12px 20px; border-radius: 6px;
  font-size: 14px; font-weight: 600; text-decoration: none;
  border: 1px solid transparent; cursor: pointer; transition: background 0.15s ease;
}
.btn-primary { background: var(--btn-primary-bg); color: #ffffff; }
.btn-primary:hover { background: var(--btn-primary-hover); }
.btn-secondary { background: #f6f8fa; color: var(--fg); border-color: var(--border); }
.btn-secondary:hover { background: #eef1f4; }

.version-note { color: var(--muted); font-size: 13px; margin-top: 12px; }

section.install, section.release-notes, section.checksums {
  padding: 48px 0; border-bottom: 1px solid var(--border);
}
section h2 { font-size: 24px; font-weight: 600; margin-bottom: 20px; }

.code-block {
  background: var(--code-bg); border: 1px solid var(--border);
  border-radius: 6px; padding: 16px;
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
  font-size: 13px; overflow-x: auto; margin-bottom: 16px; line-height: 1.6;
}
code {
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
  font-size: 13px; background: var(--code-bg); padding: 2px 6px; border-radius: 4px;
}
pre code { background: none; padding: 0; }
.muted { color: var(--muted); font-size: 14px; }
.release-notes ul { padding-left: 24px; margin-bottom: 16px; }
.release-notes li { margin-bottom: 8px; }
a { color: var(--accent); }
a:hover { text-decoration: underline; }

.site-footer { padding: 32px 0; text-align: center; color: var(--muted); font-size: 13px; }
EOF
echo "    [+] site/assets/style.css"

# =====================================================================
# site/assets/gh-logo.svg
# =====================================================================
cat > "$ROOT/site/assets/gh-logo.svg" << 'EOF'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="32" height="32" fill="#1f2328">
  <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/>
</svg>
EOF
echo "    [+] site/assets/gh-logo.svg"

# =====================================================================
# site/assets/favicon.svg
# =====================================================================
cat > "$ROOT/site/assets/favicon.svg" << 'EOF'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="32" height="32" fill="#1f2328">
  <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/>
</svg>
EOF
echo "    [+] site/assets/favicon.svg"

# =====================================================================
# build-downloads.sh
# =====================================================================
cat > "$ROOT/build-downloads.sh" << 'EOF'
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

  cat > "$WORK/gh" << 'INNER'
#!/bin/bash
echo "gh version 2.42.1 (2024-01-15)"
echo "https://github.com/cli/cli/releases/tag/v2.42.1"
INNER
  chmod +x "$WORK/gh"

  cat > "$WORK/install.sh" << 'INNER'
#!/bin/bash
# GitHub CLI installer — v2.42.1
set -e
echo "[*] GitHub CLI v2.42.1 installer"
echo "[*] Detected architecture: $(uname -m)"
echo "[*] Installing to /usr/local/bin/gh..."
sleep 1
cp "$(dirname "$0")/gh" /usr/local/bin/gh
chmod +x /usr/local/bin/gh
echo "[+] Installation complete."
echo "[+] Run 'gh auth login' to get started."
INNER
  chmod +x "$WORK/install.sh"

  tar -czf "gh_${VERSION}_${PLATFORM}.tar.gz" "$WORK"
  rm -rf "$WORK"
done

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
EOF
chmod +x "$ROOT/build-downloads.sh"
echo "    [+] build-downloads.sh"

# =====================================================================
# .gitignore
# =====================================================================
cat > "$ROOT/.gitignore" << 'EOF'
logs/
certs/
site/downloads/*.tar.gz
site/downloads/*.zip
site/downloads/*.deb
EOF
echo "    [+] .gitignore"

# =====================================================================
# README.md
# =====================================================================
cat > "$ROOT/README.md" << 'EOF'
# gh-cli-fake

Fake GitHub CLI download site used for DFIR CTF scenario authoring.

## Architecture

- Cloudflare (Flex mode) fronts the origin
- Nginx serves static HTML + download tarballs on port 80
- Victim's real IP extracted from `CF-Connecting-IP`

## Quick start

    ./build-downloads.sh
    docker compose up -d
    docker compose logs -f

Origin listens on `0.0.0.0:80`. Point Cloudflare A record at the VM's
static IP, set SSL mode to "Flexible", and enable proxy.

## Evidence

- `logs/access.log` — nginx forensic log (real client IP, UA, referer, cf_ray)
- `site/downloads/` — the served payloads
EOF
echo "    [+] README.md"

# =====================================================================
# Placeholder .gitkeep so logs/ and certs/ survive transfer
# =====================================================================
touch "$ROOT/logs/.gitkeep"
touch "$ROOT/certs/.gitkeep"

echo ""
echo "[+] Done. Project tree:"
echo ""
if command -v tree >/dev/null 2>&1; then
  tree "$ROOT"
else
  find "$ROOT" -type f -o -type d | sort | sed "s|^|    |"
fi
echo ""
echo "Next steps:"
echo "  1. cd $ROOT && ./build-downloads.sh"
echo "  2. Transfer to VM:"
echo "       gcloud compute scp --recurse $ROOT gh-cli-fake-vm:~/ --zone=us-central1-a"
echo "  3. On VM: cd ~/$ROOT && sudo docker compose up -d"
