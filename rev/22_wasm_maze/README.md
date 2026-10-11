# WASM Maze

**Category:** Reverse engineering  
**Difficulty:** Intermediateâ€“Hard  
**Technique:** WebAssembly disassembly and linear-memory inspection

Players receive `attachments/maze.wat`, a WebAssembly text module. The source
is intentionally low-level: the flag is stored in linear memory after a
per-byte transformation and is revealed by calling `unlock`.

This is an offline challenge. Use `wasm2wat`/`wat2wasm` or inspect the WAT
directly; no browser or remote service is needed.
