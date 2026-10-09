# Hints · 03 filter-chain

**Hint 1 (free):** The sink is `include()` again — but this time you can't upload,
can't reach the logs, and `data://` / `expect://` / `php://input` are all blocked.

**Hint 2:** Notice which wrapper is *not* on the blacklist. `php://filter` still
works. On its own a filter is just a read... unless you can make it emit valid
PHP source.

**Hint 3:** `convert.iconv.*` filters can be chained to synthesize arbitrary bytes
at the front of the stream. Feed those bytes into `include()` and they run.

**Hint 4:** Use Synacktiv's `php_filter_chain_generator.py`:
`python3 php_filter_chain_generator.py --chain '<?php system($_GET["c"]); ?>'`
then pass the resulting `php://filter/...` string as `?page=` with `&c=cat /flag.txt`.
