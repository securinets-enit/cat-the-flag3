# 00 · recon (warmup)

A near-empty page. The goal is to find content that exists but isn't linked.

## Vulnerability
"Hidden" paths are not access control. The home page source carries a developer
comment pointing at `robots.txt`, and `robots.txt` lists internal paths that are
still fully reachable.

## Exploitation
1. View the page source:
   ```html
   <!-- Ops keeps the crawler rules in robots.txt — don't index the internal stuff. -->
   ```
2. Fetch `/robots.txt`:
   ```
   Disallow: /assets/
   Disallow: /internal-notes-9f2a1c/
   ```
3. Browse the hidden path directly: `/internal-notes-9f2a1c/notes.txt`.

## Flag
```
SecurinetsENIT{r0b0ts_txt_1s_n0t_4_s3cur1ty_c0ntr0l}
```

## Fix
`robots.txt`, HTML comments and unlinked directories are discovery hints, never a
boundary. Protect sensitive files with authentication, not obscurity.
