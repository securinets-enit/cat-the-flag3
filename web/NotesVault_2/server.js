'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const express = require('express');
const cookieParser = require('cookie-parser');
const { createBot } = require('./bot');
const views = require('./views');

const PORT = parseInt(process.env.PORT || '3000', 10);
const INTERNAL_BASE = `http://127.0.0.1:${PORT}`;
const PUBLIC_ORIGIN = process.env.PUBLIC_ORIGIN || '';

const FLAG = fs.readFileSync(path.join(__dirname, 'flag.txt'), 'utf8').trim();

const users = new Map();
const sessions = new Map();
const notes = new Map();

function newToken() {
  return crypto.randomBytes(24).toString('hex');
}

notes.set('welcome', {
  title: 'Welcome Note',
  content: 'Welcome to Vault v3. Address a note by slug in the URL fragment, e.g. #file=welcome.',
  owner: null,
  public: true,
});

users.set('admin', {
  password: crypto.randomBytes(18).toString('hex'),
  notes: new Set(),
});

const ADMIN_TOKEN = newToken();
sessions.set(ADMIN_TOKEN, 'admin');

const app = express();
app.disable('x-powered-by');
app.use(cookieParser());
app.use(express.urlencoded({ extended: false }));
app.use(express.static(path.join(__dirname, 'public'), { index: false }));

app.use((req, _res, next) => {
  const token = req.cookies && req.cookies.session;
  req.username = (token && sessions.get(token)) || null;
  next();
});

function safeDecode(value) {
  try {
    return decodeURIComponent(value);
  } catch (_) {
    return value;
  }
}

app.use('/api', (req, res, next) => {
  const raw = req.originalUrl;
  if (raw.includes('..') || safeDecode(raw).includes('..')) {
    return res.status(403).json({ error: 'WAF: Path Traversal Detected (..)' });
  }
  if (/%2f|%2F|%5c|%5C/.test(raw)) {
    return res.status(403).json({ error: 'WAF: Encoded Slashes Prohibited' });
  }
  if (/%25/.test(raw)) {
    return res.status(403).json({ error: 'WAF: Double Encoding Detected' });
  }
  next();
});

function setSession(res, username) {
  const token = newToken();
  sessions.set(token, username);
  res.cookie('session', token, { httpOnly: true, sameSite: 'lax', path: '/' });
}

app.get('/login', (req, res) => {
  if (req.username) return res.redirect('/');
  res.send(views.loginPage({ error: null }));
});

app.post('/login', (req, res) => {
  const { username, password } = req.body;
  const u = users.get(username);
  if (!u || u.password !== password) {
    return res.status(401).send(views.loginPage({ error: 'Invalid username or password.' }));
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
    return res.status(400).send(views.signupPage({ error: 'Username and password are required.' }));
  }
  if (users.has(username)) {
    return res.status(409).send(views.signupPage({ error: 'That username is taken.' }));
  }
  users.set(username, { password, notes: new Set() });
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

app.get('/profile', (req, res) => {
  if (!req.username) return res.redirect('/login');
  res.send(views.profilePage({ user: req.username, changed: req.query.changed === '1' }));
});

app.get('/admin', (req, res) => {
  if (!req.username) return res.redirect('/login');
  if (req.username !== 'admin') {
    return res.status(403).send(views.messagePage({
      user: req.username,
      title: 'Forbidden',
      message: 'Admins only.',
      back: '/',
    }));
  }
  res.send(views.adminPage({ user: req.username, flag: FLAG }));
});

app.get('/api/v1/notes/:noteId', (req, res) => {
  const note = notes.get(req.params.noteId);
  if (!note) return res.status(404).json({ error: 'Note not found' });
  if (!note.public && note.owner !== req.username) {
    return res.status(403).json({ error: 'This note is private.' });
  }
  res.json({ title: note.title, content: note.content });
});

app.post('/api/v1/notes/:noteId', (req, res) => {
  if (!req.username) return res.status(401).json({ error: 'login required' });
  const id = req.params.noteId;
  const existing = notes.get(id);
  if (existing && existing.owner && existing.owner !== req.username) {
    return res.status(403).json({ error: 'Not your note.' });
  }
  notes.set(id, {
    title: id,
    content: String(req.body.content || ''),
    owner: req.username,
    public: false,
  });
  res.json({ ok: true, id });
});

app.get('/api/v1/admin/flag', (req, res) => {
  if (req.username !== 'admin') return res.status(403).json({ error: 'Admins only.' });
  res.json({ title: 'Flag', content: FLAG });
});

app.post('/api/v1/profile/password', (req, res) => {
  if (!req.username) return res.status(401).json({ error: 'login required' });
  const password = req.body.password;
  if (!password) return res.status(400).json({ error: 'password required' });
  const u = users.get(req.username);
  if (u) u.password = password;
  if ((req.get('accept') || '').includes('text/html')) {
    return res.redirect('/profile?changed=1');
  }
  res.json({ ok: true });
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
    return res.status(400).send(views.messagePage({
      user: req.username,
      title: 'Invalid link',
      message: 'That does not look like a valid URL.',
      back: '/',
    }));
  }

  if (!allowedHosts(req).has(parsed.hostname)) {
    return res.status(400).send(views.messagePage({
      user: req.username,
      title: 'Link rejected',
      message: 'The admin only reviews Vault links on this origin.',
      back: '/',
    }));
  }

  if (parsed.pathname !== '/') {
    return res.status(400).send(views.messagePage({
      user: req.username,
      title: 'Link rejected',
      message: 'The admin only opens the main notes page, e.g. /#file=welcome.',
      back: '/',
    }));
  }

  bot.enqueue(INTERNAL_BASE + '/' + parsed.hash);

  res.send(views.messagePage({
    user: req.username,
    title: 'Reported',
    message: 'Thanks. The admin will review your note link shortly.',
    back: '/',
  }));
});

app.listen(PORT, () => {
  console.log(`[app] Notes Vault v3 on ${INTERNAL_BASE} (PORT=${PORT})`);
  console.log(`[app] public origin: ${PUBLIC_ORIGIN || '(not set)'}`);
  console.log('[bot] admin session seeded');
});
