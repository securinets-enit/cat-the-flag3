'use strict';

function esc(value) {
  return String(value).replace(/[&<>"']/g, (c) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  }[c]));
}

function layout({ title, user, body }) {
  const nav = user
    ? `<a href="/">Notes</a><a href="/profile">Profile</a>
       <form class="inline" method="POST" action="/logout"><button class="link">Sign out (${esc(user)})</button></form>`
    : '';
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)} · Notes Vault</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<header>
  <span class="brand">Notes Vault <b>v3</b></span>
  <nav>${nav}</nav>
</header>
<main>${body}</main>
</body>
</html>`;
}

function authCard({ title, action, submit, alt, error }) {
  return `<div class="card narrow">
  <h1>${esc(title)}</h1>
  ${error ? `<p class="error">${esc(error)}</p>` : ''}
  <form method="POST" action="${esc(action)}">
    <label>Username<input name="username" autocomplete="username"></label>
    <label>Password<input name="password" type="password" autocomplete="current-password"></label>
    <button type="submit">${esc(submit)}</button>
  </form>
  <p class="muted">${alt}</p>
</div>`;
}

function loginPage({ error }) {
  return layout({
    title: 'Sign in',
    user: null,
    body: authCard({
      title: 'Sign in',
      action: '/login',
      submit: 'Sign in',
      alt: 'No account? <a href="/signup">Create one</a>.',
      error,
    }),
  });
}

function signupPage({ error }) {
  return layout({
    title: 'Sign up',
    user: null,
    body: authCard({
      title: 'Create an account',
      action: '/signup',
      submit: 'Sign up',
      alt: 'Already registered? <a href="/login">Sign in</a>.',
      error,
    }),
  });
}

function homePage({ user }) {
  const body = `
  <div class="card">
    <h1 id="title">Loading…</h1>
    <p id="content" class="muted">Fetching note…</p>
  </div>

  <div class="card">
    <h2>Report a note link</h2>
    <p class="muted">The administrator reviews reported note links in a real browser.</p>
    <form method="POST" action="/report">
      <label>Note link<input name="url" placeholder="http://…/#file=welcome" size="52"></label>
      <button type="submit">Report to admin</button>
    </form>
  </div>
  <script src="/app.js"></script>`;
  return layout({ title: `${user}'s notes`, user, body });
}

function profilePage({ user, changed }) {
  const body = `
  <div class="card">
    <h1>Profile</h1>
    <p class="muted">Signed in as <b>${esc(user)}</b>.</p>
    ${changed ? '<p class="ok">Password updated.</p>' : ''}
    <h2>Change password</h2>
    <form method="POST" action="/api/v1/profile/password">
      <label>New password<input name="password" type="password" autocomplete="new-password"></label>
      <button type="submit">Update password</button>
    </form>
  </div>`;
  return layout({ title: 'Profile', user, body });
}

function adminPage({ user, flag }) {
  const body = `
  <div class="card">
    <h1>Admin vault</h1>
    <p class="muted">Only the administrator can read this note.</p>
    <pre class="flag">${esc(flag)}</pre>
  </div>`;
  return layout({ title: 'Admin', user, body });
}

function messagePage({ user, title, message, back }) {
  const body = `
  <div class="card narrow">
    <h1>${esc(title)}</h1>
    <p>${esc(message)}</p>
    <p><a href="${esc(back)}">Back</a></p>
  </div>`;
  return layout({ title, user, body });
}

module.exports = {
  loginPage,
  signupPage,
  homePage,
  profilePage,
  adminPage,
  messagePage,
};
