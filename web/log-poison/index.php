<?php
// Re-entry guard: including this script within itself (e.g. ?page=index.php)
// recurses infinitely and exhausts the worker. Bail out on nested entry.
if (defined('QUILLPAD_MAIN')) { return; }
define('QUILLPAD_MAIN', 1);

$page = isset($_GET['page']) ? (string)$_GET['page'] : 'home';

$blocked = '/(php:\/\/|data:|expect:|phar:|zip:|glob:|ftp:|http:)/i';
if (preg_match($blocked, $page)) {
    http_response_code(403);
    die("WAF: wrapper blocked.");
}

?>
<!doctype html>
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="/style.css"><title>Quillpad - Team Notes</title></head>
<body>
  <header class="topbar">
    <a class="brand" href="/">
      <span class="logo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 4 9 15l-3.5 1 1-3.5z"/><path d="M14 6.5 17.5 10"/><path d="M5 20h10"/></svg></span>
      <span class="brand-name">Quillpad<span class="brand-tld">.app</span></span>
    </a>
    <nav class="topnav"><a href="?page=home">Home</a><a href="?page=help">Help</a></nav>
  </header>
  <main class="shell">
    <header class="site-header">
      <h1>Team Notes</h1>
      <p class="lede">A quiet internal notebook for the operations team.</p>
    </header>
    <section class="panel">
      <nav><a href="?page=home">home</a><a href="?page=help">help</a></nav>
<?php
$candidate = $page;
if ($candidate === 'home' || $candidate === 'help') {
    $candidate = "pages/{$candidate}.php";
}
if (stripos($candidate, 'flag.txt') !== false) {
  http_response_code(404);
  die("Not found.");
}
include($candidate);
?>
    </section>
  </main>
</body>
</html>
