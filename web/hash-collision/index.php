<?php
$flag = trim(@file_get_contents('/flag.txt'));

$a = isset($_POST['a']) ? (string) $_POST['a'] : '';
$b = isset($_POST['b']) ? (string) $_POST['b'] : '';
$msg = '';
$ok = false;

function valid_key($s)
{
    return $s !== '' && ctype_alnum($s) && strlen($s) >= 5 && strlen($s) <= 40;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!valid_key($a) || !valid_key($b)) {
        $msg = 'Both API keys must be alphanumeric, 5–40 characters.';
    } elseif ($a === $b) {
        $msg = 'The two keys must be different.';
    } elseif (md5($a) == md5($b)) {
        $ok = true;
        $msg = 'Signatures match — legacy access granted: ' . $flag;
    } else {
        $msg = 'Signature mismatch — these two keys are not equivalent.';
    }
}
?>
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="/style.css">
  <title>Legacy Signature Verifier</title>
</head>
<body>
<header class="topbar">
  <a class="brand" href="/">
    <span class="logo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 5 6v5c0 4.2 2.9 7.8 7 9 4.1-1.2 7-4.8 7-9V6z"/><path d="m9 12 2 2 4-4"/></svg></span>
    <span class="brand-name">Sigil<span class="brand-tld">.auth</span></span>
  </a>
  <nav class="topnav"><a href="/">Overview</a><a href="/">API</a><a href="/">Keys</a></nav>
</header>
<main class="shell">
  <header class="site-header">
    <h1>Legacy Signature Verifier</h1>
    <p class="lede">Our old partner API authenticates a request pair by their
      MD5 signatures. Two <em>different</em> keys with the same signature unlock
      the legacy access token.</p>
  </header>

  <section class="panel">
    <h3>How verification works</h3>
    <pre class="code">// $a and $b are the two submitted API keys
if ($a !== $b && md5($a) == md5($b)) {
    grant_legacy_access();   // reveals the token
}</pre>

    <form method="post" class="stack">
      <label>API key A <input name="a" value="<?= htmlspecialchars($a, ENT_QUOTES) ?>" autocomplete="off"></label>
      <label>API key B <input name="b" value="<?= htmlspecialchars($b, ENT_QUOTES) ?>" autocomplete="off"></label>
      <button>Verify signatures</button>
    </form>

<?php if ($msg !== ''): ?>
    <div class="<?= $ok ? 'ok' : 'error' ?>"><?= htmlspecialchars($msg, ENT_QUOTES) ?></div>
<?php endif; ?>
  </section>
</main>
</body>
</html>
