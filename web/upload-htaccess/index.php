<?php
$msg = '';
$blacklist = ['php','php3','php4','php5','php7','phtml','pht','phar'];

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
    $name = basename($_FILES['file']['name']);
    $ext  = strtolower(pathinfo($name, PATHINFO_EXTENSION));
    $data = @file_get_contents($_FILES['file']['tmp_name']);
    if ($data === false) {
        $data = '';
    }
    if (in_array($ext, $blacklist, true)) {
        $msg = "Blocked: PHP files are not allowed.";
    } elseif (preg_match('/<\?php/i', $data)) {
        // Content scan: reject anything that looks like a PHP script.
        $msg = "Blocked: file contents look like PHP code.";
    } else {
        move_uploaded_file($_FILES['file']['tmp_name'], __DIR__ . "/uploads/" . $name);
        $msg = "Stored uploads/" . htmlspecialchars($name);
    }
}
?>
<!doctype html>
<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="/style.css"><title>Framea - Gallery Upload</title></head><body>
<header class="topbar">
    <a class="brand" href="/">
        <span class="logo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="8.5" cy="9.5" r="1.5"/><path d="m21 16-5-5L7 20"/></svg></span>
        <span class="brand-name">Framea<span class="brand-tld">.gallery</span></span>
    </a>
    <nav class="topnav"><a href="/">Gallery</a><a href="/uploads/">Uploads</a><a href="/">Teams</a></nav>
</header>
<main class="shell">
<header class="site-header">
    <h1>Gallery Upload</h1>
    <p class="lede">Share an image with the team gallery.</p>
</header>
<section class="panel">
<p><?= $msg ?></p>
<form method="post" enctype="multipart/form-data">
  <input type="file" name="file">
  <button>Upload</button>
</form>
<p>Uploads are served from <a href="/uploads/">/uploads/</a>. PHP files and PHP code are blocked.</p>
</section>
</main>
</body></html>
