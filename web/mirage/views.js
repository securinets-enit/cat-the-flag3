'use strict';

const esc = (s) =>
  String(s == null ? '' : s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');

const LOGO = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 20h20"/><path d="M5 20V9l4-3 4 3"/><path d="M13 20V5l6 4v11"/><path d="M8 12h.01"/><path d="M16 12h.01"/><path d="M16 16h.01"/></svg>`;

function layout({ title, signedIn, body, head }) {
  const nav = signedIn
    ? `
      <nav class="nav">
        <a class="brand" href="/"><span class="logo">${LOGO}</span>Mirage<span class="sub">Industrial Systems</span></a>
        <div class="spacer"></div>
        <a href="/">Dashboard</a>
        <button class="link" id="signout">Sign out</button>
      </nav>`
    : `
      <nav class="nav">
        <a class="brand" href="/login"><span class="logo">${LOGO}</span>Mirage<span class="sub">Industrial Systems</span></a>
        <div class="spacer"></div>
        <a href="/login">Sign in</a>
        <a href="/signup">Request access</a>
      </nav>`;

  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${esc(title)} · Mirage Portal</title>
  <link rel="stylesheet" href="/style.css">
  ${head || ''}
</head>
<body>
  ${nav}
  <main class="wrap">
    ${body}
  </main>
  <footer class="foot">Mirage Industrial Systems · internal operations portal · authorized personnel only</footer>
</body>
</html>`;
}

function loginPage({ mode, error }) {
  const isSignup = mode === 'signup';
  const body = `
    <div class="auth">
      <div class="auth-badge">${LOGO}</div>
      <h1>${isSignup ? 'Request portal access' : 'Operator sign-in'}</h1>
      <p class="muted">${
        isSignup
          ? 'Create an operator account for the Mirage control portal.'
          : 'Sign in to the Mirage control portal.'
      }</p>
      <div class="err" id="err" ${error ? '' : 'style="display:none"'}>${esc(error || '')}</div>
      <form id="auth-form" data-mode="${isSignup ? 'signup' : 'login'}">
        <label>Operator ID <input name="username" autocomplete="username" autofocus required></label>
        <label>Passphrase <input name="password" type="password" autocomplete="current-password" required></label>
        <button class="btn wide" type="submit">${isSignup ? 'Create account' : 'Sign in'}</button>
      </form>
      <p class="muted">${
        isSignup
          ? 'Already provisioned? <a href="/login">Sign in</a>.'
          : 'Need an account? <a href="/signup">Request access</a>.'
      }</p>
    </div>
    <script src="/app.js"></script>`;
  return layout({ title: isSignup ? 'Request access' : 'Sign in', signedIn: false, body });
}

function dashboardPage({ jwt }) {
  const head = `<script>
    window.__MIRAGE__ = ${JSON.stringify({
      uid: jwt.uid,
      username: jwt.sub,
      role: jwt.role,
    })};
  </script>`;

  const body = `
    <header class="hero">
      <h1>Control dashboard</h1>
      <p class="muted">Signed in as <b>${esc(jwt.sub)}</b>
        <span class="role ${jwt.role === 'admin' ? 'role-admin' : ''}">role: ${esc(jwt.role)}</span>
      </p>
    </header>

    <section class="grid">
      <article class="card">
        <h3>Shift status</h3>
        <ul class="status">
          <li><span class="dot ok"></span> Line A — nominal</li>
          <li><span class="dot ok"></span> Line B — nominal</li>
          <li><span class="dot warn"></span> Coolant loop 3 — maintenance due</li>
        </ul>
        <p class="muted small">Telemetry refreshed every shift change.</p>
      </article>

      <article class="card" id="profile-card">
        <h3>Operator profile</h3>
        <dl class="kv" id="profile-view"><dt>Loading…</dt><dd></dd></dl>
        <details class="editor">
          <summary>Edit profile</summary>
          <form id="profile-form">
            <label>Display name <input name="displayName" required></label>
            <label>Title <input name="title"></label>
            <label>Theme
              <select name="theme"><option value="dark">dark</option><option value="light">light</option></select>
            </label>
            <button class="btn" type="submit">Save profile</button>
          </form>
          <div class="ok-msg" id="profile-saved" style="display:none">Profile saved.</div>
        </details>
      </article>

      <article class="card ${jwt.role === 'admin' ? '' : 'locked'}" id="admin-card">
        <h3>${jwt.role === 'admin' ? '🛠️' : '🔒'} Maintenance jobs</h3>
        <p class="muted">Operational maintenance (search-index rebuild, telemetry
          compaction) runs server-side worker jobs.</p>
        ${
          jwt.role === 'admin'
            ? ''
            : `<div class="denied" id="admin-denied">
          Access denied — your role (<b>${esc(jwt.role)}</b>) cannot run maintenance
          jobs. This console is restricted to <b>administrators</b>.
        </div>`
        }
        <button class="btn" id="run-job" ${jwt.role === 'admin' ? '' : 'disabled'}>Run index rebuild</button>
        <pre class="joblog" id="joblog" style="display:none"></pre>
      </article>

      <article class="card">
        <h3>Report a concern</h3>
        <p class="muted">Flag a portal page or operator profile for the compliance
          team to review.</p>
        <form id="report-form" class="row">
          <input name="url" type="text" placeholder="/users/… or page path" required>
          <button class="btn">Submit report</button>
        </form>
        <div class="ok-msg" id="report-ok" style="display:none">Thanks — compliance will review this shortly.</div>
      </article>
    </section>

    <script src="/app.js"></script>`;

  return layout({ title: 'Dashboard', signedIn: true, body, head });
}

module.exports = { esc, layout, loginPage, dashboardPage };
