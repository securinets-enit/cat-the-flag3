'use strict';

// Mirage maintenance worker: "rebuilds the search index." Flavour only — the
// real work is irrelevant; it exists so the admin endpoint has a Node child to
// fork(). The exploitable surface is the fork() call, not anything in here.

console.log('[worker] rebuilding search index...');
setTimeout(() => {
  console.log('[worker] index rebuild complete.');
  process.exit(0);
}, 300);
