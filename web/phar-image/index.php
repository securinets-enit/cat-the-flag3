<?php
require __DIR__ . '/gadgets.php';

$msg = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['avatar'])) {
    $tmp  = $_FILES['avatar']['tmp_name'];
    $name = basename($_FILES['avatar']['name']);
  $ext  = strtolower(pathinfo($name, PATHINFO_EXTENSION));
    $head = file_get_contents($tmp, false, null, 0, 6);
  if ($ext === 'gif' && ($head === 'GIF89a' || $head === 'GIF87a')) {
        move_uploaded_file($tmp, __DIR__ . "/uploads/" . $name);
        $msg = "Uploaded uploads/" . htmlspecialchars($name);
    } else {
        $msg = "Only GIF images are allowed.";
    }
}

$stat = '';
if (isset($_GET['check']) && $_GET['check'] !== '') {
    $stat = file_exists($_GET['check']) ? "exists" : "missing";
}
?>
<!doctype html>
<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="/style.css"><title>Avataria - Avatar Service</title></head><body>
<header class="topbar">
  <a class="brand" href="/">
    <span class="logo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="10" r="3"/><path d="M6.5 18a5.5 5.5 0 0 1 11 0"/></svg></span>
    <span class="brand-name">Avataria<span class="brand-tld">.io</span></span>
  </a>
  <nav class="topnav"><a href="/">Gallery</a><a href="/">Upload</a><a href="/">Account</a></nav>
</header>
<main class="shell">
<header class="site-header">
  <h1>Avatar Service</h1>
  <p class="lede">Upload an avatar and verify that it is available.</p>
</header>
<section class="panel">
<p><?= $msg ?></p>

<h3>Upload avatar (GIF only)</h3>
<form method="post" enctype="multipart/form-data">
  <input type="file" name="avatar">
  <button>Upload</button>
</form>

<h3>Check avatar</h3>
<form method="get">
  <input name="check" placeholder="uploads/me.gif" value="<?= htmlspecialchars($_GET['check'] ?? '') ?>">
  <button>Check</button>
</form>
<p>Status: <?= htmlspecialchars($stat) ?></p>
</section>
</main>
</body></html>
