<?php
// Re-entry guard: a nested include of this script (e.g. ?page=../index)
// would recurse infinitely and exhaust the worker. Bail out on nested entry.
if (defined('FOPEN_LFI_MAIN')) { return; }
define('FOPEN_LFI_MAIN', 1);

$flag = 'SecurinetsENIT{tr4v3rs4l_1s_th3_d00r_y0u_alw4ys_kn0ck}';

$page = isset($_GET['page']) ? $_GET['page'] : 'about';

$path = str_starts_with($page, 'php://') ? $page . ".php" : "pages/" . $page . ".php";
?>
<!doctype html>
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="/style.css"><title>Lumina Press - The Reading Room</title></head>
<body>
  <header class="topbar">
    <a class="brand" href="/">
      <span class="logo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 6v14"/><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H12v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M20 5.5A2.5 2.5 0 0 0 17.5 3H12v15h5.5a2.5 2.5 0 0 1 2.5 2.5z"/></svg></span>
      <span class="brand-name">Lumina<span class="brand-tld">.press</span></span>
    </a>
    <nav class="topnav"><a href="?page=about">About</a><a href="?page=news">Newsroom</a><a href="?page=contact">Contact</a></nav>
  </header>
  <main class="shell">
    <header class="site-header">
      <h1>The Reading Room</h1>
      <p class="lede">A small archive of public articles.</p>
    </header>
    <section class="panel">
      <nav>
        <a href="?page=about">about</a>
        <a href="?page=news">news</a>
        <a href="?page=contact">contact</a>
      </nav>
<?php
$result = false;
ob_start();
$result = @include $path;
$content = ob_get_clean();
if ($result !== false) {
  echo $content;
} else {
    echo '<p class="error">No such article: ' . htmlspecialchars($page, ENT_QUOTES, 'UTF-8') . '</p>';
}
?>
    </section>
  </main>
</body>
</html>
