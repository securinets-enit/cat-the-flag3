'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const express = require('express');
const cookieParser = require('cookie-parser');
const { createBot } = require('./bot');
const views = require('./views');

const PORT = parseInt(process.env.PORT || '8007', 10);
const INTERNAL_BASE = `http://127.0.0.1:${PORT}`;
const PUBLIC_ORIGIN = process.env.PUBLIC_ORIGIN || '';

const FLAG = fs
  .readFileSync(path.join(__dirname, 'flag.txt'), 'utf8')
  .trim();

const users = new Map();
const sessions = new Map();

function newToken() {
  return crypto.randomBytes(24).toString('hex');
}

users.set('admin', {
  password: crypto.randomBytes(18).toString('hex'),
  bio: 'Portal administrator.',
});
const ADMIN_TOKEN = newToken();
sessions.set(ADMIN_TOKEN, 'admin');

const app = express();
app.disable('x-powered-by');
app.use(cookieParser());
app.use(express.urlencoded({ extended: false }));
app.use(express.static(path.join(__dirname, 'public')));

app.use((req, _res, next) => {
  const token = req.cookies && req.cookies.session;
  req.username = (token && sessions.get(token)) || null;
  next();
});

function setSession(res, username) {
  const token = newToken();
  sessions.set(token, username);
  res.cookie('session', token, {
    httpOnly: true,
    sameSite: 'lax',
    path: '/',
  });
}

app.get('/login', (req, res) => {
  if (req.username) return res.redirect('/');
  res.send(views.loginPage({ error: null }));
});

app.post('/login', (req, res) => {
  const { username, password } = req.body;
  const u = users.get(username);
  if (!u || u.password !== password) {
    return res
      .status(401)
      .send(views.loginPage({ error: 'Invalid username or password.' }));
  }
  setSession(res, username);
  res.redirect('/');
});

app.get('/signup', (req, res) => {
  if (req.username) return res.redirect('/');
  res.send(views.signupPage({ error: null }));
});

app.post('/signup', (req, res) => {
  const username = (req.body.username || '').trim();
  const password = req.body.password || '';
  if (!username || !password) {
    return res
      .status(400)
      .send(views.signupPage({ error: 'Username and password are required.' }));
  }
  if (users.has(username)) {
    return res
      .status(409)
      .send(views.signupPage({ error: 'That username is taken.' }));
  }
  users.set(username, { password, bio: '' });
  setSession(res, username);
  res.redirect('/');
});

app.post('/logout', (req, res) => {
  const token = req.cookies && req.cookies.session;
  if (token) sessions.delete(token);
  res.clearCookie('session', { path: '/' });
  res.redirect('/login');
});

app.get('/', (req, res) => {
  if (!req.username) return res.redirect('/login');
  res.send(views.homePage({ user: req.username }));
});

app.get('/dashboard', (req, res) => {
  if (!req.username) return res.redirect('/login');
  const u = users.get(req.username);
  res.send(
    views.dashboardPage({
      user: req.username,
      bio: u ? u.bio : '',
      saved: req.query.saved === '1',
    })
  );
});

app.post('/settings/bio', (req, res) => {
  if (!req.username) return res.status(401).send('login required');
  const u = users.get(req.username);
  if (u) u.bio = req.body.bio || '';
  res.redirect('/dashboard?saved=1');
});

app.get('/profile/:username', (req, res) => {
  if (!req.username) return res.redirect('/login');
  const target = req.params.username;
  if (target === 'admin' && req.username !== 'admin') {
    return res.status(403).send(
      views.messagePage({
        user: req.username,
        title: 'Forbidden',
        message: 'That profile is private.',
        back: '/',
      })
    );
  }
  const u = users.get(target);
  if (!u) {
    return res.status(404).send(
      views.messagePage({
        user: req.username,
        title: 'Not found',
        message: 'No such user.',
        back: '/',
      })
    );
  }
  res.set('Content-Security-Policy', "default-src 'self'");
  res.send(
    views.profilePage({
      viewerUser: req.username,
      profileUser: target,
      bio: u.bio,
    })
  );
});

app.post('/password-reset', (req, res) => {
  if (!req.username) {
    return res.status(401).send('Not authenticated.');
  }
  const password = req.body.password;
  if (!password) return res.status(400).send('password required');
  const u = users.get(req.username);
  if (u) u.password = password;
  res.redirect('/dashboard?saved=1');
});

app.get('/admin', (req, res) => {
  if (!req.username) return res.redirect('/login');
  if (req.username !== 'admin') {
    return res.status(403).send(
      views.messagePage({
        user: req.username,
        title: 'Forbidden',
        message: 'Admin access only.',
        back: '/',
      })
    );
  }
  res.send(views.adminPage({ user: req.username, flag: FLAG }));
});

const bot = createBot({ internalBase: INTERNAL_BASE, adminToken: ADMIN_TOKEN });

function allowedHosts(req) {
  const hosts = new Set(['localhost', '127.0.0.1']);
  if (req.headers.host) hosts.add(req.headers.host.split(':')[0]);
  if (PUBLIC_ORIGIN) {
    try {
      hosts.add(new URL(PUBLIC_ORIGIN).hostname);
    } catch (_) {}
  }
  return hosts;
}

app.post('/report', (req, res) => {
  if (!req.username) return res.status(401).send('login required');
  const raw = req.body.url || '';
  let parsed;
  try {
    parsed = new URL(raw);
  } catch (_) {
    return res.status(400).send(
      views.messagePage({
        user: req.username,
        title: 'Invalid link',
        message: 'That does not look like a valid URL.',
        back: '/',
      })
    );
  }

  if (!allowedHosts(req).has(parsed.hostname)) {
    return res.status(400).send(
      views.messagePage({
        user: req.username,
        title: 'Link rejected',
        message:
          'The admin only reviews profile links on the Meridian portal itself.',
        back: '/',
      })
    );
  }

  if (!/^\/profile\/[^/]+$/.test(parsed.pathname)) {
    return res.status(400).send(
      views.messagePage({
        user: req.username,
        title: 'Link rejected',
        message:
          'The admin only reviews user profile links, e.g. /profile/<username>.',
        back: '/',
      })
    );
  }

  const target = INTERNAL_BASE + parsed.pathname;
  bot.enqueue(target);

  res.send(
    views.messagePage({
      user: req.username,
      title: 'Reported',
      message:
        'Thanks. The admin will review the reported profile link shortly.',
      back: '/',
    })
  );
});

app.listen(PORT, () => {
  console.log(`[app]  Meridian portal on ${INTERNAL_BASE}  (PORT=${PORT})`);
  console.log(`[app]  public origin: ${PUBLIC_ORIGIN || '(not set)'}`);
  console.log(`[bot]  admin session seeded`);
});
