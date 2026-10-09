# Hints · 00 recon

**Hint 1 (free):** Web recon starts with **View Source**. Read the HTML the server
sent, not just what's rendered.

**Hint 2:** The comment mentions crawler rules. Every site keeps those in one
well-known file.

**Hint 3:** `GET /robots.txt`. `Disallow` entries are a map of things they *don't*
want you to see.

**Solution:** browse the `Disallow`'d `/internal-notes-9f2a1c/` directory.
