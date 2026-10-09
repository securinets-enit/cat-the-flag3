'use strict';

const path = require('path');
const { fork } = require('child_process');

/*
 * Launches the maintenance worker as a Node child process.
 *
 * The child options bag is assembled by copying the configured job defaults onto
 * a fresh object. This shallow copy walks the source with for..in, which also
 * visits INHERITED enumerable properties — so if Object.prototype has been
 * polluted with an `execArgv`, it becomes an OWN property of `options`, and
 * fork() launches the worker with those flags.
 *
 * (On modern Node, passing a bare {} whose prototype is polluted does NOT work:
 * child_process copies options reading own properties only. The vulnerability is
 * precisely this config-copy materialising the inherited value as own.)
 */
function buildJobOptions() {
  // stdout/stderr are piped so the admin console can display the job's log; an
  // IPC channel is required by fork(). execArgv is intentionally NOT set here —
  // if Object.prototype has been polluted, the for..in below copies it in.
  const configured = { cwd: __dirname, stdio: ['ignore', 'pipe', 'pipe', 'ipc'] };
  const options = {};
  for (const key in configured) {
    options[key] = configured[key];
  }
  return options;
}

// Runs the worker and resolves with its captured output. The admin endpoint
// returns this log to the caller — which is the (intended) exfil channel once
// the forked node is running attacker-controlled flags.
function runMaintenanceJob() {
  const worker = path.join(__dirname, 'worker.js');
  return new Promise((resolve) => {
    let out = '';
    let done = false;
    const finish = (code) => {
      if (done) return;
      done = true;
      resolve({ code, log: out });
    };
    const child = fork(worker, [], buildJobOptions());
    if (child.stdout) child.stdout.on('data', (d) => (out += d.toString()));
    if (child.stderr) child.stderr.on('data', (d) => (out += d.toString()));
    child.on('error', () => finish(-1));
    child.on('exit', (code) => finish(code));
    // Safety valve so a hung job can't wedge the request.
    setTimeout(() => {
      try { child.kill('SIGKILL'); } catch (_) {}
      finish(-1);
    }, 5000);
  });
}

module.exports = { runMaintenanceJob, buildJobOptions };
