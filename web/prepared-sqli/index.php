<?php
require __DIR__ . '/db.php';

$q    = isset($_GET['q'])    ? (string) $_GET['q']    : '';
$sort = isset($_GET['sort']) ? (string) $_GET['sort'] : 'id';
$dir  = isset($_GET['dir'])  ? (string) $_GET['dir']  : 'asc';

$rows  = [];
$error = '';

try {
    $sql = "SELECT id, title, price FROM products WHERE active = ? AND title LIKE ? ORDER BY {$sort} {$dir}";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([1, '%' . $q . '%']);
    $rows = $stmt->fetchAll();
} catch (PDOException $e) {
    $error = $e->getMessage();
}

function sort_link($col, $q)
{
    $qs = http_build_query(['q' => $q, 'sort' => $col, 'dir' => 'asc']);
    return '?' . $qs;
}
?>
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="/style.css">
  <title>SecureStore Catalog</title>
</head>
<body>
<header class="topbar">
  <a class="brand" href="/">
    <span class="logo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8h12l-1 11a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg></span>
    <span class="brand-name">SecureStore<span class="brand-tld">.io</span></span>
  </a>
  <nav class="topnav"><a href="/">Catalog</a><a href="/source.zip">Source</a><a href="/">Support</a></nav>
</header>
<main class="shell">
  <header class="site-header">
    <h1>SecureStore Catalog</h1>
    <p class="lede">Internal product catalog. Source available for review —
      <a href="/source.zip">download source</a>.</p>
  </header>

  <section class="panel">
    <form method="get" class="searchbar">
      <input type="text" name="q" value="<?= htmlspecialchars($q, ENT_QUOTES) ?>" placeholder="Search products…">
      <button>Search</button>
    </form>

    <p class="muted">Sort by:
      <a href="<?= htmlspecialchars(sort_link('id', $q)) ?>">id</a> ·
      <a href="<?= htmlspecialchars(sort_link('title', $q)) ?>">title</a> ·
      <a href="<?= htmlspecialchars(sort_link('price', $q)) ?>">price</a>
    </p>

<?php if ($error !== ''): ?>
    <div class="error">Database error: <?= htmlspecialchars($error, ENT_QUOTES) ?></div>
<?php endif; ?>

    <table class="grid">
      <thead><tr><th>#</th><th>Product</th><th>Price</th></tr></thead>
      <tbody>
<?php foreach ($rows as $r): ?>
        <tr>
          <td><?= htmlspecialchars((string) $r['id']) ?></td>
          <td><?= htmlspecialchars((string) $r['title']) ?></td>
          <td>$<?= htmlspecialchars((string) $r['price']) ?></td>
        </tr>
<?php endforeach; ?>
<?php if (!$rows && $error === ''): ?>
        <tr><td colspan="3" class="muted">No products match.</td></tr>
<?php endif; ?>
      </tbody>
    </table>
  </section>
</main>
</body>
</html>
