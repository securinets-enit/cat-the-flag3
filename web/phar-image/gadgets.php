<?php
class Renderer {
    public $out;
    public $tpl;
    public function render() {
        file_put_contents($this->out, $this->tpl);
    }
}

class Template {
    public $engine;
    public function __destruct() {
        if (is_object($this->engine) && method_exists($this->engine, 'render')) {
            $this->engine->render();
        }
    }
}
