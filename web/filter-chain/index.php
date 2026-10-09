<?php
$page = isset($_GET['page']) ? (string)$_GET['page'] : 'home';

$blocked = '/(data:|expect:|php:\/\/input|php:\/\/fd|\/var\/log|\/proc\/self|phar:|zip:)/i';
if (preg_match($blocked, $page)) {
    http_response_code(403);
    die("WAF: blocked.");
}

if (preg_match('/^[a-z0-9-]+$/i', $page)) {
    $page = "pages/{$page}.php";
}
if (stripos($page, 'flag.txt') !== false) {
    http_response_code(404);
    die("Not found.");
}
?>
<!doctype html>
<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="/style.css"><title>Pagecraft - Template Renderer</title></head><body>
<header class="topbar">
  <a class="brand" href="/">
    <span class="logo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg></span>
    <span class="brand-name">Pagecraft<span class="brand-tld">.io</span></span>
  </a>
  <nav class="topnav"><a href="?page=home">Home</a><a href="?page=about">Docs</a><a href="?page=login">Sign in</a></nav>
</header>
<main class="shell">
<header class="site-header">
    <h1>Template Renderer</h1>
    <p class="lede">Uploads disabled. Logs unreadable. Most wrappers filtered.</p>
</header>
<section class="panel">
<nav class="site-nav" aria-label="Archive navigation">
    <a href="?page=home">home</a>
    <a href="?page=about">about the renderer</a>
    <a href="?page=news">news</a>
    <a href="?page=contact">contact admin</a>
    <a href="?page=login">staff login</a>
</nav>
<?php
include($page);
?>
</section>
</main>
</body></html>
