'use strict';

// Shared tiny helper.
async function postJSON(url, body) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  let data = {};
  try { data = await res.json(); } catch (_) {}
  return { res, data };
}

// ---------- Auth page ----------
const authForm = document.getElementById('auth-form');
if (authForm) {
  authForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const mode = authForm.dataset.mode; // 'login' | 'signup'
    const fd = new FormData(authForm);
    const { res, data } = await postJSON('/api/' + mode, {
      username: fd.get('username'),
      password: fd.get('password'),
    });
    const err = document.getElementById('err');
    if (res.ok) {
      window.location = '/';
    } else {
      err.textContent = data.error || 'Request failed.';
      err.style.display = '';
    }
  });
}

// ---------- Dashboard ----------
const ctx = window.__MIRAGE__;
if (ctx) {
  // Silently load the operator's own record. (This GET is what surfaces the
  // /users/:id endpoint in the Network tab.)
  fetch('/users/' + ctx.uid)
    .then((r) => r.json())
    .then((rec) => {
      const p = (rec && rec.profile) || {};
      const view = document.getElementById('profile-view');
      if (view) {
        view.innerHTML =
          '<dt>Display name</dt><dd>' + escapeHtml(p.displayName) + '</dd>' +
          '<dt>Title</dt><dd>' + escapeHtml(p.title) + '</dd>' +
          '<dt>Theme</dt><dd>' + escapeHtml(p.theme) + '</dd>' +
          '<dt>Operator ID</dt><dd>' + escapeHtml(String(rec.id)) + '</dd>';
      }
      const form = document.getElementById('profile-form');
      if (form) {
        if (form.displayName) form.displayName.value = p.displayName || '';
        if (form.title) form.title.value = p.title || '';
        if (form.theme && p.theme) form.theme.value = p.theme;
      }
    })
    .catch(() => {});

  // Save profile -> POST /users/:id with a JSON body (the merge endpoint).
  const profileForm = document.getElementById('profile-form');
  if (profileForm) {
    profileForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const fd = new FormData(profileForm);
      const { res } = await postJSON('/users/' + ctx.uid, {
        displayName: fd.get('displayName'),
        title: fd.get('title'),
        theme: fd.get('theme'),
      });
      const ok = document.getElementById('profile-saved');
      if (ok) { ok.style.display = res.ok ? '' : 'none'; }
    });
  }

  // Admin-only: trigger the maintenance worker.
  const runBtn = document.getElementById('run-job');
  if (runBtn) {
    runBtn.addEventListener('click', async () => {
      const log = document.getElementById('joblog');
      const { res, data } = await postJSON('/admin/maintenance', {});
      if (log) {
        log.style.display = '';
        log.textContent = res.ok
          ? '[index-rebuild] exit ' + data.code + '\n' + (data.log || '(no output)')
          : 'error: ' + (data.error || res.status);
      }
    });
  }

  // Report form — compliance rabbit hole. Purely client-side; goes nowhere.
  const reportForm = document.getElementById('report-form');
  if (reportForm) {
    reportForm.addEventListener('submit', (e) => {
      e.preventDefault();
      reportForm.reset();
      const ok = document.getElementById('report-ok');
      if (ok) ok.style.display = '';
    });
  }

  // Sign out.
  const signout = document.getElementById('signout');
  if (signout) {
    signout.addEventListener('click', async () => {
      await fetch('/api/logout', { method: 'POST' });
      window.location = '/login';
    });
  }
}

function escapeHtml(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
