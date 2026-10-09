
const esc = (s) =>
  String(s == null ? '' : s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');

function layout({ title, user, body, wide }) {
  const nav = user
    ? `
      <nav class="nav">
        <a class="brand" href="/"><span class="logo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 3 9l9 13 9-13z"/><path d="M3 9h18"/><path d="M12 2v20"/></svg></span>Meridian</a>
        <div class="spacer"></div>
        <a href="/">Home</a>
        <a href="/dashboard">My profile</a>
        <span class="who">${esc(user)}</span>
        <form method="POST" action="/logout" class="inline">
          <button class="link">Sign out</button>
        </form>
      </nav>`
    : `
      <nav class="nav">
        <a class="brand" href="/"><span class="logo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 3 9l9 13 9-13z"/><path d="M3 9h18"/><path d="M12 2v20"/></svg></span>Meridian</a>
        <div class="spacer"></div>
        <a href="/login">Sign in</a>
        <a href="/signup">Create account</a>
      </nav>`;

  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${esc(title)} · Meridian Portal</title>
  <link rel="stylesheet" href="/style.css">
</head>
<body>
  ${nav}
  <main class="${wide ? 'wrap wide' : 'wrap'}">
    ${body}
  </main>
  <footer class="foot">Meridian Internal Portal · authorized personnel only</footer>
</body>
</html>`;
}

function homePage({ user }) {
  const body = `
    <div id="notice" class="notice" style="display:none"></div>

    <header class="hero">
      <h1>Welcome back, ${esc(user)}</h1>
      <p class="muted">Meridian internal portal — announcements, directory, and reporting.</p>
    </header>

    <section class="cards">
      <article class="card">
        <h3>📣 Announcements</h3>
        <p>Q3 all-hands moved to Thursday 14:00. VPN maintenance window Friday
           night. Please rotate your credentials before the audit.</p>
      </article>
      <article class="card">
        <h3>👤 Your profile</h3>
        <p>Set a display bio and manage your account.</p>
        <a class="btn ghost" href="/dashboard">Open my profile</a>
      </article>
    </section>

    <section class="card report">
      <h3>🚩 Report a user profile</h3>
      <p class="muted">Paste a link to a user profile that violates policy. Our
         admin reviews every reported link in a browser.</p>
      <form method="POST" action="/report" class="row">
        <input type="url" name="url" placeholder="http://…/profile link" required>
        <button class="btn">Report to admin</button>
      </form>
    </section>

    <script src="/app.js"></script>
  `;
  return layout({ title: 'Home', user, body });
}

function loginPage({ error }) {
  const body = `
    <div class="auth">
      <h1>Sign in</h1>
      ${error ? `<div class="err">${esc(error)}</div>` : ''}
      <form method="POST" action="/login">
        <label>Username <input name="username" autofocus required></label>
        <label>Password <input name="password" type="password" required></label>
        <button class="btn wide">Sign in</button>
      </form>
      <p class="muted">No account? <a href="/signup">Create one</a>.</p>
    </div>`;
  return layout({ title: 'Sign in', user: null, body });
}

function signupPage({ error }) {
  const body = `
    <div class="auth">
      <h1>Create account</h1>
      ${error ? `<div class="err">${esc(error)}</div>` : ''}
      <form method="POST" action="/signup">
        <label>Username <input name="username" autofocus required></label>
        <label>Password <input name="password" type="password" required></label>
        <button class="btn wide">Create account</button>
      </form>
      <p class="muted">Already have one? <a href="/login">Sign in</a>.</p>
    </div>`;
  return layout({ title: 'Create account', user: null, body });
}

function dashboardPage({ user, bio, saved }) {
  const body = `
    <h1>${esc(user)}</h1>
    ${saved ? `<div class="ok">Profile saved.</div>` : ''}

    <section class="card">
      <h3>Your public profile</h3>
      <p class="muted">Anyone at Meridian can view your profile page — and it's
         what the admin opens when a profile is reported.</p>
      <a class="btn ghost" href="/profile/${encodeURIComponent(user)}">View my public profile → /profile/${esc(user)}</a>
    </section>

    <section class="card">
      <h3>Bio preview</h3>
      <div class="bio">${bio || '<span class="muted">No bio yet.</span>'}</div>
    </section>

    <section class="card">
      <h3>Edit bio</h3>
      <form method="POST" action="/settings/bio">
        <textarea name="bio" rows="4" placeholder="Tell the team about yourself">${esc(bio)}</textarea>
        <button class="btn">Save profile</button>
      </form>
    </section>

    <section class="card">
      <h3>Change password</h3>
      <p class="muted">Set a new password. (No current password required — legacy
         convenience endpoint.)</p>
      <form method="POST" action="/password-reset">
        <label>New password <input name="password" type="password" required></label>
        <button class="btn">Update password</button>
      </form>
    </section>`;
  return layout({ title: 'My profile', user, body });
}

function profilePage({ viewerUser, profileUser, bio }) {
  const body = `
    <section class="card">
      <h1>${esc(profileUser)}</h1>
      <p class="muted">Public profile</p>
      <div class="bio">${bio || '<span class="muted">No bio yet.</span>'}</div>
    </section>
    ${
      viewerUser === profileUser
        ? `<a class="btn ghost" href="/dashboard">Edit my profile</a>`
        : `<a class="btn ghost" href="/">Back</a>`
    }`;
  return layout({ title: profileUser + ' · profile', user: viewerUser, body });
}

function adminPage({ user, flag }) {
  const body = `
    <div class="admin">
      <h1>🔐 Admin console</h1>
      <p>Signed in as <b>${esc(user)}</b>.</p>
      <div class="flag">${esc(flag)}</div>
    </div>`;
  return layout({ title: 'Admin', user, body });
}

function messagePage({ user, title, message, back }) {
  const body = `
    <div class="card">
      <h1>${esc(title)}</h1>
      <p>${esc(message)}</p>
      ${back ? `<a class="btn ghost" href="${esc(back)}">Back</a>` : ''}
    </div>`;
  return layout({ title, user: user || null, body });
}

module.exports = {
  esc,
  layout,
  homePage,
  loginPage,
  signupPage,
  dashboardPage,
  profilePage,
  adminPage,
  messagePage,
};
